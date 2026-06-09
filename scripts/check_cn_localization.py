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

REQUIRED_SKILL_NEEDLES = [
    "中文版执行契约",
    "../../DATA_SOURCES_CN.md",
    "../../DATA_QUERY_ORDER_CN.md",
    "../../CN_OUTPUT_FORMATTING.md",
    "../../CN_MARKDOWN_OUTPUT_CONTRACT.md",
    "产物合同读取与输出门槛",
    "生成正式输出前必须读取",
    "先生成“数据源发现记录”",
    "Gate 通过前不得网页搜索",
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

HTML_SKILLS = {"earnings-preview-beta"}
CHART_SKILLS = {"initiating-coverage"}

ARTIFACT_CONTRACTS = {
    "DOCX": ("../../CN_DOCX_OUTPUT_CONTRACT.md", DOCX_SKILLS, "DOCX 文件"),
    "XLSX": ("../../CN_XLSX_OUTPUT_CONTRACT.md", XLSX_SKILLS, "XLSX 文件"),
    "PPTX": ("../../CN_PPTX_OUTPUT_CONTRACT.md", PPTX_SKILLS, "PPTX 文件"),
    "HTML": ("../../CN_HTML_OUTPUT_CONTRACT.md", HTML_SKILLS, "HTML 文件"),
    "图表/ZIP": ("../../CN_CHART_OUTPUT_CONTRACT.md", CHART_SKILLS, "图表/ZIP 文件"),
}

DATA_REFERENCE_NEEDLES = (
    "数据查询顺序合同",
    "网页搜索前 Gate",
    "数据源发现记录",
    "已说明是否实际调用；未调用时必须写明原因",
    "Gate 未通过时，不得网页搜索",
    "未覆盖数据项",
)

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

ROOT_FONT_CONTRACTS = {
    "CN_OUTPUT_FORMATTING.md": (
        "Source Han Serif CN",
        "唯一指定字体",
        "SubsetOTF/CN/SourceHanSerifCN-Regular.otf",
        "SubsetOTF/CN/SourceHanSerifCN-Bold.otf",
        "图表内部来源固定为 7pt Regular",
        "DOCX 中图表下方只允许居中标注 `图表 N：<主题>`",
    ),
    "CN_DOCX_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        'w:eastAsia`、`w:ascii`、`w:hAnsi` 都必须等于 `Source Han Serif CN`',
        "body: {size: 10.5pt, weight: Regular, line_spacing: 1.20",
        "表头默认 8.5pt Bold，行距 1.15",
        "表体默认 8.5pt Regular，行距 1.15",
        "图表内部来源固定为 7pt Regular",
        "`图表 N：<主题>` 默认 9pt Bold",
        "图表下方不得再另写来源小字",
    ),
    "CN_PPTX_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        "正文默认 11pt Regular，行距 1.15",
        "表体默认 8.5pt Regular",
        "图表内部来源默认 7pt Regular",
        "同时导出 PDF 作为字体视觉兜底",
    ),
    "CN_XLSX_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        "工作簿默认字体为 10pt Regular，默认行高 18pt",
        "表体默认 10pt Regular，行高 18pt",
        "图表内部来源默认 7pt Regular",
    ),
    "CN_MARKDOWN_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        "Markdown 原文不声明字体",
        "导出为 DOCX 时，图表下方只允许居中 `图表 N：<主题>`",
    ),
    "CN_HTML_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        "cdn.jsdelivr.net/gh/adobe-fonts/source-han-serif@release/SubsetOTF/CN/SourceHanSerifCN-Regular.otf",
        "cdn.jsdelivr.net/gh/adobe-fonts/source-han-serif@release/SubsetOTF/CN/SourceHanSerifCN-Bold.otf",
        "正文默认 15px Regular，line-height 1.55",
    ),
    "CN_CHART_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        "图表标题默认 12pt Bold",
        "图表内部来源默认 7pt Regular",
        "major/minor gridlines",
    ),
}

ROOT_CHART_STYLE_CONTRACTS = {
    "CN_OUTPUT_FORMATTING.md": (
        "柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线",
        "major/minor gridlines",
        "图表内部来源固定为 7pt Regular",
        "固定校验标签",
        "正式表格缺失值显示 `—`",
    ),
    "CN_DOCX_OUTPUT_CONTRACT.md": (
        "柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线",
        "major/minor gridlines",
        "DOCX 中嵌入的 PNG/JPG 图表也必须遵守",
        "Render QA 必须检查柱状图是否错误显示纵坐标横向网格线",
        "图表下方不得再另写来源小字",
        "DOCX 章节默认连续排版",
        "只允许 Word 自然分页",
    ),
    "CN_PPTX_OUTPUT_CONTRACT.md": (
        "柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线",
        "major/minor gridlines",
        "PPTX 中嵌入的 PNG/JPG 图表也必须遵守",
        "没有错误显示纵坐标横向网格线",
        "图表内部来源默认 7pt Regular",
    ),
    "CN_XLSX_OUTPUT_CONTRACT.md": (
        "图表内部来源默认 7pt Regular",
        "正式表格缺失值使用 `—`",
    ),
    "CN_MARKDOWN_OUTPUT_CONTRACT.md": (
        "导出为 DOCX 时，图表下方只允许居中 `图表 N：<主题>`",
        "正式表格缺失值使用 `—`",
    ),
    "CN_HTML_OUTPUT_CONTRACT.md": (
        "Source Han Serif CN",
        "图表内部来源默认 7pt Regular",
    ),
    "CN_CHART_OUTPUT_CONTRACT.md": (
        "柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线",
        "major/minor gridlines",
        "图表内部来源默认 7pt Regular",
    ),
}

DOCX_PAGINATION_CONTRACT_NEEDLES = (
    "DOCX 章节默认连续排版",
    "只允许 Word 自然分页",
    "只有用户明确要求",
)

DOCX_PAGINATION_FORBIDDEN_TEXT = (
    "逐页模板",
    "pageBreakBefore",
    "w:pageBreakBefore",
    "add_page_break",
    "WD_BREAK.PAGE",
    'w:type="page"',
    "自动换页",
    "另起一页",
)

DOCX_PAGINATION_FORBIDDEN_REGEX = (
    re.compile(r"^##\s+第\s*\d", re.MULTILINE),
    re.compile(r"创建第\s*1\s*页"),
)

CHART_WORKFLOW_FILES = [
    "skills/competitive-analysis/SKILL.md",
    "skills/earnings-analysis/SKILL.md",
    "skills/earnings-analysis/references/best-practices.md",
    "skills/earnings-analysis/references/workflow.md",
    "skills/earnings-preview-beta/SKILL.md",
    "skills/earnings-preview-beta/report-template.md",
    "skills/funding-digest/SKILL.md",
    "skills/initiating-coverage/SKILL.md",
    "skills/initiating-coverage/assets/quality-checklist.md",
    "skills/initiating-coverage/assets/report-template.md",
    "skills/initiating-coverage/references/task1-company-research.md",
    "skills/initiating-coverage/references/task4-chart-generation.md",
    "skills/initiating-coverage/references/task5-report-assembly.md",
    "skills/pptx-author/SKILL.md",
    "skills/strip-profile/SKILL.md",
]

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
    "数据源发现硬门槛",
    "数据源发现记录必须包含",
    "未生成该记录，不得进入网页搜索",
    "最终报告必须在“数据来源与口径说明”中摘要列示该记录",
    "默认意图解析",
    "DOCX 生成前必须读取",
    "CN_DOCX_OUTPUT_CONTRACT.md",
    "未生成 DOCX 时，不得声称任务完成",
    "最终回复必须包含 DOCX 文件路径",
    "cn_institutional_research_brief",
    "DOCX 主交付物未完成",
]

WEAK_DATA_GATE_WORDING = [
    "可用 MCP/已授权数据源优先，网页搜索其次",
    "先检查可用 MCP/已授权源",
    "先检查可用 MCP/已授权数据源",
    "再在覆盖不足时",
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

FORBIDDEN_FONT_WORDING = [
    "Microsoft YaHei",
    "微软雅黑",
    "PingFang SC",
    "SimHei",
    "SimSun",
    "Source Han Sans",
    "中文字体栈",
    "fallback_fonts",
]

FORBIDDEN_OUTPUT_LABELS = [
    "\u7ec8\u7aef\u8d1f\u8377",
    "\u7ec8\u7aef\u590d\u6838",
    "\u7ec8\u7aef\u5ba1\u6838",
    "\u9700\u7ec8\u7aef\u590d\u6838",
    "\u9700\u786e\u8ba4",
    "\u5f85\u786e\u8ba4",
    "\u590d\u6838",
]

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml"}
SKIP_PARTS = {".git", "venv", "out", "__pycache__"}
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
    "DCF",
    "DOCX",
    "EBITDA",
    "EV",
    "Global",
    "HTML",
    "IRR",
    "Kensho",
    "KYC",
    "LBO",
    "LSEG",
    "LLM",
    "MCP",
    "MOIC",
    "NAV",
    "OpenBB",
    "PPTX",
    "Source",
    "Han",
    "Serif",
    "Tushare",
    "WACC",
    "XLSX",
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
        if re.search(r"\.(png|jpg|jpeg|svg|csv|xlsx|pptx|docx|py|json|yaml|yml|otf)\b", line):
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


def check_no_local_formatting_references() -> None:
    for folder_name in ("references", "reference"):
        for path in sorted(SKILLS.glob(f"*/{folder_name}/cn-*formatting.md")):
            err(f"不得保留本地 formatting reference：{rel(path)}")
        for path in sorted(SKILLS.glob(f"*/{folder_name}/data-query-order.md")):
            err(f"不得保留本地 data query reference：{rel(path)}")
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"references/cn-[a-z]+-formatting\.md", text):
            err(f"不得再引用本地 formatting reference：{rel(path)}")
        if "references/data-query-order.md" in text:
            err(f"不得再引用本地 data query reference：{rel(path)}")


def check_root_data_query_contract() -> None:
    path = ROOT / "DATA_QUERY_ORDER_CN.md"
    if not path.exists():
        err("缺少根级 DATA_QUERY_ORDER_CN.md")
        return
    text = path.read_text(encoding="utf-8")
    for needle in DATA_REFERENCE_NEEDLES:
        if needle not in text:
            err(f"DATA_QUERY_ORDER_CN.md 缺少 `{needle}`")


def check_root_contract_references() -> None:
    contract_pattern = "|".join(re.escape(item) for item in sorted(ROOT_CONTRACT_DOCS))
    pattern = re.compile(r"(?<!\.)(?:\.\./)+(?:%s)" % contract_pattern)
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            target = (path.parent / match.group(0)).resolve()
            if not target.is_file():
                err(f"根级合同引用不可解析：{rel(path)} -> {match.group(0)}")


def check_root_font_contracts() -> None:
    for item, needles in ROOT_FONT_CONTRACTS.items():
        path = ROOT / item
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                err(f"{item} 缺少字体参数 `{needle}`")


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
        for artifact_type, (contract, skill_names, gate_prefix) in ARTIFACT_CONTRACTS.items():
            if skill_name not in skill_names:
                continue
            for needle in (
                contract,
                f"{gate_prefix}已生成",
                f"{gate_prefix}路径存在",
                f"最终回复包含 {gate_prefix}路径",
            ):
                spaced = needle.replace("最终回复包含", "最终回复包含 ")
                if needle not in text and spaced not in text:
                    err(f"{skill_name} 缺少 {artifact_type} 交付门槛 `{needle}`")


def check_artifact_rules() -> None:
    for item in ARTIFACT_RULE_FILES:
        path = ROOT / item
        if not path.exists():
            err(f"缺少中文产物格式文件：{item}")
            continue
        text = path.read_text(encoding="utf-8")
        if "CN_OUTPUT_FORMATTING.md" not in text and "中文" not in text:
            err(f"产物格式文件缺少中文格式规则：{item}")


def check_chart_style_contracts() -> None:
    for item, needles in ROOT_CHART_STYLE_CONTRACTS.items():
        path = ROOT / item
        if not path.exists():
            err(f"缺少图表样式合同文件：{item}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                err(f"{item} 缺少图表样式硬规则 `{needle}`")
    for item in CHART_WORKFLOW_FILES:
        path = ROOT / item
        if not path.exists():
            err(f"缺少图表 workflow 文件：{item}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in (
            "柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线",
            "major/minor gridlines",
        ):
            if needle not in text:
                err(f"{item} 缺少图表 workflow Gate `{needle}`")


def check_docx_pagination_contracts() -> None:
    root_docx = ROOT / "CN_DOCX_OUTPUT_CONTRACT.md"
    text = root_docx.read_text(encoding="utf-8")
    for needle in DOCX_PAGINATION_CONTRACT_NEEDLES:
        if needle not in text:
            err(f"{rel(root_docx)} 缺少 DOCX 连续排版规则 `{needle}`")
    for forbidden in DOCX_PAGINATION_FORBIDDEN_TEXT:
        if forbidden in text:
            err(f"{rel(root_docx)} 出现 DOCX 显式分页风险文本 `{forbidden}`")

    for path in (
        ROOT / "skills" / "earnings-analysis" / "SKILL.md",
        ROOT / "skills" / "earnings-analysis" / "references" / "workflow.md",
        ROOT / "skills" / "earnings-analysis" / "references" / "report-structure.md",
    ):
        text = path.read_text(encoding="utf-8")
        for forbidden in DOCX_PAGINATION_FORBIDDEN_TEXT:
            if forbidden in text:
                err(f"{rel(path)} 出现 DOCX 显式分页风险文本 `{forbidden}`")
        for pattern in DOCX_PAGINATION_FORBIDDEN_REGEX:
            if pattern.search(text):
                err(f"{rel(path)} 仍存在逐页结构标题或创建步骤：{pattern.pattern}")
        if "章节应连续排版" not in text and "章节必须连续排版" not in text:
            err(f"{rel(path)} 缺少 earnings-analysis 连续排版说明")


def check_data_gate_wording() -> None:
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for weak in WEAK_DATA_GATE_WORDING:
            if weak in text:
                err(f"发现弱数据查询口径 `{weak}`：{rel(path)}")


def check_reference_linkage() -> None:
    for folder_name in ("references", "reference"):
        for path in sorted(SKILLS.glob(f"*/{folder_name}/*.md")):
            if path.name == "data-query-order.md":
                continue
            text = path.read_text(encoding="utf-8")
            if "Reference 链路：执行本文件前" not in text:
                err(f"既有 reference 文件缺少格式链路提示：{rel(path)}")
            if "DATA_QUERY_ORDER_CN.md" not in text:
                err(f"既有 reference 文件未指向根级数据合同：{rel(path)}")
            if "CN_OUTPUT_FORMATTING.md" not in text and "CN_MARKDOWN_OUTPUT_CONTRACT.md" not in text:
                err(f"既有 reference 文件未指向根级格式合同：{rel(path)}")
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
        if "CN_HTML_OUTPUT_CONTRACT.md" not in text:
            err("earnings-preview-beta/report-template.md 未指向根级 HTML 格式合同")


def check_earnings_analysis_contract() -> None:
    skill = ROOT / "skills" / "earnings-analysis" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    for needle in EARNINGS_ANALYSIS_NEEDLES:
        if needle not in text:
            err(f"earnings-analysis 缺少硬门槛文本：{needle}")


def check_forbidden_and_residual_text() -> None:
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for forbidden in FORBIDDEN_OUTPUT_LABELS:
            if forbidden in text:
                err(f"发现禁止输出标签 `{forbidden}`：{rel(path)}")
        for forbidden in FORBIDDEN_LEGACY_WORDING:
            if forbidden.lower() in text.lower():
                err(f"发现旧英文或旧架构文本 `{forbidden}`：{rel(path)}")
        for forbidden in FORBIDDEN_FONT_WORDING:
            if forbidden in text:
                err(f"发现旧字体口径 `{forbidden}`：{rel(path)}")
        if path.suffix == ".md":
            residual = english_phrase_lines(text)
            if residual:
                err(f"疑似未翻译英文行：{rel(path)}: {residual[0]}")


def main() -> int:
    check_required_docs()
    check_manifest()
    check_no_local_formatting_references()
    check_root_data_query_contract()
    check_root_contract_references()
    check_root_font_contracts()
    check_skills()
    check_artifact_rules()
    check_chart_style_contracts()
    check_docx_pagination_contracts()
    check_data_gate_wording()
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
