#!/usr/bin/env python3
"""校验 Financial Services CN 的根级 Codex 插件结构。"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
MCP = ROOT / "OPTIONAL_MCP_SERVERS.json"
SKILLS = ROOT / "skills"

PLUGIN_NAME = "financial-services-cn"
EXPECTED_REPOSITORY = "https://github.com/Qmeasure/codex-financial-cn"
EXPECTED_SKILL_COUNT = 66

REQUIRED_ROOT_DOCS = [
    "README.md",
    "AGENTS.md",
    "DATA_SOURCES_CN.md",
    "DATA_QUERY_ORDER_CN.md",
    "CN_OUTPUT_FORMATTING.md",
    "CN_DOCX_OUTPUT_CONTRACT.md",
    "CN_XLSX_OUTPUT_CONTRACT.md",
    "CN_PPTX_OUTPUT_CONTRACT.md",
    "CN_MARKDOWN_OUTPUT_CONTRACT.md",
    "CN_HTML_OUTPUT_CONTRACT.md",
    "CN_CHART_OUTPUT_CONTRACT.md",
    "OPTIONAL_MCP_TEMPLATES.md",
    "ACCEPTANCE_SAMPLES_CN.md",
    "THIRD_PARTY_NOTICES.md",
]

ROOT_CONTRACT_DOCS = {
    "DATA_SOURCES_CN.md",
    "DATA_QUERY_ORDER_CN.md",
    "CN_OUTPUT_FORMATTING.md",
    "CN_DOCX_OUTPUT_CONTRACT.md",
    "CN_XLSX_OUTPUT_CONTRACT.md",
    "CN_PPTX_OUTPUT_CONTRACT.md",
    "CN_MARKDOWN_OUTPUT_CONTRACT.md",
    "CN_HTML_OUTPUT_CONTRACT.md",
    "CN_CHART_OUTPUT_CONTRACT.md",
}

FORBIDDEN_PATH_PARTS = {
    ".agents",
    ".claude",
    ".codex",
    "agent-plugins",
    "claude-for-msft-365-install",
    "commands",
    "managed-agent-cookbooks",
    "plugins",
}

FORBIDDEN_TEXT_PATTERNS = [
    r"(?<!-)\.claude/",
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
    return isinstance(value, str) and re.fullmatch(
        r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
        value,
    ) is not None


def validate_root_docs() -> None:
    for doc in REQUIRED_ROOT_DOCS:
        if not (ROOT / doc).is_file():
            err(f"缺少根文档：{doc}")


def iter_repository_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return [ROOT / line for line in result.stdout.splitlines() if line]
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
    ]


def validate_forbidden_paths() -> None:
    for path in iter_repository_files():
        parts = set(path.relative_to(ROOT).parts)
        forbidden = parts & FORBIDDEN_PATH_PARTS
        if forbidden:
            err(f"发现旧架构或本地运行时路径：{rel(path)}")


def validate_manifest() -> None:
    data = load_json(MANIFEST)
    if not isinstance(data, dict):
        return

    if data.get("name") != PLUGIN_NAME:
        err(f"plugin.json name 必须是 {PLUGIN_NAME}")
    if not is_semver(data.get("version")):
        err("plugin.json version 必须是 semver，可包含 pre-release 或 build metadata")
    if not has_cjk(str(data.get("description", ""))):
        err("plugin.json description 必须是中文")
    if data.get("skills") != "./skills/":
        err("plugin.json skills 必须是 ./skills/")
    if data.get("homepage") != EXPECTED_REPOSITORY:
        err(f"plugin.json homepage 必须是 {EXPECTED_REPOSITORY}")
    if data.get("repository") != EXPECTED_REPOSITORY:
        err(f"plugin.json repository 必须是 {EXPECTED_REPOSITORY}")
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


def validate_no_runtime_components(data: dict[str, Any], label: str) -> None:
    for key in ("mcpServers", "hooks", "agents", "commands"):
        if key in data:
            err(f"{label} 默认不得声明 {key}；本仓库只通过 skills/ 暴露能力")


def validate_claude_plugin_config() -> None:
    codex = load_json(MANIFEST)
    claude = load_json(CLAUDE_MANIFEST)
    marketplace = load_json(CLAUDE_MARKETPLACE)
    if not isinstance(codex, dict) or not isinstance(claude, dict) or not isinstance(marketplace, dict):
        return

    interface = codex.get("interface", {})
    expected_display_name = interface.get("displayName") if isinstance(interface, dict) else None
    for key in ("name", "version", "homepage", "repository", "license"):
        if claude.get(key) != codex.get(key):
            err(f"Claude Code plugin.json 的 {key} 必须与 Codex manifest 一致")
    if claude.get("skills") != "./skills/":
        err("Claude Code plugin.json skills 必须是 ./skills/")
    if expected_display_name and claude.get("displayName") != expected_display_name:
        err("Claude Code plugin.json displayName 必须与 Codex interface.displayName 一致")
    if not has_cjk(str(claude.get("description", ""))):
        err("Claude Code plugin.json description 必须是中文")
    codex_author = codex.get("author")
    author = claude.get("author")
    expected_author_name = codex_author.get("name") if isinstance(codex_author, dict) else None
    if not isinstance(author, dict) or author.get("name") != expected_author_name:
        err("Claude Code plugin.json author.name 必须与 Codex manifest 一致")
    validate_no_runtime_components(claude, "Claude Code plugin.json")

    if marketplace.get("name") != PLUGIN_NAME:
        err(f"Claude Code marketplace name 必须是 {PLUGIN_NAME}")
    if not has_cjk(str(marketplace.get("description", ""))):
        err("Claude Code marketplace description 必须是中文")
    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        err("Claude Code marketplace owner.name 不能为空")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        err("Claude Code marketplace 必须只声明 financial-services-cn 一个插件")
        return
    entry = plugins[0]
    if entry.get("name") != PLUGIN_NAME:
        err(f"Claude Code marketplace 插件 name 必须是 {PLUGIN_NAME}")
    if entry.get("source") != "./":
        err("Claude Code marketplace 插件 source 必须是 ./")
    for key in ("version", "homepage", "repository", "license"):
        if entry.get(key) != codex.get(key):
            err(f"Claude Code marketplace 插件 {key} 必须与 Codex manifest 一致")
    if expected_display_name and entry.get("displayName") != expected_display_name:
        err("Claude Code marketplace 插件 displayName 必须与 Codex interface.displayName 一致")
    if not has_cjk(str(entry.get("description", ""))):
        err("Claude Code marketplace 插件 description 必须是中文")
    validate_no_runtime_components(entry, "Claude Code marketplace 插件")


def validate_mcp_config() -> None:
    data = load_json(MCP)
    if not isinstance(data, dict):
        return
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        err("OPTIONAL_MCP_SERVERS.json 必须包含 mcpServers 对象")
        return

    names = set(servers)
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
    tushare = servers.get("tushare-pro")
    if isinstance(tushare, dict) and tushare.get("env", {}).get("TUSHARE_TOKEN") != "${TUSHARE_TOKEN}":
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
        for root_contract in (
            "../../DATA_SOURCES_CN.md",
            "../../DATA_QUERY_ORDER_CN.md",
            "../../CN_OUTPUT_FORMATTING.md",
            "../../CN_MARKDOWN_OUTPUT_CONTRACT.md",
        ):
            if root_contract not in text:
                err(f"skill 未引用根级共享合同 {root_contract}：{rel(skill)}")


def validate_shared_contract_layout() -> None:
    for skill_dir in sorted(SKILLS.glob("*")):
        if not skill_dir.is_dir():
            continue
        for folder_name in ("references", "reference"):
            refs = skill_dir / folder_name
            if not refs.is_dir():
                continue
            data_reference = refs / "data-query-order.md"
            if data_reference.exists():
                err(f"不得保留本地 data query reference 文件：{rel(data_reference)}")
            for formatting_reference in refs.glob("cn-*formatting.md"):
                err(f"不得保留本地 formatting reference 文件：{rel(formatting_reference)}")


def validate_root_contract_references() -> None:
    contract_pattern = "|".join(re.escape(item) for item in sorted(ROOT_CONTRACT_DOCS))
    pattern = re.compile(r"(?<!\.)(?:\.\./)+(?:%s)" % contract_pattern)
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            target = (path.parent / match.group(0)).resolve()
            if not target.is_file():
                err(f"根级合同引用不可解析：{rel(path)} -> {match.group(0)}")


def validate_forbidden_text() -> None:
    for path in iter_repository_files():
        if path in SKIP_TEXT_FILES:
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                err(f"发现旧架构文本 `{pattern}`：{rel(path)}")


def main() -> int:
    validate_root_docs()
    validate_forbidden_paths()
    validate_manifest()
    validate_claude_plugin_config()
    validate_mcp_config()
    validate_skills()
    validate_shared_contract_layout()
    validate_root_contract_references()
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
