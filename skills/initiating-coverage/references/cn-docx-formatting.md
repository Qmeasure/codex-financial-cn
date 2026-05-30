# 中文 DOCX 格式合同

本文件是本 skill 的本地 DOCX/Word reference。生成正式 DOCX 前必须读取；根级 `../../CN_DOCX_OUTPUT_CONTRACT.md` 仍作为上位标准。

## 页面与字体

- 默认使用 A4 页面，页边距、页眉、页脚和页码按中文机构材料处理。
- DOCX 章节默认连续排版：H1/H2、章节标题、附录标题和报告 section 不得主动插入显式分页或分节符；只允许 Word 自然分页。只有用户明确要求，或用户提供的 Word 模板本身已有分页/分节设置时，才可保留。
- 中文字体优先级：Microsoft YaHei、PingFang SC、Noto Sans CJK SC、Source Han Sans SC、SimSun、Arial Unicode MS fallback。
- Word OOXML 必须设置 `w:rFonts@w:eastAsia`、`w:rFonts@w:ascii`、`w:rFonts@w:hAnsi`。
- 标题、正文、表格、图表标题、来源脚注和免责声明必须使用统一中文样式。

## 表格、列表与来源

- 表格必须使用固定宽度，包含 `tblGrid`、`tcW` 和 cell margin。
- 列表必须使用真实 Word numbering definitions，禁止 fake bullets。
- 来源必须是可点击 hyperlink，禁止在正文裸露 URL。
- 图表标题、轴标签、图例、注释和来源必须中文化。
- Exhibit 下方来源标注必须使用很小字体：默认 6pt，最大不得超过 7pt；覆盖图表、表格、图片、关键数据块和紧邻页面底部的来源行。
- 每个 Exhibit 下方只保留最重要的 1 个来源，必须使用有意义显示文本和可点击 hyperlink；hyperlink run 必须显式设置同一小字号；多来源清单放入“数据来源与口径说明”或“参考资料”，不得在 Exhibit 下方罗列。
- DOCX 正文、表格单元格、脚注、来源、caption 和超链接显示文本不得出现固定校验标签；正式表格缺失值使用 `—`，说明性限制放入“数据来源与口径说明”。


## 图表样式硬规则

- 柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线；保留坐标轴、刻度和必要数据标签。
- 除非用户明确要求或图表类型必须依赖网格线，否则不得显示 major/minor gridlines。
- DOCX 和 PPTX 中嵌入的 PNG/JPG 图表也必须遵守该规则，不得因图表由 Python、HTML、PPTX、DOCX 或其他工具预生成而绕过检查。
- Render QA 必须检查中文字体、图表遮挡、来源、柱状图横向网格线、图例挤压和坐标轴标签。

## 交付与 QA

- 最终回复前必须确认 DOCX 文件已生成、路径存在、可打开或结构校验通过。
- 如 LibreOffice/`soffice` 可用，必须执行 DOCX -> PNG render QA，并检查中文乱码、表格溢出、页眉页脚错位和来源脚注贴边。
- 如无法完成视觉渲染 QA，最终回复必须说明原因；不得把结构校验说成视觉 QA 通过。
- 最终回复必须包含 DOCX 文件路径。
