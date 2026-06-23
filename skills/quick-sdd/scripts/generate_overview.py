#!/usr/bin/env python3
"""Generate a professional HTML overview from codespec feature files.

Reads proposal.md, stories.md, architecture.md, tasks.md from a feature
directory and produces a single overview.html for quick comprehension.

CSS/JS templates are read from skills/quick-sdd/templates/html/ by default,
ensuring style consistency across all projects using the quick-sdd skill.
If template files are not found, embedded fallback constants are used.

Usage:
    python generate_overview.py <feature_dir>
    python generate_overview.py codespec/specs/FEAT-001-角色专业能力赋能
"""

import argparse
import json
import re
import sys
import html
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates" / "html"

FEATURE_DIR_RE = re.compile(r"^FEAT-(\d+)(?:-.+)?$")
HTML_CONFIG_RE = re.compile(
    r"<!--\s*QUICK-SDD-HTML-START\s*-->(?P<body>.*?)<!--\s*QUICK-SDD-HTML-END\s*-->",
    re.DOTALL | re.IGNORECASE,
)


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_text(path):
    return path.read_text(encoding="utf-8-sig")


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def load_template_asset(name, fallback=None):
    """Load a template asset from the skills/quick-sdd/templates/html/ directory.

    Returns the file content if it exists, otherwise returns the fallback constant.
    This ensures style consistency: the template files are the canonical source
    of truth, and any project using the same skill version gets the same styles.
    """
    template_path = TEMPLATES_DIR / name
    if template_path.exists():
        return read_text(template_path)
    return fallback


def parse_bool(value, default=True):
    if isinstance(value, bool):
        return value
    normalized = str(value if value is not None else "").strip().lower()
    if normalized in {"true", "yes", "y", "1", "on", "enabled", "enable"}:
        return True
    if normalized in {"false", "no", "n", "0", "off", "disabled", "disable"}:
        return False
    return default


def html_export_enabled(repo_root):
    """Return whether automatic HTML generation is enabled by AGENTS.md.

    Default is enabled. The stable manual override lives in AGENTS.md:

    <!-- QUICK-SDD-HTML-START -->
    ```yaml
    quick_sdd:
      html_export:
        enabled: true
    ```
    <!-- QUICK-SDD-HTML-END -->
    """
    agents_path = Path(repo_root) / "AGENTS.md"
    if not agents_path.exists():
        return True
    text = read_text(agents_path)
    block_match = HTML_CONFIG_RE.search(text)
    search_text = block_match.group("body") if block_match else text

    if yaml:
        yaml_match = re.search(r"```yaml\s*\n(?P<yaml>.*?)\n```", search_text, re.DOTALL)
        if yaml_match:
            loaded = yaml.safe_load(yaml_match.group("yaml")) or {}
            html_export = (
                loaded.get("quick_sdd", {})
                .get("html_export", {})
                if isinstance(loaded, dict)
                else {}
            )
            if isinstance(html_export, dict) and "enabled" in html_export:
                return parse_bool(html_export.get("enabled"), default=True)

    enabled_match = re.search(r"\benabled\s*:\s*([^\s#]+)", search_text, re.IGNORECASE)
    if enabled_match:
        return parse_bool(enabled_match.group(1), default=True)

    inline_match = re.search(
        r"\bquick-sdd-html\s*:\s*(disabled|disable|false|off|0|enabled|enable|true|on|1)\b",
        search_text,
        re.IGNORECASE,
    )
    if inline_match:
        return parse_bool(inline_match.group(1), default=True)
    return True


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():].lstrip("\n")
    if yaml:
        return yaml.safe_load(raw) or {}, body
    meta = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip().strip("\"'")
            if v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                v = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
            meta[k.strip()] = v
    return meta, body


def extract_sections(md_text):
    sections = []
    current = {"level": 0, "title": "", "lines": []}
    in_code = False
    for line in md_text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            current["lines"].append(line)
            continue
        if in_code:
            current["lines"].append(line)
            continue
        hm = re.match(r"^(#{1,6})\s+(.+)$", line)
        if hm:
            if current["title"] or current["lines"]:
                sections.append(current)
            level = len(hm.group(1))
            current = {"level": level, "title": hm.group(2).strip(), "lines": []}
        else:
            current["lines"].append(line)
    if current["title"] or current["lines"]:
        sections.append(current)
    return sections


def md_to_html(md_text):
    lines = md_text.splitlines()
    out = []
    in_code = False
    code_lang = ""
    code_buf = []
    in_table = False
    table_rows = []
    in_list = False
    list_items = []

    def flush_list():
        nonlocal in_list, list_items
        if in_list and list_items:
            out.append("<ul>")
            for li in list_items:
                out.append(f"<li>{inline_md(li)}</li>")
            out.append("</ul>")
            list_items = []
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            out.append('<div class="table-wrap"><table>')
            for i, row in enumerate(table_rows):
                cells = [c.strip() for c in row.strip("|").split("|")]
                if i == 0:
                    out.append("<thead><tr>")
                    for c in cells:
                        out.append(f"<th>{inline_md(c)}</th>")
                    out.append("</tr></thead><tbody>")
                elif all(re.match(r"^[-:]+$", c.strip()) for c in cells if c.strip()):
                    continue
                else:
                    out.append("<tr>")
                    for c in cells:
                        out.append(f"<td>{inline_md(c)}</td>")
                    out.append("</tr>")
            out.append("</tbody></table></div>")
            table_rows = []
            in_table = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                if code_lang.lower() == "mermaid":
                    out.append(f'<pre class="mermaid">{"".join(code_buf)}</pre>')
                else:
                    out.append(f'<pre><code>{html.escape("".join(code_buf))}</code></pre>')
                code_buf = []
                in_code = False
            else:
                flush_list()
                flush_table()
                in_code = True
                code_lang = line.strip()[3:]
            continue
        if in_code:
            code_buf.append(line + "\n")
            continue

        stripped = line.strip()

        if "|" in stripped and stripped.startswith("|"):
            flush_list()
            if not in_table:
                in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            flush_table()

        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_table()
            if not in_list:
                in_list = True
            list_items.append(stripped[2:])
            continue
        elif in_list:
            flush_list()

        if stripped == "":
            flush_list()
            flush_table()
            continue

        if stripped.startswith("> "):
            flush_list()
            content = stripped[2:]
            out.append(f'<blockquote><p>{inline_md(content)}</p></blockquote>')
            continue

        out.append(f"<p>{inline_md(stripped)}</p>")

    flush_list()
    flush_table()
    if in_code and code_buf:
        if code_lang.lower() == "mermaid":
            out.append(f'<pre class="mermaid">{"".join(code_buf)}</pre>')
        else:
            out.append(f'<pre><code>{html.escape("".join(code_buf))}</code></pre>')

    return "\n".join(out)


def inline_md(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r'<code>\1</code>', text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def parse_stories(md_text):
    stories = []
    sections = extract_sections(md_text)
    current_story = None
    for sec in sections:
        if sec["level"] == 2 and sec["title"].startswith("索引"):
            continue
        hm = re.match(r"^(ST-\d+)\s+(.+)$", sec["title"])
        if hm and sec["level"] == 2:
            if current_story:
                stories.append(current_story)
            current_story = {
                "id": hm.group(1),
                "title": hm.group(2),
                "meta": {},
                "narrative": "",
                "ac": [],
                "out_of_scope": [],
                "content": [],
            }
            continue
        if current_story is None:
            continue
        body = "\n".join(sec["lines"])
        yaml_match = re.search(r"```yaml\s*\n(.*?)```", body, re.DOTALL)
        if yaml_match and sec["level"] <= 3:
            raw = yaml_match.group(1)
            if yaml:
                current_story["meta"] = yaml.safe_load(raw) or {}
            else:
                meta = {}
                for line in raw.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip()
                current_story["meta"] = meta
        if sec["title"].startswith("故事") or sec["title"].startswith("Story"):
            current_story["narrative"] = body.replace("```yaml", "").strip()
            yaml_end = re.search(r"```\s*\n", body)
            if yaml_end:
                current_story["narrative"] = body[yaml_end.end():].strip()
        elif sec["title"].startswith("验收标准"):
            for line in sec["lines"]:
                ac_match = re.match(r"^- `(AC-\d+)`:\s*(.+)$", line.strip())
                if ac_match:
                    current_story["ac"].append({"id": ac_match.group(1), "text": ac_match.group(2)})
        elif sec["title"].startswith("范围外"):
            for line in sec["lines"]:
                if line.strip().startswith("- "):
                    current_story["out_of_scope"].append(line.strip()[2:])
        if sec["level"] >= 2 and sec["title"]:
            current_story["content"].append(sec)
    if current_story:
        stories.append(current_story)
    return stories


def parse_tasks(md_text):
    tasks = []
    phases = []
    sections = extract_sections(md_text)
    current_task = None
    current_phase = None

    for sec in sections:
        if sec["title"].startswith("索引"):
            continue
        if sec["title"].startswith("编写说明"):
            continue

        phase_match = re.match(r"^阶段\s+([A-Z])\s+(.+)$", sec["title"])
        if phase_match and sec["level"] == 2:
            current_phase = {"id": phase_match.group(1), "title": phase_match.group(2), "tasks": []}
            phases.append(current_phase)
            continue

        task_match = re.match(r"^(T-\d+)\s+(.+)$", sec["title"])
        if task_match and sec["level"] == 2:
            if current_task:
                tasks.append(current_task)
                if current_phase:
                    current_phase["tasks"].append(current_task["id"])
            current_task = {
                "id": task_match.group(1),
                "title": task_match.group(2),
                "meta": {},
                "goal": [],
                "deliverables": [],
                "notes": [],
                "phase": current_phase["id"] if current_phase else "",
            }
            body = "\n".join(sec["lines"])
            yaml_match = re.search(r"```yaml\s*\n(.*?)```", body, re.DOTALL)
            if yaml_match:
                raw = yaml_match.group(1)
                if yaml:
                    current_task["meta"] = yaml.safe_load(raw) or {}
                else:
                    meta = {}
                    for line in raw.splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            meta[k.strip()] = v.strip()
                    current_task["meta"] = meta
            continue

        if current_task is None:
            continue

        if sec["title"].startswith("目标"):
            for line in sec["lines"]:
                if line.strip().startswith("- "):
                    current_task["goal"].append(line.strip()[2:])
        elif sec["title"].startswith("交付物"):
            for line in sec["lines"]:
                if line.strip().startswith("- "):
                    current_task["deliverables"].append(line.strip()[2:])
        elif sec["title"].startswith("备注"):
            for line in sec["lines"]:
                if line.strip().startswith("- "):
                    current_task["notes"].append(line.strip()[2:])

    if current_task:
        tasks.append(current_task)
    return tasks, phases


def status_class(status):
    s = str(status).lower().strip()
    if s in ("done", "pass", "accepted"):
        return "done"
    if s in (
        "ready",
        "in_progress",
        "conditional_pass",
        "draft",
        "proposal",
        "stories",
        "architecture",
        "planning",
        "task_review",
        "implementing",
        "validating",
        "accepting",
    ):
        return "ready"
    if s in ("todo", "pending", "fail", "rejected"):
        return "todo"
    return "draft"


def priority_class(p):
    p = str(p).upper()
    if "P0" in p:
        return "p0"
    if "P1" in p:
        return "p1"
    return "p2"


def feature_sort_key(feature_dir):
    match = FEATURE_DIR_RE.match(feature_dir.name)
    if match:
        return (int(match.group(1)), feature_dir.name)
    return (sys.maxsize, feature_dir.name)


def discover_feature_dirs(repo_root):
    specs_dir = Path(repo_root) / "codespec" / "specs"
    if not specs_dir.exists():
        return []
    feature_dirs = []
    for child in specs_dir.iterdir():
        if not child.is_dir():
            continue
        if not FEATURE_DIR_RE.match(child.name):
            continue
        if any((child / name).exists() for name in ("proposal.md", "stories.md", "architecture.md", "tasks.md")):
            feature_dirs.append(child)
    return sorted(feature_dirs, key=feature_sort_key)


def resolve_feature_dir(repo_root, feature):
    candidate = Path(feature)
    if candidate.is_dir():
        return candidate
    specs_dir = Path(repo_root) / "codespec" / "specs"
    exact = specs_dir / feature
    if exact.is_dir():
        return exact
    matches = [path for path in discover_feature_dirs(repo_root) if path.name.startswith(feature)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"Feature selector is ambiguous: {feature}")
    raise ValueError(f"Feature not found: {feature}")


def load_feature_summary(feature_dir):
    proposal_meta, proposal_body = {}, ""
    arch_meta = {}
    proposal_path = feature_dir / "proposal.md"
    arch_path = feature_dir / "architecture.md"
    if proposal_path.exists():
        proposal_meta, proposal_body = parse_frontmatter(read_text(proposal_path))
    if arch_path.exists():
        arch_meta, _ = parse_frontmatter(read_text(arch_path))
    fid = proposal_meta.get("id") or arch_meta.get("id") or feature_dir.name.split("-", 2)[0]
    title = proposal_meta.get("title") or arch_meta.get("title") or feature_dir.name
    status = proposal_meta.get("status") or arch_meta.get("status") or "draft"
    tasks_path = feature_dir / "tasks.md"
    if str(status).lower() == "draft" and tasks_path.exists():
        _, tasks_body = parse_frontmatter(read_text(tasks_path))
        tasks, _ = parse_tasks(tasks_body)
        if tasks and all(str(task["meta"].get("status", "")).lower() == "done" for task in tasks):
            status = "done"
    priority = proposal_meta.get("priority") or "P1"
    feature_type = proposal_meta.get("type") or "feature"
    description = ""
    for section in extract_sections(proposal_body):
        if section["title"] in {"目标", "问题", "简介", "1 简介"}:
            description = " ".join(
                line.strip().lstrip("- ").strip()
                for line in section["lines"]
                if line.strip() and not line.strip().startswith("<!--")
            )
            break
    return {
        "id": str(fid),
        "title": str(title),
        "status": str(status),
        "priority": str(priority),
        "type": str(feature_type),
        "description": description[:240],
        "dir_name": feature_dir.name,
    }


_CSS_FALLBACK = r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f8f9fb;--surface:#fff;--border:#e2e6ed;--border-light:#eef1f6;
  --text:#1a1d23;--text-sec:#5a6170;--text-mute:#8b92a0;
  --accent:#4f6ef7;--accent-l:#eef1ff;--accent-d:#3a56d4;
  --proposal:#e8793a;--proposal-bg:#fef4ee;
  --story:#7c5cbf;--story-bg:#f5f0ff;
  --arch:#2a9d8f;--arch-bg:#edf8f6;
  --task:#4f6ef7;--task-bg:#eef1ff;
  --done:#22c55e;--done-bg:#ecfdf5;
  --ready:#f59e0b;--ready-bg:#fffbeb;
  --todo:#94a3b8;--todo-bg:#f8fafc;
  --risk:#ef4444;--risk-bg:#fef2f2;
  --radius:8px;--radius-lg:12px;
  --shadow-sm:0 1px 2px rgba(0,0,0,.04);
  --shadow:0 1px 4px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
  --mono:"JetBrains Mono","Fira Code","SF Mono",Consolas,monospace;
  --sidebar-w:260px;
}
html{font-size:15px;scroll-behavior:smooth;scroll-padding-top:80px}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.65;-webkit-font-smoothing:antialiased}

.sidebar{position:fixed;top:0;left:0;width:var(--sidebar-w);height:100vh;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;z-index:100;transition:transform .25s ease}
.sidebar-hd{padding:20px 20px 16px;border-bottom:1px solid var(--border-light)}
.sidebar-hd .logo{font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--text-mute);margin-bottom:2px}
.sidebar-hd .fid{font-size:1.05rem;font-weight:700;color:var(--text)}
.sidebar-nav{flex:1;overflow-y:auto;padding:12px 0}
.nav-grp{padding:0 12px;margin-bottom:4px}
.nav-grp-title{font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--text-mute);padding:8px 8px 4px}
.sidebar-nav a{display:flex;align-items:center;gap:8px;padding:6px 12px;border-radius:var(--radius);font-size:.83rem;color:var(--text-sec);text-decoration:none;transition:all .15s ease}
.sidebar-nav a:hover{background:var(--bg);color:var(--text)}
.sidebar-nav a.active{background:var(--accent-l);color:var(--accent);font-weight:600}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot.p{background:var(--proposal)}.dot.s{background:var(--story)}.dot.a{background:var(--arch)}.dot.t{background:var(--task)}
.sidebar-ft{padding:12px 20px;border-top:1px solid var(--border-light);font-size:.72rem;color:var(--text-mute)}

.main{margin-left:var(--sidebar-w);min-height:100vh}
.topbar{position:sticky;top:0;z-index:50;background:rgba(248,249,251,.88);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:12px 40px;display:flex;align-items:center;gap:16px}
.topbar .bc{font-size:.85rem;color:var(--text-mute)}.topbar .bc strong{color:var(--text);font-weight:600}
.back-btn{display:inline-flex;align-items:center;gap:4px;padding:4px 12px;border-radius:var(--radius);font-size:.8rem;font-weight:600;color:var(--accent);background:var(--accent-l);text-decoration:none;border:1px solid transparent;transition:all .15s ease}
.back-btn:hover{border-color:var(--accent);background:#fff}
.back-btn svg{width:14px;height:14px}
.back-top{position:fixed;bottom:28px;right:28px;width:40px;height:40px;border-radius:50%;background:var(--accent);color:#fff;border:none;cursor:pointer;box-shadow:var(--shadow-lg);display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:all .2s ease;z-index:200}
.back-top.show{opacity:1;pointer-events:auto}
.back-top:hover{background:var(--accent-d);transform:translateY(-2px)}
.pill{margin-left:auto;display:flex;align-items:center;gap:6px;padding:4px 14px;border-radius:20px;font-size:.8rem;font-weight:600}
.pill.done{background:var(--done-bg);color:#15803d}.pill.ready{background:var(--ready-bg);color:#b45309}.pill.draft{background:#f1f5f9;color:#475569}

.content{max-width:940px;margin:0 auto;padding:32px 40px 80px}

.hero{margin-bottom:36px}
.hero h1{font-size:1.75rem;font-weight:800;line-height:1.3;margin-bottom:10px}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 12px;border-radius:20px;font-size:.78rem;font-weight:600;border:1px solid var(--border);background:var(--surface)}
.badge.p1{border-color:#fbbf24;background:#fffbeb;color:#92400e}
.badge.p0{border-color:var(--risk);background:var(--risk-bg);color:#991b1b}
.badge.type{border-color:var(--accent);background:var(--accent-l);color:var(--accent)}
.hero-desc{font-size:.93rem;color:var(--text-sec);max-width:680px;line-height:1.7}

.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:36px}
.stat{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:16px 20px;text-align:center}
.stat .n{font-size:1.6rem;font-weight:800;line-height:1}
.stat .l{font-size:.73rem;color:var(--text-mute);margin-top:4px;font-weight:500}
.stat.s1 .n{color:var(--proposal)}.stat.s2 .n{color:var(--story)}.stat.s3 .n{color:var(--arch)}.stat.s4 .n{color:var(--task)}

.section{margin-bottom:44px}
.sec-hd{display:flex;align-items:center;gap:10px;margin-bottom:18px;padding-bottom:10px;border-bottom:2px solid var(--border)}
.sec-ico{width:32px;height:32px;border-radius:var(--radius);display:flex;align-items:center;justify-content:center}
.sec-ico.p{background:var(--proposal-bg);color:var(--proposal)}
.sec-ico.s{background:var(--story-bg);color:var(--story)}
.sec-ico.a{background:var(--arch-bg);color:var(--arch)}
.sec-ico.t{background:var(--task-bg);color:var(--task)}
.sec-hd h2{font-size:1.2rem;font-weight:700}
.sec-cnt{margin-left:auto;font-size:.76rem;color:var(--text-mute);background:var(--bg);padding:2px 10px;border-radius:12px;font-weight:500}

.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:18px 22px;margin-bottom:14px;box-shadow:var(--shadow-sm);transition:box-shadow .15s ease}
.card:hover{box-shadow:var(--shadow)}
.card-hd{display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.cid{font-size:.73rem;font-weight:700;font-family:var(--mono);padding:2px 8px;border-radius:var(--radius);flex-shrink:0}
.cid.p{background:var(--proposal-bg);color:var(--proposal)}
.cid.s{background:var(--story-bg);color:var(--story)}
.cid.a{background:var(--arch-bg);color:var(--arch)}
.cid.t{background:var(--task-bg);color:var(--task)}
.ctitle{font-size:.93rem;font-weight:600;flex:1}
.cst{font-size:.72rem;font-weight:600;padding:2px 10px;border-radius:12px;flex-shrink:0}
.cst.done{background:var(--done-bg);color:#15803d}.cst.ready{background:var(--ready-bg);color:#b45309}.cst.todo{background:var(--todo-bg);color:#64748b}.cst.draft{background:#f1f5f9;color:#475569}

.prose{font-size:.88rem;color:var(--text-sec);line-height:1.7}
.prose ul,.prose ol{padding-left:18px;margin:4px 0}
.prose li{margin-bottom:3px}.prose li::marker{color:var(--text-mute)}
.prose p{margin-bottom:6px}
.prose code{font-family:var(--mono);font-size:.82em;background:var(--bg);padding:1px 5px;border-radius:4px;border:1px solid var(--border-light)}
.prose strong{color:var(--text);font-weight:600}
.prose pre{background:#1e1e2e;color:#cdd6f4;padding:14px 18px;border-radius:var(--radius);overflow-x:auto;font-size:.82rem;line-height:1.5;margin:8px 0}
.prose pre code{background:none;border:none;color:inherit;padding:0}
.prose blockquote{border-left:3px solid var(--accent);padding:8px 14px;margin:8px 0;background:var(--accent-l);border-radius:0 var(--radius) var(--radius) 0;font-size:.85rem;color:var(--text-sec)}
.prose table{width:100%;border-collapse:collapse;font-size:.83rem;margin:8px 0}
.prose th{text-align:left;padding:7px 10px;font-weight:600;color:var(--text-sec);border-bottom:2px solid var(--border);font-size:.76rem;text-transform:uppercase;letter-spacing:.04em}
.prose td{padding:7px 10px;border-bottom:1px solid var(--border-light);color:var(--text-sec);vertical-align:top}
.prose tr:hover td{background:var(--bg)}
.table-wrap{overflow-x:auto;margin:8px 0}

.subsec{margin-bottom:20px}
.subsec h3{font-size:1.02rem;font-weight:700;margin-bottom:6px;color:var(--text)}
.subsec h4{font-size:.9rem;font-weight:600;margin:10px 0 4px;color:var(--text-sec)}

.ac-list{list-style:none;padding:0;margin:6px 0}
.ac-item{display:flex;gap:10px;padding:8px 12px;margin-bottom:5px;background:var(--bg);border-radius:var(--radius);font-size:.84rem;border-left:3px solid var(--story)}
.ac-id{font-family:var(--mono);font-weight:700;color:var(--story);flex-shrink:0;font-size:.78rem}
.ac-text{color:var(--text-sec);line-height:1.6}

.dep{display:inline-flex;align-items:center;gap:3px;font-size:.73rem;font-family:var(--mono);padding:1px 7px;border-radius:4px;background:var(--bg);border:1px solid var(--border-light);color:var(--text-mute)}

.callout{display:flex;gap:12px;padding:12px 16px;border-radius:var(--radius);margin:10px 0;font-size:.84rem;line-height:1.6}
.callout.risk{background:var(--risk-bg);border-left:3px solid var(--risk);color:#991b1b}
.callout.info{background:var(--accent-l);border-left:3px solid var(--accent);color:#1e40af}
.callout-ok{background:var(--done-bg);border-left:3px solid var(--done);color:#15803d}
.callout svg{flex-shrink:0;margin-top:2px}

.task-toggle{display:inline-flex;align-items:center;gap:4px;font-size:.76px;color:var(--accent);cursor:pointer;font-weight:600;background:none;border:none;padding:3px 0}
.task-toggle:hover{color:var(--accent-d)}
.task-toggle svg{transition:transform .2s ease}
.task-toggle.open svg{transform:rotate(90deg)}
.task-detail{max-height:0;overflow:hidden;transition:max-height .3s ease}
.task-detail.open{max-height:2000px}

.scope-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.scope-in{border-left:3px solid var(--done)}
.scope-out{border-left:3px solid var(--risk)}
.scope-label{font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}
.scope-label.in{color:var(--done)}.scope-label.out{color:var(--risk)}

@media(max-width:860px){
  .sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}
  .main{margin-left:0}.content{padding:24px 20px 60px}.topbar{padding:12px 20px}
  .stats{grid-template-columns:repeat(2,1fr)}.scope-grid{grid-template-columns:1fr}
}
@media print{.sidebar,.topbar,.task-toggle{display:none!important}.main{margin-left:0}.card{break-inside:avoid;box-shadow:none}.task-detail{max-height:none!important}html{font-size:12px}}
"""

_JS_FALLBACK = r"""
function setActive(el){document.querySelectorAll('.sidebar-nav a').forEach(a=>a.classList.remove('active'));el.classList.add('active');if(window.innerWidth<=860)document.getElementById('sidebar').classList.remove('open')}
function toggleDetail(btn){btn.classList.toggle('open');btn.closest('.card').querySelector('.task-detail').classList.toggle('open')}
const secs=document.querySelectorAll('[id]');const links=document.querySelectorAll('.sidebar-nav a[href^="#"]');
const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){const id=e.target.getAttribute('id');links.forEach(l=>{l.classList.toggle('active',l.getAttribute('href')==='#'+id)})}})},{rootMargin:'-80px 0px -60% 0px',threshold:0});
secs.forEach(s=>obs.observe(s));
const backTop=document.getElementById('backTop');
window.addEventListener('scroll',()=>{backTop.classList.toggle('show',window.scrollY>400)},{passive:true});
"""


def _get_css():
    return load_template_asset("feature-overview.css", _CSS_FALLBACK)


def _get_js():
    return load_template_asset("feature-overview.js", _JS_FALLBACK)


def _get_index_css():
    return load_template_asset("index.css", _INDEX_CSS_FALLBACK)

SVG = {
    "doc": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    "users": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "layers": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "check": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    "warn": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "info": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "chev": '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>',
    "grid": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "tick": '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
}


def generate(feature_dir: Path) -> str:
    css_content = _get_css()
    js_content = _get_js()
    proposal_path = feature_dir / "proposal.md"
    stories_path = feature_dir / "stories.md"
    arch_path = feature_dir / "architecture.md"
    tasks_path = feature_dir / "tasks.md"

    proposal_meta, proposal_body = {}, ""
    if proposal_path.exists():
        proposal_meta, proposal_body = parse_frontmatter(proposal_path.read_text(encoding="utf-8"))

    stories_meta, stories_body = {}, ""
    if stories_path.exists():
        stories_meta, stories_body = parse_frontmatter(stories_path.read_text(encoding="utf-8"))

    arch_meta, arch_body = {}, ""
    if arch_path.exists():
        arch_meta, arch_body = parse_frontmatter(arch_path.read_text(encoding="utf-8"))

    arch_needed_raw = str(stories_meta.get("architecture_needed", "")).strip().lower()
    has_arch = arch_path.exists()
    arch_skipped = arch_needed_raw in {"false", "no", "0"} and not has_arch
    arch_reason = str(stories_meta.get("architecture_reason", "") or "")

    tasks_meta, tasks_body = {}, ""
    if tasks_path.exists():
        _, tasks_body = parse_frontmatter(tasks_path.read_text(encoding="utf-8"))

    fid = proposal_meta.get("id", arch_meta.get("id", "FEAT-XXX"))
    ftitle = proposal_meta.get("title", arch_meta.get("title", "Feature"))
    ftype = proposal_meta.get("type", "feature")
    fpriority = proposal_meta.get("priority", "P1")
    fdepends = proposal_meta.get("depends_on", [])
    fstatus = proposal_meta.get("status", arch_meta.get("status", "draft"))

    stories = parse_stories(stories_body)
    tasks, phases = parse_tasks(tasks_body)

    proposal_sections = extract_sections(proposal_body)
    arch_sections = extract_sections(arch_body)

    done_tasks = sum(1 for t in tasks if str(t["meta"].get("status", "")).lower() == "done")
    total_tasks = len(tasks)

    sidebar_items = []
    sidebar_items.append(f'<div class="nav-grp"><div class="nav-grp-title">概览</div>')
    sidebar_items.append(f'<a href="#overview" class="active" onclick="setActive(this)">{SVG["grid"]} Feature 总览</a></div>')

    sidebar_items.append(f'<div class="nav-grp"><div class="nav-grp-title">需求设计</div>')
    sidebar_items.append(f'<a href="#proposal" onclick="setActive(this)"><span class="dot p"></span>提案概述</a>')
    for sec in proposal_sections:
        if sec["level"] == 2 and sec["title"] not in ("提案", "Proposal"):
            anchor = f"prop-{sec['title'][:8]}"
            sidebar_items.append(f'<a href="#{anchor}" onclick="setActive(this)"><span class="dot p"></span>{sec["title"]}</a>')
    sidebar_items.append("</div>")

    sidebar_items.append(f'<div class="nav-grp"><div class="nav-grp-title">Story 设计</div>')
    sidebar_items.append(f'<a href="#stories" onclick="setActive(this)"><span class="dot s"></span>故事索引</a>')
    for st in stories:
        sidebar_items.append(f'<a href="#{st["id"].lower()}" onclick="setActive(this)"><span class="dot s"></span>{st["id"]} {st["title"][:12]}</a>')
    sidebar_items.append("</div>")

    if has_arch or arch_skipped:
        sidebar_items.append(f'<div class="nav-grp"><div class="nav-grp-title">架构设计</div>')
        if has_arch:
            sidebar_items.append(f'<a href="#architecture" onclick="setActive(this)"><span class="dot a"></span>架构概述</a>')
            for sec in arch_sections:
                if sec["level"] == 2:
                    anchor = f"arch-{sec['title'][:8]}"
                    sidebar_items.append(f'<a href="#{anchor}" onclick="setActive(this)"><span class="dot a"></span>{sec["title"]}</a>')
        else:
            sidebar_items.append(f'<a href="#architecture" onclick="setActive(this)"><span class="dot a"></span>已跳过</a>')
        sidebar_items.append("</div>")

    sidebar_items.append(f'<div class="nav-grp"><div class="nav-grp-title">任务清单</div>')
    sidebar_items.append(f'<a href="#tasks" onclick="setActive(this)"><span class="dot t"></span>任务索引</a>')
    for ph in phases:
        sidebar_items.append(f'<a href="#phase-{ph["id"].lower()}" onclick="setActive(this)"><span class="dot t"></span>{ph["id"]} {ph["title"]}</a>')
    sidebar_items.append("</div>")

    sidebar_html = "\n".join(sidebar_items)

    body = []

    body.append(f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html.escape(fid)} · {html.escape(ftitle)}</title>
<style>{css_content}</style></head><body>""")

    body.append(f"""<aside class="sidebar" id="sidebar">
<div class="sidebar-hd"><div class="logo">Quick SDD</div><div class="fid">{html.escape(fid)}</div></div>
<nav class="sidebar-nav">{sidebar_html}</nav>
<div class="sidebar-ft">Generated by Quick SDD</div>
</aside>""")

    body.append('<div class="main">')

    body.append(f"""<header class="topbar">
<button class="menu-btn" onclick="document.getElementById('sidebar').classList.toggle('open')" style="display:none;background:none;border:none;cursor:pointer;padding:8px">{SVG["menu"]}</button>
<a class="back-btn" href="../../index.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>所有特性</a>
<div class="bc">codespec / specs / <strong>{html.escape(fid)}</strong></div>
<span class="pill {status_class(fstatus)}">{SVG["tick"]} {html.escape(str(fstatus).capitalize())}</span>
</header>
<button class="back-top" id="backTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="回到顶部"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="18 15 12 9 6 15"/></svg></button>""")

    body.append('<div class="content">')

    dep_text = "无依赖" if not fdepends else ", ".join(str(d) for d in fdepends)
    pclass = priority_class(str(fpriority))
    body.append(f"""<section class="hero" id="overview">
<h1>{html.escape(ftitle)}</h1>
<div class="hero-meta">
<span class="badge type">{html.escape(str(ftype))}</span>
<span class="badge {pclass}">{html.escape(str(fpriority))}</span>
<span class="badge">{html.escape(fid)}</span>
<span class="badge">{html.escape(dep_text)}</span>
</div>
</section>""")

    body.append(f"""<div class="stats">
<div class="stat s1"><div class="n">1</div><div class="l">提案</div></div>
<div class="stat s2"><div class="n">{len(stories)}</div><div class="l">用户故事</div></div>
<div class="stat s3"><div class="n">{"跳过" if arch_skipped else (len(arch_sections) if has_arch else "—")}</div><div class="l">架构章节</div></div>
<div class="stat s4"><div class="n">{done_tasks}/{total_tasks}</div><div class="l">任务完成</div></div>
</div>""")

    # ── PROPOSAL ──
    body.append(f"""<section class="section" id="proposal">
<div class="sec-hd"><div class="sec-ico p">{SVG["doc"]}</div><h2>需求设计 · Proposal</h2></div>""")

    for sec in proposal_sections:
        if not sec["title"]:
            continue
        body_text = "\n".join(sec["lines"]).strip()
        if not body_text and not sec["title"]:
            continue
        anchor = f"prop-{sec['title'][:8]}"

        if sec["level"] == 2:
            body.append(f'<div class="subsec" id="{anchor}"><h3>{html.escape(sec["title"])}</h3>')

            if sec["title"] in ("范围内", "In-scope", "范围"):
                sub_sections = extract_sections(body_text)
                in_scope = ""
                out_scope = ""
                for ss in sub_sections:
                    if "内" in ss["title"] or "In" in ss["title"]:
                        in_scope = "\n".join(ss["lines"])
                    elif "外" in ss["title"] or "Out" in ss["title"] or "非目标" in ss["title"]:
                        out_scope = "\n".join(ss["lines"])
                if in_scope or out_scope:
                    body.append('<div class="scope-grid">')
                    if in_scope:
                        body.append(f'<div class="card scope-in"><div class="scope-label in">范围内</div><div class="prose">{md_to_html(in_scope)}</div></div>')
                    if out_scope:
                        body.append(f'<div class="card scope-out"><div class="scope-label out">范围外</div><div class="prose">{md_to_html(out_scope)}</div></div>')
                    body.append("</div>")
                else:
                    body.append(f'<div class="card"><div class="prose">{md_to_html(body_text)}</div></div>')
            elif sec["title"] in ("风险", "Risks", "风险与待确认问题"):
                body.append(f'<div class="card"><div class="prose">{md_to_html(body_text)}</div></div>')
            else:
                body.append(f'<div class="card"><div class="prose">{md_to_html(body_text)}</div></div>')

            sub_secs = extract_sections(body_text)
            for ss in sub_secs:
                if ss["level"] == 3 and ss["title"]:
                    ss_body = "\n".join(ss["lines"]).strip()
                    if ss["title"] in ("范围内", "In-scope"):
                        continue
                    if ss["title"] in ("范围外", "Out-of-scope", "非目标"):
                        continue
                    body.append(f'<h4>{html.escape(ss["title"])}</h4>')
                    body.append(f'<div class="card"><div class="prose">{md_to_html(ss_body)}</div></div>')

            body.append("</div>")

        elif sec["level"] == 1:
            body.append(f'<div class="subsec"><h3>{html.escape(sec["title"])}</h3>')
            body.append(f'<div class="card"><div class="prose">{md_to_html(body_text)}</div></div>')
            body.append("</div>")

    body.append("</section>")

    # ── STORIES ──
    body.append(f"""<section class="section" id="stories">
<div class="sec-hd"><div class="sec-ico s">{SVG["users"]}</div><h2>Story 设计 · User Stories</h2><span class="sec-cnt">{len(stories)} stories</span></div>""")

    if stories:
        body.append('<div class="table-wrap"><table><thead><tr><th>ID</th><th>标题</th><th>优先级</th><th>状态</th><th>依赖</th></tr></thead><tbody>')
        for st in stories:
            m = st["meta"]
            sid = st["id"]
            dep = m.get("depends_on", [])
            dep_str = "—" if not dep else " ".join(f'<span class="dep">{d}</span>' for d in dep)
            st_status = m.get("status", "ready")
            body.append(f'<tr><td><strong>{sid}</strong></td><td><a href="#{sid.lower()}" style="color:var(--text);text-decoration:none">{html.escape(st["title"])}</a></td><td>{html.escape(str(m.get("priority","P1")))}</td><td><span class="cst {status_class(st_status)}">{html.escape(str(st_status))}</span></td><td>{dep_str}</td></tr>')
        body.append("</tbody></table></div>")

    for st in stories:
        m = st["meta"]
        sid = st["id"]
        dep = m.get("depends_on", [])
        dep_html = " ".join(f'<span class="dep">{d}</span>' for d in dep) if dep else ""
        st_status = m.get("status", "ready")

        body.append(f'<div class="card" id="{sid.lower()}">')
        body.append(f'<div class="card-hd"><span class="cid s">{sid}</span><span class="ctitle">{html.escape(st["title"])}</span><span class="cst {status_class(st_status)}">{html.escape(str(st_status))}</span>{dep_html}</div>')

        if st["narrative"]:
            body.append(f'<div class="prose">{md_to_html(st["narrative"])}</div>')
        else:
            for sec in st["content"]:
                if "故事" in sec["title"] or "Story" in sec["title"]:
                    sec_body = "\n".join(sec["lines"]).strip()
                    body.append(f'<div class="prose">{md_to_html(sec_body)}</div>')

        if st["ac"]:
            body.append('<h4 style="font-size:.88rem;font-weight:600;margin:10px 0 4px;color:var(--text-sec)">验收标准</h4>')
            body.append('<ul class="ac-list">')
            for ac in st["ac"]:
                body.append(f'<li class="ac-item"><span class="ac-id">{ac["id"]}</span><span class="ac-text">{html.escape(ac["text"])}</span></li>')
            body.append("</ul>")

        for sec in st["content"]:
            if "验收" in sec["title"]:
                continue
            if "故事" in sec["title"] or "Story" in sec["title"]:
                continue
            if "范围外" in sec["title"]:
                continue
            sec_body = "\n".join(sec["lines"]).strip()
            if sec_body:
                body.append(f'<h4 style="font-size:.88rem;font-weight:600;margin:10px 0 4px;color:var(--text-sec)">{html.escape(sec["title"])}</h4>')
                body.append(f'<div class="prose">{md_to_html(sec_body)}</div>')

        body.append("</div>")

    body.append("</section>")

    # ── ARCHITECTURE ──
    if has_arch:
        body.append(f"""<section class="section" id="architecture">
<div class="sec-hd"><div class="sec-ico a">{SVG["layers"]}</div><h2>架构设计 · Architecture</h2></div>""")

        for sec in arch_sections:
            if not sec["title"]:
                continue
            body_text = "\n".join(sec["lines"]).strip()
            anchor = f"arch-{sec['title'][:8]}"

            if sec["level"] == 1:
                body.append(f'<div class="subsec"><h3>{html.escape(sec["title"])}</h3>')
                body.append(f'<div class="card"><div class="prose">{md_to_html(body_text)}</div></div>')
                sub_secs = extract_sections(body_text)
                for ss in sub_secs:
                    if ss["level"] <= 3 and ss["title"]:
                        ss_body = "\n".join(ss["lines"]).strip()
                        if ss_body:
                            body.append(f'<h4>{html.escape(ss["title"])}</h4>')
                            body.append(f'<div class="card"><div class="prose">{md_to_html(ss_body)}</div></div>')
                body.append("</div>")

            elif sec["level"] == 2:
                body.append(f'<div class="subsec" id="{anchor}"><h3>{html.escape(sec["title"])}</h3>')
                body.append(f'<div class="card"><div class="prose">{md_to_html(body_text)}</div></div>')
                sub_secs = extract_sections(body_text)
                for ss in sub_secs:
                    if ss["level"] == 3 and ss["title"]:
                        ss_body = "\n".join(ss["lines"]).strip()
                        if ss_body:
                            body.append(f'<h4>{html.escape(ss["title"])}</h4>')
                            body.append(f'<div class="card"><div class="prose">{md_to_html(ss_body)}</div></div>')
                body.append("</div>")

        body.append("</section>")
    elif arch_skipped:
        skip_reason = f"：{html.escape(arch_reason)}" if arch_reason else ""
        body.append(f"""<section class="section" id="architecture">
<div class="sec-hd"><div class="sec-ico a">{SVG["layers"]}</div><h2>架构设计 · Architecture</h2><span class="sec-cnt">已跳过</span></div>
<div class="card"><div class="prose"><p>本 feature 经 TA 评估跳过架构设计文档{skip_reason}。QA 会审计跳过理由是否站得住。</p></div></div>
</section>""")

    # ── TASKS ──
    body.append(f"""<section class="section" id="tasks">
<div class="sec-hd"><div class="sec-ico t">{SVG["check"]}</div><h2>任务清单 · Tasks</h2><span class="sec-cnt">{total_tasks} tasks · {done_tasks} done</span></div>""")

    if tasks:
        body.append('<div class="table-wrap"><table><thead><tr><th>ID</th><th>Story</th><th>标题</th><th>状态</th><th>依赖</th><th>负责</th></tr></thead><tbody>')
        for t in tasks:
            m = t["meta"]
            tid = t["id"]
            dep = m.get("depends_on", [])
            dep_str = "—" if not dep else " ".join(f'<span class="dep">{d}</span>' for d in dep)
            t_status = m.get("status", "todo")
            owner = m.get("owner_role", "dev")
            story = m.get("story_id", "")
            body.append(f'<tr><td><strong>{tid}</strong></td><td>{html.escape(str(story))}</td><td>{html.escape(t["title"])}</td><td><span class="cst {status_class(t_status)}">{html.escape(str(t_status))}</span></td><td>{dep_str}</td><td>{html.escape(str(owner))}</td></tr>')
        body.append("</tbody></table></div>")

    for ph in phases:
        body.append(f'<div class="subsec" id="phase-{ph["id"].lower()}"><h3>阶段 {ph["id"]} · {html.escape(ph["title"])}</h3>')
        ph_tasks = [t for t in tasks if t.get("phase") == ph["id"]]
        for t in ph_tasks:
            m = t["meta"]
            tid = t["id"]
            t_status = m.get("status", "todo")
            body.append(f'<div class="card">')
            body.append(f'<div class="card-hd"><span class="cid t">{tid}</span><span class="ctitle">{html.escape(t["title"])}</span><span class="cst {status_class(t_status)}">{html.escape(str(t_status))}</span>')
            body.append(f'<button class="task-toggle" onclick="toggleDetail(this)">{SVG["chev"]} 详情</button></div>')
            body.append('<div class="task-detail"><div class="prose">')
            if t["goal"]:
                body.append("<h4>目标</h4><ul>")
                for g in t["goal"]:
                    body.append(f"<li>{inline_md(g)}</li>")
                body.append("</ul>")
            if t["deliverables"]:
                body.append("<h4>交付物</h4><ul>")
                for d in t["deliverables"]:
                    body.append(f"<li>{inline_md(d)}</li>")
                body.append("</ul>")
            if t["notes"]:
                body.append("<h4>备注</h4><ul>")
                for n in t["notes"]:
                    body.append(f"<li>{inline_md(n)}</li>")
                body.append("</ul>")
            body.append("</div></div></div>")
        body.append("</div>")

    body.append("</section>")

    body.append("</div></div>")

    body.append(f"<script>{js_content}</script>")
    body.append('<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>')
    body.append('<script>mermaid.initialize({startOnLoad:true,theme:"neutral",securityLevel:"loose"});</script>')

    style_mobile = "<style>@media(max-width:860px){.menu-btn{display:block!important}}</style>"
    body.append(style_mobile)

    body.append("</body></html>")

    return "\n".join(body)


_INDEX_CSS_FALLBACK = r"""
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f7f8fb;--surface:#fff;--border:#dfe4ec;--text:#20242c;--muted:#667085;
  --accent:#3158d4;--accent-bg:#eef2ff;--done:#15803d;--draft:#64748b;--shadow:0 1px 3px rgba(16,24,40,.08);
  --radius:8px;--radius-lg:12px
}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans SC","Microsoft YaHei",sans-serif;line-height:1.6}
header{padding:24px 40px 18px;border-bottom:1px solid var(--border);background:var(--surface)}
main{max-width:1120px;margin:0 auto;padding:24px 32px 64px}
h1{margin:0 0 4px;font-size:1.5rem;letter-spacing:0}
.meta{color:var(--muted);font-size:.88rem}

.controls{display:flex;gap:10px;align-items:center;margin:20px 0 16px;flex-wrap:wrap}
.search-box{position:relative;flex:1;min-width:200px;max-width:360px}
.search-box input{width:100%;padding:8px 12px 8px 34px;border:1px solid var(--border);border-radius:var(--radius);font-size:.88rem;background:var(--surface);color:var(--text);outline:none;transition:border-color .15s}
.search-box input:focus{border-color:var(--accent)}
.search-box svg{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--muted);pointer-events:none}
.filter-group{display:flex;gap:4px;flex-wrap:wrap}
.filter-btn{padding:5px 12px;border:1px solid var(--border);border-radius:999px;background:var(--surface);font-size:.78rem;color:var(--muted);cursor:pointer;transition:all .15s;white-space:nowrap}
.filter-btn:hover{border-color:#b8c3d8;color:var(--text)}
.filter-btn.active{background:var(--accent-bg);border-color:var(--accent);color:var(--accent);font-weight:600}
.sort-select{padding:5px 10px;border:1px solid var(--border);border-radius:var(--radius);font-size:.82rem;background:var(--surface);color:var(--text);cursor:pointer;outline:none}
.result-info{font-size:.82rem;color:var(--muted);margin-bottom:14px}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.card{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow);min-height:156px;transition:border-color .15s,box-shadow .15s}
.card:hover{border-color:#b8c3d8;box-shadow:0 2px 8px rgba(16,24,40,.1)}
.card-head{display:flex;gap:8px;align-items:center;margin-bottom:8px}
.id{font-family:"SF Mono",Consolas,monospace;font-weight:700;color:var(--accent);background:var(--accent-bg);border-radius:6px;padding:2px 8px;font-size:.78rem}
.status{margin-left:auto;border-radius:999px;padding:2px 9px;font-size:.74rem;background:#f1f5f9;color:var(--draft)}
.status.done,.status.accepted,.status.pass{background:#ecfdf5;color:var(--done)}
.status.ready,.status.validating,.status.draft{background:#fffbeb;color:#b45309}
.title{font-size:1rem;font-weight:700;margin-bottom:6px}
.desc{font-size:.86rem;color:var(--muted);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;flex:1}
.foot{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.tag{font-size:.74rem;color:var(--muted);border:1px solid var(--border);border-radius:6px;padding:1px 7px}

.pagination{display:flex;justify-content:center;align-items:center;gap:6px;margin-top:28px;flex-wrap:wrap}
.page-btn{width:34px;height:34px;display:flex;align-items:center;justify-content:center;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);font-size:.84rem;color:var(--text);cursor:pointer;transition:all .15s}
.page-btn:hover{border-color:var(--accent);color:var(--accent)}
.page-btn.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.page-btn:disabled{opacity:.4;cursor:default;pointer-events:none}
.page-ellipsis{padding:0 4px;color:var(--muted);font-size:.84rem}
.empty-state{text-align:center;padding:60px 20px;color:var(--muted)}
.empty-state svg{margin-bottom:12px;opacity:.4}
.empty-state p{font-size:.95rem}

@media(max-width:640px){
  header{padding:20px 20px 16px}
  main{padding:20px 16px 48px}
  .controls{gap:8px}
  .search-box{max-width:none;min-width:0}
  .grid{grid-template-columns:1fr}
}
"""


def generate_index(repo_root, feature_dirs=None, output_path=None):
    index_css = _get_index_css()
    repo_root = Path(repo_root)
    feature_dirs = feature_dirs if feature_dirs is not None else discover_feature_dirs(repo_root)
    output_path = Path(output_path) if output_path else repo_root / "codespec" / "index.html"
    summaries = [load_feature_summary(path) for path in feature_dirs]
    generated_at = now_iso()
    rel_prefix = "" if output_path.parent == repo_root / "codespec" else "codespec/"

    features_json = json.dumps(
        [
            {
                "id": item["id"],
                "title": item["title"],
                "status": item["status"],
                "type": item["type"],
                "priority": item["priority"],
                "description": item["description"] or item["dir_name"],
                "href": f"{rel_prefix}specs/{item['dir_name']}/overview.html",
            }
            for item in summaries
        ],
        ensure_ascii=False,
    )

    content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quick SDD Specs</title>
<style>{index_css}</style>
</head>
<body>
<header>
  <h1>Quick SDD Specs</h1>
  <div class="meta">项目规格站点入口 · {html.escape(repo_root.name)} · Generated {html.escape(generated_at)}</div>
</header>
<main>
  <div class="controls">
    <div class="search-box">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="text" id="searchInput" placeholder="搜索特性名称、ID 或描述..." autocomplete="off">
    </div>
    <div class="filter-group" id="statusFilter">
      <button class="filter-btn active" data-status="all">全部</button>
      <button class="filter-btn" data-status="done">已完成</button>
      <button class="filter-btn" data-status="ready">进行中</button>
      <button class="filter-btn" data-status="draft">草稿</button>
    </div>
    <select class="sort-select" id="sortSelect">
      <option value="id-asc">ID 升序</option>
      <option value="id-desc">ID 降序</option>
      <option value="priority">优先级</option>
      <option value="status">状态</option>
      <option value="title">名称</option>
    </select>
  </div>
  <div class="result-info" id="resultInfo"></div>
  <section class="grid" id="grid"></section>
  <div class="pagination" id="pagination"></div>
</main>
<script>
const FEATURES={features_json};
const PER_PAGE=24;
let currentPage=1;
let filtered=[...FEATURES];

function escHtml(s){{const d=document.createElement('div');d.textContent=s;return d.innerHTML}}

function statusClass(s){{
  const v=s.toLowerCase();
  if(['done','accepted','pass'].includes(v))return 'done';
  if(['ready','validating','draft'].includes(v))return 'ready';
  return '';
}}

function priorityOrder(p){{
  const m={{'P0':0,'P1':1,'P2':2,'P3':3,'P4':4}};
  return m[p]??99;
}}

function applyFilters(){{
  const q=document.getElementById('searchInput').value.toLowerCase().trim();
  const statusBtn=document.querySelector('#statusFilter .filter-btn.active');
  const status=statusBtn?statusBtn.dataset.status:'all';
  const sort=document.getElementById('sortSelect').value;

  filtered=FEATURES.filter(f=>{{
    if(status!=='all'){{
      const sc=statusClass(f.status);
      if(status==='done'&&sc!=='done')return false;
      if(status==='ready'&&sc!=='ready')return false;
      if(status==='draft'&&sc!=='')return false;
    }}
    if(q){{
      const hay=(f.id+' '+f.title+' '+f.description+' '+f.type+' '+f.priority).toLowerCase();
      if(!hay.includes(q))return false;
    }}
    return true;
  }});

  if(sort==='id-asc')filtered.sort((a,b)=>a.id.localeCompare(b.id,undefined,{{numeric:true}}));
  else if(sort==='id-desc')filtered.sort((a,b)=>b.id.localeCompare(a.id,undefined,{{numeric:true}}));
  else if(sort==='priority')filtered.sort((a,b)=>priorityOrder(a.priority)-priorityOrder(b.priority));
  else if(sort==='status')filtered.sort((a,b)=>statusClass(a.status).localeCompare(statusClass(b.status)));
  else if(sort==='title')filtered.sort((a,b)=>a.title.localeCompare(b.title,'zh'));

  currentPage=1;
  render();
}}

function render(){{
  const grid=document.getElementById('grid');
  const info=document.getElementById('resultInfo');
  const pag=document.getElementById('pagination');
  const total=filtered.length;
  const totalPages=Math.max(1,Math.ceil(total/PER_PAGE));
  if(currentPage>totalPages)currentPage=totalPages;
  const start=(currentPage-1)*PER_PAGE;
  const pageItems=filtered.slice(start,start+PER_PAGE);

  info.textContent=total===FEATURES.length
    ?`共 ${{total}} 个特性`
    :`显示 ${{total}} / ${{FEATURES.length}} 个特性`;

  if(total===0){{
    grid.innerHTML='<div class="empty-state"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><p>没有找到匹配的特性</p></div>';
    pag.innerHTML='';
    return;
  }}

  grid.innerHTML=pageItems.map(f=>`<a class="card" href="${{escHtml(f.href)}}">
<div class="card-head"><span class="id">${{escHtml(f.id)}}</span><span class="status ${{statusClass(f.status)}}">${{escHtml(f.status)}}</span></div>
<div class="title">${{escHtml(f.title)}}</div>
<div class="desc">${{escHtml(f.description)}}</div>
<div class="foot"><span class="tag">${{escHtml(f.type)}}</span><span class="tag">${{escHtml(f.priority)}}</span></div>
</a>`).join('');

  if(totalPages<=1){{pag.innerHTML='';return;}}

  let btns=[];
  btns.push(`<button class="page-btn" ${{currentPage===1?'disabled':''}} onclick="goPage(${{currentPage-1}})">‹</button>`);

  const range=[];
  if(totalPages<=7){{for(let i=1;i<=totalPages;i++)range.push(i);}}
  else{{
    range.push(1);
    if(currentPage>3)range.push('...');
    for(let i=Math.max(2,currentPage-1);i<=Math.min(totalPages-1,currentPage+1);i++)range.push(i);
    if(currentPage<totalPages-2)range.push('...');
    range.push(totalPages);
  }}
  for(const p of range){{
    if(p==='...')btns.push('<span class="page-ellipsis">…</span>');
    else btns.push(`<button class="page-btn ${{p===currentPage?'active':''}}" onclick="goPage(${{p}})">${{p}}</button>`);
  }}
  btns.push(`<button class="page-btn" ${{currentPage===totalPages?'disabled':''}} onclick="goPage(${{currentPage+1}})">›</button>`);
  pag.innerHTML=btns.join('');
}}

function goPage(p){{currentPage=p;render();window.scrollTo({{top:0,behavior:'smooth'}});}}

document.getElementById('searchInput').addEventListener('input',applyFilters);
document.getElementById('sortSelect').addEventListener('change',applyFilters);
document.getElementById('statusFilter').addEventListener('click',e=>{{
  const btn=e.target.closest('.filter-btn');
  if(!btn)return;
  document.querySelectorAll('#statusFilter .filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  applyFilters();
}});

applyFilters();
</script>
</body>
</html>
"""
    write_text(output_path, content)
    return output_path


def generate_feature_overview(feature_dir):
    feature_dir = Path(feature_dir)
    html_content = generate(feature_dir)
    output_path = feature_dir / "overview.html"
    write_text(output_path, html_content)
    return output_path


def generate_site(repo_root, feature_dirs=None, include_index=True, respect_agents_config=False):
    repo_root = Path(repo_root)
    if respect_agents_config and not html_export_enabled(repo_root):
        return {
            "status": "SKIPPED",
            "reason": "html_export_disabled",
            "repo_root": str(repo_root),
            "generated": [],
        }
    resolved_feature_dirs = list(feature_dirs) if feature_dirs is not None else discover_feature_dirs(repo_root)
    generated = []
    for feature_dir in resolved_feature_dirs:
        generated.append(str(generate_feature_overview(feature_dir)))
    if include_index:
        generated.append(str(generate_index(repo_root)))
    return {
        "status": "DONE",
        "repo_root": str(repo_root),
        "generated": generated,
    }


def build_parser():
    parser = argparse.ArgumentParser(description="Generate Quick SDD HTML overviews.")
    parser.add_argument("feature_dir", nargs="?", help="Legacy mode: generate one feature overview.")
    parser.add_argument("--repo-root", help="Repository root. Enables site/index generation mode.")
    parser.add_argument("--all", action="store_true", help="Generate HTML for all existing feature specs.")
    parser.add_argument(
        "--feature",
        action="append",
        default=[],
        help="Feature directory name, feature id prefix, or path. Can be repeated.",
    )
    parser.add_argument("--index-only", action="store_true", help="Only generate codespec/index.html.")
    parser.add_argument("--skip-index", action="store_true", help="Do not generate codespec/index.html.")
    parser.add_argument(
        "--respect-agents-config",
        action="store_true",
        help="Skip generation when AGENTS.md disables automatic HTML export.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.feature_dir and not args.repo_root:
        feature_dir = Path(args.feature_dir)
        if not feature_dir.is_dir():
            print(f"Error: {feature_dir} is not a directory")
            return 1
        output_path = generate_feature_overview(feature_dir)
        print(f"Generated: {output_path}")
        return 0

    if not args.repo_root:
        parser.error("Either provide <feature_dir> or --repo-root.")

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        print(f"Error: {repo_root} is not a directory")
        return 1

    try:
        if args.index_only:
            output_path = generate_index(repo_root)
            payload = {"status": "DONE", "repo_root": str(repo_root), "generated": [str(output_path)]}
        else:
            if args.feature:
                feature_dirs = [resolve_feature_dir(repo_root, selector) for selector in args.feature]
            elif args.all or not args.feature_dir:
                feature_dirs = discover_feature_dirs(repo_root)
            else:
                feature_dirs = [resolve_feature_dir(repo_root, args.feature_dir)]
            payload = generate_site(
                repo_root=repo_root,
                feature_dirs=feature_dirs,
                include_index=not args.skip_index,
                respect_agents_config=args.respect_agents_config,
            )
    except ValueError as exc:
        payload = {"status": "BLOCKED", "reason": "invalid_feature", "details": str(exc)}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"Error: {exc}")
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for path in payload.get("generated", []):
            print(f"Generated: {path}")
        if payload.get("status") == "SKIPPED":
            print(f"Skipped: {payload.get('reason')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
