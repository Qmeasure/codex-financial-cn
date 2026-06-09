#!/usr/bin/env python3
"""仓库自带的根级 Codex plugin manifest 校验入口。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"

errors: list[str] = []


def err(message: str) -> None:
    errors.append(message)


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err("缺少 .codex-plugin/plugin.json")
        return {}
    except json.JSONDecodeError as exc:
        err(f"plugin.json 不是合法 JSON：{exc}")
        return {}
    if not isinstance(payload, dict):
        err("plugin.json 必须是 JSON 对象")
        return {}
    return payload


def normalize_contract_path(raw_path: object) -> str | None:
    if not isinstance(raw_path, str):
        return None
    path = raw_path.strip().removeprefix("./").rstrip("/")
    return path or None


def validate_contract_path(data: dict, key: str, expected: str) -> None:
    value = data.get(key)
    normalized = normalize_contract_path(value)
    if normalized != expected:
        err(f"plugin.json 的 {key} 必须是 {expected}")
    if normalized and not (ROOT / expected).exists():
        err(f"plugin.json 的 {key} 指向不存在的路径")


def validate_optional_contract_path(data: dict, key: str, expected: str) -> None:
    if key not in data:
        return
    validate_contract_path(data, key, expected)


def main() -> int:
    data = load_json(MANIFEST)
    if not data:
        return 1

    allowed = {
        "id",
        "name",
        "version",
        "description",
        "skills",
        "apps",
        "mcpServers",
        "interface",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
    }
    for key in sorted(set(data) - allowed):
        err(f"plugin.json 不支持字段 {key}")

    if data.get("name") != "financial-services-cn":
        err("plugin.json 的 name 必须是 financial-services-cn")
    if not isinstance(data.get("version"), str) or not re.fullmatch(
        r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
        data["version"],
    ):
        err("plugin.json 的 version 必须是 semver，可包含 pre-release 或 build metadata")
    if not data.get("description"):
        err("plugin.json 的 description 不能为空")
    if not isinstance(data.get("author"), dict) or not data["author"].get("name"):
        err("plugin.json 的 author.name 不能为空")

    validate_contract_path(data, "skills", "skills")
    validate_optional_contract_path(data, "mcpServers", ".mcp.json")
    if "apps" in data and not (ROOT / ".app.json").is_file():
        err("没有 .app.json 时不得声明 apps")

    interface = data.get("interface")
    if not isinstance(interface, dict):
        err("plugin.json 必须包含 interface 对象")
    else:
        for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            if not interface.get(field):
                err(f"interface.{field} 不能为空")
        capabilities = interface.get("capabilities")
        if not isinstance(capabilities, list) or not all(isinstance(item, str) and item for item in capabilities):
            err("interface.capabilities 必须是非空字符串数组")
        if "defaultPrompt" not in interface and "default_prompt" not in interface:
            err("interface.defaultPrompt 不能为空")

    if errors:
        print(f"FAIL — {len(errors)} 个 Codex manifest 问题：", file=sys.stderr)
        for message in errors:
            print(f"  ✗ {message}", file=sys.stderr)
        return 1
    print(f"OK — 根级 Codex plugin manifest 校验通过：{ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
