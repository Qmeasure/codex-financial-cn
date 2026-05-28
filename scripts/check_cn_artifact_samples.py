#!/usr/bin/env python3
"""Generate and inspect representative Chinese artifact samples."""
from __future__ import annotations

import sys
import zipfile
import xml.etree.ElementTree as ET
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

docx = OUT / "cn_acceptance_sample.docx"
content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>
"""
package_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""
styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="正文"/>
    <w:rPr>
      <w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/>
      <w:sz w:val="21"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="标题 1"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/>
      <w:b/>
      <w:color w:val="1F4E5F"/>
      <w:sz w:val="30"/>
    </w:rPr>
  </w:style>
</w:styles>
"""
numbering_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="1">
    <w:multiLevelType w:val="singleLevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>
      <w:lvlText w:val="%1."/>
      <w:lvlJc w:val="left"/>
      <w:pPr>
        <w:ind w:left="420" w:hanging="240"/>
      </w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="1"/>
  </w:num>
</w:numbering>
"""
document_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdSource" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="https://example.com/announcement" TargetMode="External"/>
</Relationships>
"""
document_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    <w:p>
      <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
      <w:r>
        <w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr>
        <w:t>A股优先业绩更新报告</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr>
        <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
      </w:pPr>
      <w:r>
        <w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr>
        <w:t>收入同比增长，毛利率需结合公告口径复核。</w:t>
      </w:r>
    </w:p>
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="9000" w:type="dxa"/>
        <w:tblLayout w:type="fixed"/>
        <w:tblCellMar>
          <w:top w:w="80" w:type="dxa"/>
          <w:left w:w="120" w:type="dxa"/>
          <w:bottom w:w="80" w:type="dxa"/>
          <w:right w:w="120" w:type="dxa"/>
        </w:tblCellMar>
      </w:tblPr>
      <w:tblGrid>
        <w:gridCol w:w="3000"/>
        <w:gridCol w:w="3000"/>
        <w:gridCol w:w="3000"/>
      </w:tblGrid>
      <w:tr>
        <w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr><w:t>指标</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr><w:t>本期</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr><w:t>来源</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr><w:t>收入（人民币亿元）</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr><w:t>125.4</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/></w:tcPr><w:p><w:r><w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr><w:t>数据来源：交易所公告</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>
    <w:p>
      <w:r>
        <w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr>
        <w:t>来源链接：</w:t>
      </w:r>
      <w:hyperlink r:id="rIdSource">
        <w:r>
          <w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/><w:u w:val="single"/><w:color w:val="0563C1"/></w:rPr>
          <w:t>交易所公告</w:t>
        </w:r>
      </w:hyperlink>
    </w:p>
    <w:p>
      <w:r>
        <w:rPr><w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/></w:rPr>
        <w:t>免责声明：本材料不构成投资建议，需人工复核。</w:t>
      </w:r>
    </w:p>
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1021" w:right="1021" w:bottom="907" w:left="1021" w:header="454" w:footer="454" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"""

with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("[Content_Types].xml", content_types)
    zf.writestr("_rels/.rels", package_rels)
    zf.writestr("word/document.xml", document_xml)
    zf.writestr("word/styles.xml", styles_xml)
    zf.writestr("word/numbering.xml", numbering_xml)
    zf.writestr("word/_rels/document.xml.rels", document_rels)

with zipfile.ZipFile(docx) as zf:
    names = set(zf.namelist())
    required_parts = {
        "word/document.xml",
        "word/styles.xml",
        "word/numbering.xml",
        "word/_rels/document.xml.rels",
    }
    missing = sorted(required_parts - names)
    if missing:
        fail(f"docx missing parts: {', '.join(missing)}")
    doc_xml = zf.read("word/document.xml").decode("utf-8")
    style_xml = zf.read("word/styles.xml").decode("utf-8")
    num_xml = zf.read("word/numbering.xml").decode("utf-8")
    rel_xml = zf.read("word/_rels/document.xml.rels").decode("utf-8")

for needle in (
    'w:eastAsia="Microsoft YaHei"',
    'w:ascii="Microsoft YaHei"',
    'w:hAnsi="Microsoft YaHei"',
):
    if needle not in doc_xml or needle not in style_xml:
        fail(f"docx font attribute missing {needle}")
for needle in ("<w:tblGrid>", "<w:tcW ", "<w:tblCellMar>"):
    if needle not in doc_xml:
        fail(f"docx table geometry missing {needle}")
if "<w:numPr>" not in doc_xml or "<w:abstractNum " not in num_xml or "<w:num " not in num_xml:
    fail("docx real numbering definitions missing")
doc_visible_text = "".join(ET.fromstring(doc_xml).itertext())
if "•" in doc_visible_text or "http://" in doc_visible_text or "https://" in doc_visible_text:
    fail("docx visible body text contains fake bullet or bare URL")
if 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"' not in rel_xml:
    fail("docx hyperlink relationship missing")
if 'Target="https://example.com/announcement"' not in rel_xml or 'TargetMode="External"' not in rel_xml:
    fail("docx hyperlink target missing or not external")
for needle in ("交易所公告", "数据来源", "免责声明"):
    if needle not in doc_xml:
        fail(f"docx Chinese content missing {needle}")

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

print("OK — generated and inspected CN XLSX/PPTX/DOCX/Markdown artifact samples.")
