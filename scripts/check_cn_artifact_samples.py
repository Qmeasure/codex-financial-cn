#!/usr/bin/env python3
"""Generate and inspect representative Chinese artifact samples."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font
except Exception as exc:  # pragma: no cover
    print(f"requires openpyxl: {exc}", file=sys.stderr)
    sys.exit(2)

try:
    from pptx import Presentation
    from pptx.util import Pt
except Exception as exc:  # pragma: no cover
    print(f"requires python-pptx: {exc}", file=sys.stderr)
    sys.exit(2)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


xlsx = OUT / "cn_acceptance_sample.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "可比公司"
ws["A1"] = "A股优先可比公司分析"
ws["A1"].font = Font(name="Microsoft YaHei", bold=True)
ws["A3"] = "公司"
ws["B3"] = "收入（人民币亿元）"
ws["C3"] = "EV/EBITDA（倍）"
ws["D3"] = "来源"
for cell in ws[3]:
    cell.font = Font(name="Microsoft YaHei", bold=True)
ws["A4"] = "示例股份（600000.SH）"
ws["B4"] = 125.4
ws["C4"] = "=B4/10"
ws["D4"] = "交易所公告，2026年5月27日"
ws["B4"].number_format = '¥#,##0.0"亿"'
ws["C4"].number_format = '0.0x'
ws["A6"] = "免责声明：本样例不构成投资建议，需人工复核。"
ws["A6"].font = Font(name="Microsoft YaHei")
wb.save(xlsx)

loaded = load_workbook(xlsx, data_only=False)
ws = loaded["可比公司"]
if "人民币亿元" not in ws["B3"].value:
    fail("xlsx unit header missing Chinese RMB unit")
if ws["C4"].data_type != "f":
    fail("xlsx formula cell is not a formula")
if "投资建议" not in ws["A6"].value:
    fail("xlsx disclaimer missing")

pptx = OUT / "cn_acceptance_sample.pptx"
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])
title = slide.shapes.title
title.text = "A股优先估值摘要"
title.text_frame.paragraphs[0].runs[0].font.name = "Microsoft YaHei"
title.text_frame.paragraphs[0].runs[0].font.size = Pt(28)
box = slide.shapes.add_textbox(left=914400, top=1828800, width=7315200, height=1828800)
tf = box.text_frame
tf.text = "来源：交易所公告；币种：人民币；单位：亿元；需人工复核。"
tf.paragraphs[0].runs[0].font.name = "Microsoft YaHei"
prs.save(pptx)

prs2 = Presentation(pptx)
texts = "\n".join(shape.text for slide in prs2.slides for shape in slide.shapes if hasattr(shape, "text"))
if "A股优先估值摘要" not in texts:
    fail("pptx title missing Chinese text")
if "来源" not in texts or "人民币" not in texts:
    fail("pptx source or currency note missing")

md = OUT / "cn_acceptance_sample.md"
md.write_text(
    "# 中文研究摘要\n\n"
    "数据来源：交易所公告，2026年5月27日。\n\n"
    "币种与单位：人民币亿元。\n\n"
    "风险提示：本材料不构成投资建议，需人工复核。\n"
)
text = md.read_text()
for needle in ("数据来源", "人民币亿元", "不构成投资建议"):
    if needle not in text:
        fail(f"markdown sample missing {needle}")

print("OK — generated and inspected CN XLSX/PPTX/Markdown artifact samples.")
