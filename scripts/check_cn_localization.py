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
    "CN_DOCX_OUTPUT_CONTRACT.md",
    "CN_XLSX_OUTPUT_CONTRACT.md",
    "CN_PPTX_OUTPUT_CONTRACT.md",
    "CN_MARKDOWN_OUTPUT_CONTRACT.md",
    "OPTIONAL_MCP_TEMPLATES.md",
    "ACCEPTANCE_SAMPLES_CN.md",
    "THIRD_PARTY_NOTICES.md",
]

REQUIRED_SKILL_NEEDLES = [
    "中文版执行契约",
    "../../DATA_SOURCES_CN.md",
    "../../CN_OUTPUT_FORMATTING.md",
    "../../CN_MARKDOWN_OUTPUT_CONTRACT.md",
    "references/cn-markdown-formatting.md",
    "references/data-query-order.md",
    "产物合同读取与输出门槛",
    "生成正式输出前必须读取",
    "聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物",
]

DOCX_SKILLS = {
    "cim-builder",
    "client-report",
    "client-review",
    "earnings-analysis",
    "financial-plan",
    "ic-memo",
    "initiating-coverage",
    "model-update",
    "morning-note",
    "process-letter",
    "sector-overview",
    "tear-sheet",
    "teaser",
    "thesis-tracker",
    "value-creation-plan",
}

XLSX_SKILLS = {
    "3-statement-model",
    "buyer-list",
    "catalyst-calendar",
    "clean-data-xls",
    "comps-analysis",
    "datapack-builder",
    "dcf-model",
    "dd-checklist",
    "deal-tracker",
    "initiating-coverage",
    "lbo-model",
    "merger-model",
    "model-update",
    "portfolio-rebalance",
    "returns-analysis",
    "tax-loss-harvesting",
    "unit-economics",
    "xlsx-author",
}

PPTX_SKILLS = {
    "competitive-analysis",
    "deck-refresh",
    "funding-digest",
    "investment-proposal",
    "pitch-deck",
    "ppt-template-creator",
    "pptx-author",
    "sector-overview",
    "strip-profile",
    "teaser",
    "value-creation-plan",
}

HTML_SKILLS = {
    "earnings-preview-beta",
}

CHART_SKILLS = {
    "initiating-coverage",
}

ARTIFACT_CONTRACTS = {
    "DOCX": ("../../CN_DOCX_OUTPUT_CONTRACT.md", DOCX_SKILLS),
    "XLSX": ("../../CN_XLSX_OUTPUT_CONTRACT.md", XLSX_SKILLS),
    "PPTX": ("../../CN_PPTX_OUTPUT_CONTRACT.md", PPTX_SKILLS),
}

LOCAL_REFERENCE_CONTRACTS = {
    "DOCX": ("references/cn-docx-formatting.md", DOCX_SKILLS, "DOCX 文件"),
    "XLSX": ("references/cn-xlsx-formatting.md", XLSX_SKILLS, "XLSX 文件"),
    "PPTX": ("references/cn-pptx-formatting.md", PPTX_SKILLS, "PPTX 文件"),
    "HTML": ("references/cn-html-formatting.md", HTML_SKILLS, "HTML 文件"),
    "图表/ZIP": ("references/cn-chart-formatting.md", CHART_SKILLS, "图表/ZIP 文件"),
}

BASELINE_REFERENCE_FILES = {
    "cn-markdown-formatting.md": (
        "中文 Markdown 与聊天输出格式合同",
        "不得把聊天摘要冒充已经生成的文件交付物",
    ),
    "data-query-order.md": (
        "数据查询顺序合同",
        "先检查用户提供的文件、当前会话可用 MCP",
        "再进行网页搜索",
    ),
}

TYPE_REFERENCE_FILES = {
    "cn-docx-formatting.md": ("中文 DOCX 格式合同", "w:rFonts@w:eastAsia", "最终回复必须包含 DOCX 文件路径"),
    "cn-xlsx-formatting.md": ("中文 XLSX 格式合同", "公式", "最终回复必须包含 XLSX 文件路径"),
    "cn-pptx-formatting.md": ("中文 PPTX 格式合同", "文字溢出", "最终回复必须包含 PPTX 文件路径"),
    "cn-html-formatting.md": ("中文 HTML 格式合同", "浏览器打开", "最终回复必须包含 HTML 文件路径"),
    "cn-chart-formatting.md": ("中文图表与 ZIP 交付格式合同", "中文字体", "最终回复必须包含图表/ZIP 文件路径"),
}

GENERATED_REFERENCE_NAMES = set(BASELINE_REFERENCE_FILES) | set(TYPE_REFERENCE_FILES)

ARTIFACT_RULE_FILES = [
    "skills/xlsx-author/SKILL.md",
    "skills/pptx-author/SKILL.md",
    "skills/earnings-analysis/SKILL.md",
    "skills/earnings-analysis/references/report-structure.md",
    "skills/earnings-analysis/references/best-practices.md",
    "skills/pitch-deck/reference/formatting-standards.md",
    "skills/3-statement-model/references/formatting.md",
]

EARNINGS_ANALYSIS_NEEDLES = [
    "交付物硬门槛",
    "默认意图解析",
    "DOCX 生成前必须读取",
    "CN_DOCX_OUTPUT_CONTRACT.md",
    "未生成 DOCX 时，不得声称任务完成",
    "最终回复必须包含 DOCX 文件路径",
    "cn_institutional_research_brief",
    "DOCX 主交付物未完成",
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
        skill_name = skill.parent.name
        refs = skill.parent / "references"
        for filename, needles in BASELINE_REFERENCE_FILES.items():
            path = refs / filename
            if not path.is_file():
                err(f"{skill_name} 缺少本地 reference：references/{filename}")
                continue
            ref_text = path.read_text(encoding="utf-8")
            for needle in needles:
                if needle not in ref_text:
                    err(f"{skill_name} 的 references/{filename} 缺少 `{needle}`")
        for artifact_type, (contract, skill_names) in ARTIFACT_CONTRACTS.items():
            if skill_name not in skill_names:
                continue
            for needle in (
                contract,
                f"{artifact_type} 文件已生成",
                f"{artifact_type} 文件路径存在",
                f"最终回复包含 {artifact_type} 文件路径",
            ):
                if needle not in text:
                    err(f"{skill_name} 缺少 {artifact_type} 交付门槛 `{needle}`")
        for artifact_type, (local_ref, skill_names, gate_prefix) in LOCAL_REFERENCE_CONTRACTS.items():
            if skill_name not in skill_names:
                continue
            if local_ref not in text:
                err(f"{skill_name} 缺少本地 {artifact_type} reference 读取指令：{local_ref}")
            filename = local_ref.split("/", 1)[1]
            path = refs / filename
            if not path.is_file():
                err(f"{skill_name} 缺少本地 {artifact_type} reference 文件：{local_ref}")
                continue
            ref_text = path.read_text(encoding="utf-8")
            for needle in TYPE_REFERENCE_FILES[filename]:
                if needle not in ref_text:
                    err(f"{skill_name} 的 {local_ref} 缺少 `{needle}`")
            for needle in (
                f"{gate_prefix}已生成",
                f"{gate_prefix}路径存在",
                f"最终回复包含{gate_prefix}路径",
            ):
                spaced = needle.replace("最终回复包含", "最终回复包含 ")
                if needle not in text and spaced not in text:
                    err(f"{skill_name} 缺少 {artifact_type} 本地交付门槛 `{needle}`")


def check_artifact_rules() -> None:
    for item in ARTIFACT_RULE_FILES:
        path = ROOT / item
        if not path.exists():
            err(f"缺少中文产物格式文件：{item}")
            continue
        text = path.read_text(encoding="utf-8")
        if "CN_OUTPUT_FORMATTING.md" not in text and "中文" not in text:
            err(f"产物格式文件缺少中文格式规则：{item}")


def check_reference_linkage() -> None:
    for folder_name in ("references", "reference"):
        for path in sorted(SKILLS.glob(f"*/{folder_name}/*.md")):
            if path.name in GENERATED_REFERENCE_NAMES:
                continue
            text = path.read_text(encoding="utf-8")
            if "Reference 链路：执行本文件前" not in text:
                err(f"既有 reference 文件缺少本地格式链路提示：{rel(path)}")
            if "references/data-query-order.md" not in text or "references/cn-markdown-formatting.md" not in text:
                err(f"既有 reference 文件未指向本地数据/Markdown 合同：{rel(path)}")
            for generated_title in (
                "中文 DOCX 格式合同",
                "中文 XLSX 格式合同",
                "中文 PPTX 格式合同",
                "中文 HTML 格式合同",
                "中文图表与 ZIP 交付格式合同",
            ):
                if generated_title in text:
                    err(f"既有 reference 文件疑似承载新增格式正文：{rel(path)}")

    template = ROOT / "skills" / "earnings-preview-beta" / "report-template.md"
    if template.is_file():
        text = template.read_text(encoding="utf-8")
        if "references/cn-html-formatting.md" not in text:
            err("earnings-preview-beta/report-template.md 未指向本地 HTML 格式合同")


def check_earnings_analysis_contract() -> None:
    skill = ROOT / "skills" / "earnings-analysis" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    for needle in EARNINGS_ANALYSIS_NEEDLES:
        if needle not in text:
            err(f"earnings-analysis 缺少硬门槛文本：{needle}")


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
    check_reference_linkage()
    check_earnings_analysis_contract()
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
