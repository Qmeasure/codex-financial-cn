# 中文 DOCX 交付契约

本文件是 `financial-services-cn` 的中文 Word 交付契约。任何技能生成 DOCX、Word 或面向 Google Docs 导入的 `.docx` 文件时，都必须在用户模板和品牌规范之外遵守本契约。用户模板优先，但不得省略中文可读性、来源、币种、单位、日期、口径、免责声明和人工审阅边界。

## 1. 默认 preset

默认中文机构投研/投行 DOCX preset 名称：

```yaml
preset_name: cn_institutional_research_brief
page:
  size: A4
  margins: {top: 1.8cm, right: 1.8cm, bottom: 1.6cm, left: 1.8cm}
  header_distance: 0.8cm
  footer_distance: 0.8cm
typography:
  font_family: Source Han Serif CN
  allowed_weights: [Regular, Bold]
  body: {size: 10.5pt, weight: Regular, line_spacing: 1.20, before: 0pt, after: 3pt}
headings:
  h1: {size: 15pt, weight: Bold, color: "#1F4E5F", line_spacing: 1.15, before: 10pt, after: 6pt}
  h2: {size: 12pt, weight: Bold, color: "#2F5965", line_spacing: 1.15, before: 8pt, after: 4pt}
  h3: {size: 11pt, weight: Bold, color: "#333333", line_spacing: 1.15, before: 6pt, after: 3pt}
tables:
  width: fixed
  header: {size: 8.5pt, weight: Bold, line_spacing: 1.15, fill: "#1F4E5F", font_color: "#FFFFFF"}
  body: {size: 8.5pt, weight: Regular, line_spacing: 1.15}
  cell_margins_dxa: {top: 80, bottom: 80, start: 120, end: 120}
charts:
  internal_source: {size: 7pt, weight: Regular, color: "#666666"}
  caption_below: {pattern: "图表 N：<主题>", size: 9pt, weight: Bold, alignment: center, line_spacing: 1.15, before: 3pt, after: 6pt}
```

该 preset 是本仓库对 Documents skill design preset 的 named override。生成 DOCX 时必须先读取 Documents skill 的 `SKILL.md` 和 `references/design_presets.md`，再把本 preset 的中文金融 token 显式应用到文档实现中。

## 2. 字体与 OOXML

- 唯一指定字体为 `Source Han Serif CN`。正文、标题、表格正文、表头、图表标题、图表内部来源、图表下方编号、脚注和免责声明都必须使用该字体。
- 只允许 Regular 和 Bold 两种字重。正文、表体、来源、免责声明使用 Regular；标题、表头和图表下方编号使用 Bold。
- Word OOXML 中每个主要样式和关键直接格式化 run 必须设置 `w:rFonts`，并且 `w:eastAsia`、`w:ascii`、`w:hAnsi` 都必须等于 `Source Han Serif CN`。不得只设置西文字体。
- 生成或校验前必须确认当前用户环境能解析 `Source Han Serif CN` Regular/Bold；缺少字体时必须先安装官方 `SubsetOTF/CN` 字体文件，不能静默换用其他字体。

## 3. 页面、页眉和页脚

- 中文机构材料默认 A4 纵向页面。
- 页边距默认上 1.8cm、右 1.8cm、下 1.6cm、左 1.8cm；用户模板另有要求时以模板为准。
- 页眉应包含公司名称、股票代码、报告类型、季度和日期中的关键元数据。
- 页脚应包含页码、免责声明短句或材料状态。页码必须是真实 Word 字段或由 DOCX 工具可更新的页码结构，不得用手写静态数字伪装。
- 美股、港股或 ADR 报告必须在页眉或首页元数据区标注交易所、币种、会计准则和数据日期。
- DOCX 章节默认连续排版：H1/H2、章节标题、附录标题和报告 section 不得主动插入显式分页或分节符；只允许 Word 自然分页。
- 只有用户明确要求，或用户提供的 Word 模板本身已有分页/分节设置时，才可保留显式分页或分节；保留原因必须在交付说明中写清楚。

## 4. 中文样式

- 标题必须用中文结论式表达，不使用只有英文名词堆叠的标题。
- 正文默认 10.5pt Regular，行距 1.20，段前 0pt，段后 3pt，两端对齐；不得出现密集英文模板段落。
- 一级标题默认 15pt Bold，行距 1.15，段前 10pt，段后 6pt，颜色 `#1F4E5F`。
- 二级标题默认 12pt Bold，行距 1.15，段前 8pt，段后 4pt，颜色 `#2F5965`。
- 三级标题默认 11pt Bold，行距 1.15，段前 6pt，段后 3pt，颜色 `#333333`。
- 列表正文默认 10.5pt Regular，行距 1.20，段后 2pt；左缩进 0.63cm，悬挂 0.25cm。
- 免责声明默认 7pt Regular，行距 1.10，段前 6pt，段后 0pt，颜色 `#666666`，必须包含“不构成投资、法律、税务、会计或监管建议”和“应由专业人员审阅”含义。

## 5. 表格

- 表格必须使用真实 Word 表格，禁止用空格、制表符或截图伪造表格。
- 表格必须固定宽度，禁止依赖 Word 默认 autofit。
- OOXML 必须包含 `tblGrid`、每列 `gridCol` 和每个单元格 `tcW`；`tblW`、`tblGrid` 和 `tcW` 必须一致。
- 必须设置 cell margin，默认 `top=80`、`bottom=80`、`start=120`、`end=120` DXA。
- 表格标题默认 9pt Bold，行距 1.15，段前 6pt，段后 3pt。
- 表头默认 8.5pt Bold，行距 1.15，底色 `#1F4E5F`，字体白色，水平居中。
- 表体默认 8.5pt Regular，行距 1.15，段前 0pt，段后 0pt；数值右对齐，文本左对齐。
- 表格必须标注币种、单位、期间和来源。预测、估算或未经审计数据必须明确标识。

## 6. 列表

- 禁止 fake bullets：不得用 `•`、`-`、`*`、手写数字或换行文本伪造列表。
- 必须使用 Word numbering definitions。无序列表、编号列表和多级列表都必须有真实 numbering 结构。
- 列表换行后必须与列表正文对齐，不得缩进到 marker 下方。

## 7. 来源、超链接和裸 URL

- 来源必须使用可点击 Word hyperlink，显示文本应为“业绩公告”“10-Q”“港交所公告”“投资者演示材料”等有意义名称。
- 禁止裸 URL 出现在正文、脚注、图表、表格来源和参考资料章节中。
- 如果来源来自订阅数据源且没有公开 URL，必须写明数据源或数据库名称、数据日期；不要输出固定缺口标签。
- SEC 披露优先链接 EDGAR viewer；A股使用交易所公告、巨潮资讯或公司公告页；港股使用披露易、交易所公告或公司 IR 页面。

## 8. 图表

- 图表标题、轴标签、图例、数据标签、注释和来源必须中文化，并使用 `Source Han Serif CN`。
- 每张图表必须在图表内部标注来源和数据日期；图表内部来源固定为 7pt Regular、`#666666`。
- DOCX 中每张图表下方必须居中写明 `图表 N：<主题>`，其中 N 使用真实连续编号，主题必须能概括图表内容。
- `图表 N：<主题>` 默认 9pt Bold，行距 1.15，段前 3pt，段后 6pt。
- 图表下方不得再另写来源小字、来源超链接或多来源清单。完整来源清单放入“数据来源与口径说明”或“参考资料”。
- DOCX 正文、表格单元格、脚注、来源、caption 和超链接显示文本不得出现固定校验标签；正式表格缺失值使用 `—`。
- Exhibit 与 caption 必须保持视觉配对，不能跨页断开后无法判断对应关系。
- 柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线；保留坐标轴、刻度和必要数据标签。除非用户明确要求或图表类型必须依赖网格线，否则不得显示 major/minor gridlines。
- DOCX 中嵌入的 PNG/JPG 图表也必须遵守上述字体、来源、编号和网格线规则；不得因为图表先在 Python、HTML、PPTX 或其他工具中生成而绕过检查。

## 9. 结构校验与视觉 QA

交付 DOCX 前必须完成以下检查：

- 文件存在且路径可访问。
- DOCX zip 结构可打开，核心 XML 可解析。
- `word/styles.xml` 或 `word/document.xml` 中能找到 `w:rFonts`，且 `w:eastAsia`、`w:ascii`、`w:hAnsi` 都等于 `Source Han Serif CN`。
- 表格存在时，`tblGrid`、`tcW` 和 cell margin 存在。
- 列表存在时，`word/numbering.xml` 存在且使用真实 numbering。
- 超链接存在时，`word/_rels/document.xml.rels` 中有 hyperlink relationship。
- 文档 XML 中没有裸 URL。
- 每个图表下方存在 `图表 N：<主题>`，且图表下方不存在来源小字。
- 若 LibreOffice/`soffice` 可用，必须执行 DOCX -> PNG render QA 并逐页检查中文、表格、图表、页眉页脚和图表编号。
- Render QA 必须检查柱状图是否错误显示纵坐标横向网格线，同时检查图例挤压、坐标轴标签、中文字体和图表内部来源。

如果本机缺少 LibreOffice/`soffice`，允许交付结构校验通过的 DOCX，但最终回复必须写明：

```text
未完成 DOCX 视觉渲染 QA：本机缺少 LibreOffice/soffice。
已完成结构校验，但结构校验不能替代视觉验收。
```

不得把 zip/docx 结构校验说成视觉 QA 通过。
