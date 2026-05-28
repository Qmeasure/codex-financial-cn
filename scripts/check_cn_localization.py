#!/usr/bin/env python3
"""校验中文化和中文金融产物规则。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
SKILLS = ROOT / "skills"

REQUIRED_DOCS = [
    "DATA_SOURCES_CN.md",
    "CN_OUTPUT_FORMATTING.md",
    "OPTIONAL_MCP_TEMPLATES.md",
    "ACCEPTANCE_SAMPLES_CN.md",
    "THIRD_PARTY_NOTICES.md",
]

REQUIRED_SKILL_NEEDLES = [
    "中文版执行契约",
    "DATA_SOURCES_CN.md",
    "CN_OUTPUT_FORMATTING.md",
]

ARTIFACT_RULE_FILES = [
    "skills/xlsx-author/SKILL.md",
    "skills/pptx-author/SKILL.md",
    "skills/pitch-deck/reference/formatting-standards.md",
    "skills/3-statement-model/references/formatting.md",
]

FORBIDDEN_LEGACY_WORDING = [
    "Times New Roman (professional, readable, industry standard)",
    "USD Millions/Billions",
    "claude plugin",
    "Claude Code",
    "Cowork",
    ".claude-plugin",
    "managed-agent",
    "Managed Agents",
    "callable_agents",
    "POST /v1/agents",
    "commands/",
    "slash command",
    "斜杠命令",
]

TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".yaml",
    ".yml",
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

TECHNICAL_ASCII_ALLOW = {
    "A",
    "AI",
    "API",
    "Capital",
    "CLI",
    "CN",
    "Codex",
    "CTD",
    "DCF",
    "DOCX",
    "EBITDA",
    "EV",
    "FinQ4Cn",
    "G",
    "Global",
    "Greeks",
    "IRR",
    "Kensho",
    "KYC",
    "LBO",
    "LSEG",
    "LLM",
    "M",
    "MCP",
    "MOIC",
    "NAV",
    "OAS",
    "OpenBB",
    "P",
    "PEP",
    "PPTX",
    "SABR",
    "Services",
    "Tushare",
    "WACC",
    "XLSX",
    "Z",
}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


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


def strip_code_and_links(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", "", text)
    return text


def english_phrase_lines(text: str) -> list[str]:
    hits: list[str] = []
    for raw_line in strip_code_and_links(text).splitlines():
        line = raw_line.strip()
        if not line or has_cjk(line):
            continue
        if line.startswith("|"):
            continue
        if re.search(r"\.(png|jpg|jpeg|svg|csv|xlsx|pptx|docx|py|json|yaml|yml)\b", line):
            continue
        if re.search(r"[_=()\[\]{}]", line):
            continue
        if re.match(r"^(from|import|class|def|return|print|const|let|var|for|while|if|elif|else|with|try|except)\b", line):
            continue
        words = re.findall(r"[A-Za-z][A-Za-z0-9&./+-]*", line)
        meaningful = [word for word in words if word not in TECHNICAL_ASCII_ALLOW]
        if len(meaningful) >= 4:
            hits.append(line[:160])
    return hits


def check_required_docs() -> None:
    for doc in REQUIRED_DOCS:
        path = ROOT / doc
        if not path.is_file():
            err(f"缺少中文规则文档：{doc}")
            continue
        if not has_cjk(path.read_text(encoding="utf-8")):
            err(f"中文规则文档缺少中文内容：{doc}")


def check_manifest() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("name") != "financial-services-cn":
        err("plugin.json name 必须是 financial-services-cn")
    if not has_cjk(data.get("description", "")):
        err("plugin.json description 必须是中文")
    interface = data.get("interface", {})
    for field in ("displayName", "shortDescription", "longDescription"):
        if not has_cjk(interface.get(field, "")):
            err(f"plugin.json 的 interface.{field} 不是中文")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or any(not has_cjk(str(prompt)) for prompt in prompts):
        err("plugin.json 的 defaultPrompt 必须全部使用中文")


def check_skills() -> None:
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_files:
        err("没有找到任何 skill")
        return
    for skill in skill_files:
        text = skill.read_text(encoding="utf-8")
        if not has_cjk(text):
            err(f"skill 缺少中文内容：{rel(skill)}")
        for needle in REQUIRED_SKILL_NEEDLES:
            if needle not in text:
                err(f"skill 缺少 {needle}：{rel(skill)}")


def check_artifact_rules() -> None:
    for item in ARTIFACT_RULE_FILES:
        path = ROOT / item
        if not path.exists():
            err(f"缺少中文产物格式文件：{item}")
            continue
        text = path.read_text(encoding="utf-8")
        if "CN_OUTPUT_FORMATTING.md" not in text and "中文" not in text:
            err(f"产物格式文件缺少中文格式规则：{item}")


def check_forbidden_and_residual_text() -> None:
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for forbidden in FORBIDDEN_LEGACY_WORDING:
            if forbidden.lower() in text.lower():
                err(f"发现旧英文或旧架构文本 `{forbidden}`：{rel(path)}")
        if path.suffix == ".md":
            residual = english_phrase_lines(text)
            if residual:
                err(f"疑似未翻译英文行：{rel(path)}: {residual[0]}")


def main() -> int:
    check_required_docs()
    check_manifest()
    check_skills()
    check_artifact_rules()
    check_forbidden_and_residual_text()

    if errors:
        print(f"FAIL — {len(errors)} 个中文化问题：", file=sys.stderr)
        for message in errors:
            print(f"  ✗ {message}", file=sys.stderr)
        return 1
    print("OK — 中文化和中文金融产物规则检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
