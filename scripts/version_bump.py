#!/usr/bin/env python3
"""根级 Codex 插件版本递增检查。"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def git_ok(*args: str) -> str | None:
    try:
        return git(*args)
    except subprocess.CalledProcessError:
        return None


def resolve_base(explicit: str | None) -> str | None:
    for ref in (explicit, "origin/main", "main"):
        if ref and git_ok("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"):
            return ref
    return None


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def parse_semver(value: str) -> tuple[int, int, int] | None:
    parts = (value or "").split(".")
    if len(parts) != 3:
        return None
    try:
        return tuple(int(part) for part in parts)  # type: ignore[return-value]
    except ValueError:
        return None


def patch_bump(value: str) -> str:
    parsed = parse_semver(value)
    if parsed is None:
        return "0.0.1"
    return f"{parsed[0]}.{parsed[1]}.{parsed[2] + 1}"


def base_version(base: str) -> str | None:
    raw = git_ok("show", f"{base}:{rel(PLUGIN_JSON)}")
    if raw is None:
        return None
    try:
        return json.loads(raw).get("version")
    except json.JSONDecodeError:
        return None


def working_version() -> str | None:
    try:
        return json.loads(PLUGIN_JSON.read_text(encoding="utf-8")).get("version")
    except (OSError, json.JSONDecodeError):
        return None


def is_ahead(work: str | None, base: str | None) -> bool:
    if base is None:
        return True
    work_version = parse_semver(work or "")
    base_version_value = parse_semver(base)
    if work_version is None or base_version_value is None:
        return (work or "") != base
    return work_version > base_version_value


def changed_files(base: str, staged_only: bool) -> list[str]:
    if staged_only:
        output = git_ok("diff", "--cached", "--name-only") or ""
    else:
        output = git_ok("diff", "--name-only", f"{base}...HEAD") or ""
        if not output:
            output = git_ok("diff", "--name-only", base) or ""
    return [line for line in output.splitlines() if line]


def cmd_apply(base: str) -> int:
    if not changed_files(base, staged_only=True):
        return 0
    work = working_version()
    base_value = base_version(base)
    if is_ahead(work, base_value):
        return 0
    new_version = patch_bump(base_value or work or "0.0.0")
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    data["version"] = new_version
    PLUGIN_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    git("add", rel(PLUGIN_JSON))
    print(f"[version-bump] {PLUGIN_JSON.parent.parent.name}: {base_value or '(new)'} -> {new_version}")
    return 0


def cmd_check(base: str) -> int:
    if not changed_files(base, staged_only=False):
        print("OK — 没有需要检查版本递增的变更。")
        return 0

    work = working_version()
    base_value = base_version(base)
    if not is_ahead(work, base_value):
        print("FAIL — 根级插件已修改但版本未递增：", file=sys.stderr)
        print(
            f"  ✗ {rel(PLUGIN_JSON)}: {base_value} -> {work}。"
            "请递增 .codex-plugin/plugin.json 的 version。",
            file=sys.stderr,
        )
        return 1
    print("OK — 根级插件满足版本递增规则。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="根级 Codex 插件版本递增检查。")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="递增已暂存插件版本")
    mode.add_argument("--check", action="store_true", help="检查已修改插件版本")
    parser.add_argument("--base", help="对比基准，默认 origin/main 后退到 main")
    args = parser.parse_args()

    base = resolve_base(args.base)
    if base is None:
        print("[version-bump] 未找到基准引用，跳过。", file=sys.stderr)
        return 0

    return cmd_apply(base) if args.apply else cmd_check(base)


if __name__ == "__main__":
    sys.exit(main())
