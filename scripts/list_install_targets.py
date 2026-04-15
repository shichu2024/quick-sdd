#!/usr/bin/env python3
"""List installable Quick SDD skills and render repo-path install commands."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid manifest: {exc}") from exc


def build_skill_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    skills = manifest.get("skills", [])
    if not isinstance(skills, list):
        raise SystemExit("invalid manifest: skills must be a list")
    skill_map: dict[str, dict[str, Any]] = {}
    for item in skills:
        if not isinstance(item, dict):
            raise SystemExit("invalid manifest: skill item must be an object")
        name = str(item.get("name", "")).strip()
        path = str(item.get("path", "")).strip()
        if not name or not path:
            raise SystemExit("invalid manifest: skill item missing name/path")
        skill_map[name] = item
    return skill_map


def build_bundle_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    bundles = manifest.get("bundles", [])
    if not isinstance(bundles, list):
        raise SystemExit("invalid manifest: bundles must be a list")
    bundle_map: dict[str, dict[str, Any]] = {}
    for item in bundles:
        if not isinstance(item, dict):
            raise SystemExit("invalid manifest: bundle item must be an object")
        name = str(item.get("name", "")).strip()
        if not name:
            raise SystemExit("invalid manifest: bundle item missing name")
        bundle_map[name] = item
    return bundle_map


def ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def resolve_skill_dependencies(name: str, skill_map: dict[str, dict[str, Any]]) -> list[str]:
    if name not in skill_map:
        raise SystemExit(f"unknown skill: {name}")
    resolved: list[str] = []
    visiting: set[str] = set()

    def visit(skill_name: str) -> None:
        if skill_name in resolved:
            return
        if skill_name in visiting:
            raise SystemExit(f"cyclic dependency detected: {skill_name}")
        if skill_name not in skill_map:
            raise SystemExit(f"missing dependency target: {skill_name}")
        visiting.add(skill_name)
        depends_on = skill_map[skill_name].get("depends_on", []) or []
        if not isinstance(depends_on, list):
            raise SystemExit(f"invalid depends_on for skill: {skill_name}")
        for dep in depends_on:
            visit(str(dep))
        visiting.remove(skill_name)
        resolved.append(skill_name)

    visit(name)
    return resolved


def resolve_bundle(name: str, bundle_map: dict[str, dict[str, Any]], skill_map: dict[str, dict[str, Any]]) -> list[str]:
    if name not in bundle_map:
        raise SystemExit(f"unknown bundle: {name}")
    bundle = bundle_map[name]
    skills = bundle.get("skills", []) or []
    if not isinstance(skills, list):
        raise SystemExit(f"invalid bundle skills for: {name}")
    expanded: list[str] = []
    for skill_name in skills:
        expanded.extend(resolve_skill_dependencies(str(skill_name), skill_map))
    return ordered_unique(expanded)


def repo_paths_for(skills: list[str], skill_map: dict[str, dict[str, Any]]) -> list[str]:
    return [str(skill_map[skill]["path"]) for skill in skills]


def render_command(repo: str, ref: str, paths: list[str]) -> str:
    parts = [
        "python <skill-installer-dir>/scripts/install-skill-from-github.py",
        f"--repo {repo}",
    ]
    if ref and ref != "main":
        parts.append(f"--ref {ref}")
    parts.extend(f"--path {path}" for path in paths)
    return " ".join(parts)


def verify_skill_paths(repo_root: Path, skill_map: dict[str, dict[str, Any]]) -> None:
    for skill in skill_map.values():
        skill_dir = repo_root / str(skill["path"])
        skill_md = skill_dir / "SKILL.md"
        if not skill_dir.is_dir():
            raise SystemExit(f"missing skill directory: {skill_dir}")
        if not skill_md.exists():
            raise SystemExit(f"missing SKILL.md: {skill_md}")


def build_payload(
    manifest: dict[str, Any],
    repo_root: Path,
    skill_name: str,
    bundle_name: str,
    repo: str,
    ref: str,
) -> dict[str, Any]:
    skill_map = build_skill_map(manifest)
    bundle_map = build_bundle_map(manifest)
    verify_skill_paths(repo_root, skill_map)

    selected_skills: list[str] = []
    selection_type = ""
    selection_name = ""
    if skill_name:
        selected_skills = resolve_skill_dependencies(skill_name, skill_map)
        selection_type = "skill"
        selection_name = skill_name
    elif bundle_name:
        selected_skills = resolve_bundle(bundle_name, bundle_map, skill_map)
        selection_type = "bundle"
        selection_name = bundle_name

    payload: dict[str, Any] = {
        "repository": manifest.get("repository", {}),
        "skills": list(skill_map.values()),
        "bundles": list(bundle_map.values()),
        "selection": {
            "type": selection_type,
            "name": selection_name,
            "skills": selected_skills,
            "paths": repo_paths_for(selected_skills, skill_map) if selected_skills else [],
        },
    }
    if repo and selected_skills:
        payload["selection"]["install_command"] = render_command(
            repo=repo,
            ref=ref,
            paths=payload["selection"]["paths"],
        )
    return payload


def render_text(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    repo_info = payload.get("repository", {}) or {}
    lines.append(f"Repository: {repo_info.get('name', 'unknown')}")
    lines.append("")
    lines.append("Installable skills:")
    for skill in payload.get("skills", []):
        suffix = "standalone" if skill.get("standalone") else "requires deps"
        depends_on = skill.get("depends_on", []) or []
        depends_text = f" -> depends on: {', '.join(depends_on)}" if depends_on else ""
        lines.append(f"- {skill.get('name')}: {suffix}{depends_text}")
    lines.append("")
    lines.append("Bundles:")
    for bundle in payload.get("bundles", []):
        lines.append(f"- {bundle.get('name')}: {', '.join(bundle.get('skills', []))}")

    selection = payload.get("selection", {}) or {}
    if selection.get("name"):
        lines.append("")
        lines.append(f"Selected {selection.get('type')}: {selection.get('name')}")
        lines.append(f"Resolved skills: {', '.join(selection.get('skills', []))}")
        lines.append(f"Repo paths: {', '.join(selection.get('paths', []))}")
        command = selection.get("install_command", "")
        if command:
            lines.append("Suggested command:")
            lines.append(command)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List installable Quick SDD skills and render repo-path install plans."
    )
    parser.add_argument(
        "--manifest",
        default="install/manifest.json",
        help="Path to the repository install manifest, relative to repo root.",
    )
    parser.add_argument(
        "--skill",
        default="",
        help="Resolve a single skill and its dependencies.",
    )
    parser.add_argument(
        "--bundle",
        default="",
        help="Resolve a bundle and its dependencies.",
    )
    parser.add_argument(
        "--repo",
        default="",
        help="GitHub repo slug such as owner/repo, used to render install commands.",
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Git ref used when rendering install commands.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.skill and args.bundle:
        raise SystemExit("choose either --skill or --bundle, not both")
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / args.manifest
    manifest = load_manifest(manifest_path)
    payload = build_payload(
        manifest=manifest,
        repo_root=repo_root,
        skill_name=args.skill,
        bundle_name=args.bundle,
        repo=args.repo,
        ref=args.ref,
    )
    if args.format == "json":
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render_text(payload) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
