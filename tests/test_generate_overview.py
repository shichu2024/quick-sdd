import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "quick-sdd" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import generate_overview  # noqa: E402


PROPOSAL = """---
id: FEAT-001
title: 示例规格
type: feature
priority: P1
status: draft
---

# 提案

## 目标

- 支持把规格文档生成 HTML。
"""

STORIES = """# 用户故事

## ST-001 浏览规格

```yaml
id: ST-001
title: 浏览规格
priority: P1
status: ready
depends_on: []
```

### 故事

作为维护者，我希望能在浏览器中阅读规格，以便更快理解 feature。

### 验收标准

- `AC-1`: Given 已有规格文档，when 生成 HTML，then 能打开 feature overview。
"""

ARCHITECTURE = """---
id: FEAT-001
title: 示例规格
owner_role: ta
status: draft
---

# 架构设计

## 关键决策

- 使用静态 HTML，避免引入运行时服务。
"""

TASKS = """# 任务清单

## 阶段 A 生成链路

## T-001 生成 HTML

```yaml
id: T-001
story_id: ST-001
title: 生成 HTML
owner_role: dev
status: done
depends_on: []
read_paths:
  - codespec/specs/FEAT-001-demo/**
write_paths:
  - codespec/specs/FEAT-001-demo/overview.html
verify:
  - type: command
    value: python skills/quick-sdd/scripts/generate_overview.py --repo-root . --all
```

### 目标

- 生成 feature overview。

### 交付物

- `overview.html`
"""


def write_feature(repo_root: Path, name: str = "FEAT-001-demo") -> Path:
    feature_dir = repo_root / "codespec" / "specs" / name
    feature_dir.mkdir(parents=True)
    (feature_dir / "proposal.md").write_text(PROPOSAL, encoding="utf-8")
    (feature_dir / "stories.md").write_text(STORIES, encoding="utf-8")
    (feature_dir / "architecture.md").write_text(ARCHITECTURE, encoding="utf-8")
    (feature_dir / "tasks.md").write_text(TASKS, encoding="utf-8")
    return feature_dir


def write_agents(repo_root: Path, enabled: bool) -> None:
    repo_root.joinpath("AGENTS.md").write_text(
        f"""# Agents

<!-- QUICK-SDD-HTML-START -->
```yaml
quick_sdd:
  html_export:
    enabled: {str(enabled).lower()}
```
<!-- QUICK-SDD-HTML-END -->
""",
        encoding="utf-8",
    )


class GenerateOverviewTests(unittest.TestCase):
    def test_auto_generation_respects_agents_disable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            feature_dir = write_feature(repo_root)
            write_agents(repo_root, enabled=False)

            result = generate_overview.generate_site(
                repo_root=repo_root,
                feature_dirs=[feature_dir],
                respect_agents_config=True,
            )

            self.assertEqual(result["status"], "SKIPPED")
            self.assertFalse((feature_dir / "overview.html").exists())
            self.assertFalse((repo_root / "codespec" / "index.html").exists())

    def test_manual_generation_converts_existing_specs_even_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            feature_dir = write_feature(repo_root)
            write_agents(repo_root, enabled=False)

            result = generate_overview.generate_site(
                repo_root=repo_root,
                feature_dirs=[feature_dir],
                respect_agents_config=False,
            )

            self.assertEqual(result["status"], "DONE")
            self.assertTrue((feature_dir / "overview.html").exists())
            self.assertTrue((repo_root / "codespec" / "index.html").exists())

    def test_cli_all_generates_site(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            write_feature(repo_root)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "generate_overview.py"),
                    "--repo-root",
                    str(repo_root),
                    "--all",
                    "--json",
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "DONE")
            self.assertTrue((repo_root / "codespec" / "index.html").exists())
            self.assertTrue((repo_root / "codespec" / "specs" / "FEAT-001-demo" / "overview.html").exists())

    def test_init_codespec_autogenerates_html_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "init_codespec.py"),
                    "--repo-root",
                    str(repo_root),
                    "--feature-title",
                    "HTML 规格站点",
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            payload = json.loads(completed.stdout)
            feature_dir = repo_root / "codespec" / "specs" / payload["feature_dir"]
            self.assertTrue((feature_dir / "overview.html").exists())
            self.assertTrue((repo_root / "codespec" / "index.html").exists())
            self.assertGreaterEqual(len(payload["html_generated"]), 2)

    def test_init_codespec_copies_git_submit_template_to_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "init_codespec.py"),
                    "--repo-root",
                    str(repo_root),
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            payload = json.loads(completed.stdout)
            git_submit_path = repo_root / "git-submit.md"
            template_path = (
                REPO_ROOT / "skills" / "quick-sdd" / "templates" / "git-submit.template.md"
            )
            self.assertTrue(git_submit_path.exists())
            self.assertEqual(git_submit_path.read_bytes(), template_path.read_bytes())
            self.assertIn(str(git_submit_path), payload["created"])


if __name__ == "__main__":
    unittest.main()
