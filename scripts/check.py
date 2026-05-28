#!/usr/bin/env python3
"""校验 Financial Services CN 的根级 Codex 插件结构。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MCP = ROOT / "OPTIONAL_MCP_SERVERS.json"
SKILLS = ROOT / "skills"

PLUGIN_NAME = "financial-services-cn"
EXPECTED_SKILL_COUNT = 66
EXPECTED_MCP_SERVERS = {
    "daloopa",
    "morningstar",
    "sp-global",
    "factset",
    "moodys",
    "mtnewswire",
    "aiera",
    "lseg",
    "lseg-server-cl",
    "pitchbook",
    "chronograph",
    "egnyte",
    "openbb-cn-market",
    "tushare-pro",
    "akshare-one",
}

REQUIRED_ROOT_DOCS = [
    "README.md",
    "AGENTS.md",
    "DATA_SOURCES_CN.md",
    "CN_OUTPUT_FORMATTING.md",
    "CN_DOCX_OUTPUT_CONTRACT.md",
    "OPTIONAL_MCP_TEMPLATES.md",
    "ACCEPTANCE_SAMPLES_CN.md",
    "THIRD_PARTY_NOTICES.md",
]

FORBIDDEN_DIR_NAMES = {
    ".agents",
    ".claude",
    ".claude-plugin",
    "agent-plugins",
    "claude-for-msft-365-install",
    "commands",
    "managed-agent-cookbooks",
    "plugins",
}

FORBIDDEN_TEXT_PATTERNS = [
    r"\.claude-plugin",
    r"\bclaude plugin\b",
    r"\bClaude Code\b",
    r"\bCowork\b",
    r"\bCMA\b",
    r"\bmanaged-agent\b",
    r"\bManaged Agents\b",
    r"\bcallable_agents\b",
    r"\bagent-plugins\b",
    r"\bmanaged-agent-cookbooks\b",
    r"POST /v1/agents",
    r"\bcommands/",
    r"\bslash command\b",
    r"斜杠命令",
]

TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".py",
    ".sh",
    ".yaml",
    ".yml",
    ".toml",
}

SKIP_PARTS = {
    ".git",
    "venv",
    "out",
    "__pycache__",
}

SKIP_TEXT_FILES = {
    ROOT / "scripts" / "check.py",
    ROOT / "scripts" / "check_cn_localization.py",
}

errors: list[str] = []
checked_json = 0


def err(message: str) -> None:
    errors.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    global checked_json
    checked_json += 1
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(f"缺少 JSON 文件：{rel(path)}")
    except json.JSONDecodeError as exc:
        err(f"JSON 解析失败：{rel(path)}: {exc}")
    return None


def has_cjk(value: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", value or ""))


def is_semver(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"\d+\.\d+\.\d+", value) is not None


def validate_root_docs() -> None:
    for doc in REQUIRED_ROOT_DOCS:
        if not (ROOT / doc).is_file():
            err(f"缺少根文档：{doc}")


def validate_forbidden_paths() -> None:
    for path in ROOT.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.is_dir() and path.name in FORBIDDEN_DIR_NAMES:
            err(f"发现旧架构目录：{rel(path)}")


def validate_manifest() -> None:
    data = load_json(MANIFEST)
    if not isinstance(data, dict):
        return

    if data.get("name") != PLUGIN_NAME:
        err(f"plugin.json name 必须是 {PLUGIN_NAME}")
    if not is_semver(data.get("version")):
        err("plugin.json version 必须是 x.y.z")
    if not has_cjk(str(data.get("description", ""))):
        err("plugin.json description 必须是中文")
    if data.get("skills") != "./skills/":
        err("plugin.json skills 必须是 ./skills/")
    if "mcpServers" in data:
        err("plugin.json 默认不得声明 mcpServers；机构源和本地 MCP 只能保留为可选配置")
    if "hooks" in data:
        err("plugin.json 不得声明 hooks")
    if "apps" in data and not (ROOT / ".app.json").is_file():
        err("没有 .app.json 时不得声明 apps")

    interface = data.get("interface")
    if not isinstance(interface, dict):
        err("plugin.json 缺少 interface")
        return

    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not interface.get(key):
            err(f"interface.{key} 不能为空")
    for key in ("displayName", "shortDescription", "longDescription"):
        if not has_cjk(str(interface.get(key, ""))):
            err(f"interface.{key} 必须是中文")
    if interface.get("capabilities") != ["Interactive", "Read", "Write"]:
        err("interface.capabilities 必须是 Interactive/Read/Write")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or len(prompts) != 3:
        err("interface.defaultPrompt 必须是 3 条中文 prompt")
    else:
        for prompt in prompts:
            if not has_cjk(str(prompt)):
                err("defaultPrompt 必须使用中文")


def validate_mcp_config() -> None:
    data = load_json(MCP)
    if not isinstance(data, dict):
        return
    servers = data.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        err("OPTIONAL_MCP_SERVERS.json 必须包含非空 mcpServers 对象")
        return

    names = set(servers)
    if names != EXPECTED_MCP_SERVERS:
        missing = sorted(EXPECTED_MCP_SERVERS - names)
        extra = sorted(names - EXPECTED_MCP_SERVERS)
        err(f"OPTIONAL_MCP_SERVERS.json MCP 清单不正确，缺少 {missing}，多出 {extra}")
    if "spglobal" in names:
        err("S&P Global MCP 必须统一命名为 sp-global")

    for server_name, config in servers.items():
        if not isinstance(config, dict):
            err(f"MCP {server_name} 配置必须是对象")
            continue
        has_url = isinstance(config.get("url"), str) and bool(config.get("url"))
        has_command = isinstance(config.get("command"), str) and bool(config.get("command"))
        if has_url == has_command:
            err(f"MCP {server_name} 必须且只能声明 url 或 command")
        if has_url and not str(config["url"]).startswith(("http://", "https://")):
            err(f"MCP {server_name} 的 url 必须是 HTTP(S) 地址")
        if has_command:
            args = config.get("args", [])
            if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
                err(f"MCP {server_name} 的 args 必须是字符串数组")
            env = config.get("env", {})
            if env and (not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items())):
                err(f"MCP {server_name} 的 env 必须是字符串字典")
    tushare = servers.get("tushare-pro", {})
    if tushare.get("env", {}).get("TUSHARE_TOKEN") != "${TUSHARE_TOKEN}":
        err("tushare-pro 必须通过 ${TUSHARE_TOKEN} 读取 token")


def validate_skills() -> None:
    if not SKILLS.is_dir():
        err("缺少 skills/ 目录")
        return
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if len(skill_files) != EXPECTED_SKILL_COUNT:
        err(f"SKILL.md 数量必须是 {EXPECTED_SKILL_COUNT}，当前为 {len(skill_files)}")

    for skill in skill_files:
        text = skill.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---\n"):
            err(f"skill 缺少 YAML frontmatter：{rel(skill)}")
        if not has_cjk(text):
            err(f"skill 缺少中文内容：{rel(skill)}")


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path in SKIP_TEXT_FILES:
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return files


def validate_forbidden_text() -> None:
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                err(f"发现旧架构文本 `{pattern}`：{rel(path)}")


def main() -> int:
    validate_root_docs()
    validate_forbidden_paths()
    validate_manifest()
    validate_mcp_config()
    validate_skills()
    validate_forbidden_text()

    if errors:
        print(f"FAIL — {len(errors)} 个结构问题：", file=sys.stderr)
        for message in errors:
            print(f"  ✗ {message}", file=sys.stderr)
        return 1
    print(f"OK — 根级 Codex 插件结构检查通过，解析 {checked_json} 个 JSON 文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
