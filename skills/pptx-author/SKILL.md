---
name: pptx-author
description: 在磁盘生成 .pptx 文件（无界面），而不是驱动实时 PowerPoint 文档；用于没有打开 Office 应用的托管代理会话。
---

## 中文版执行契约

- 默认使用中国大陆金融语境：A股优先，港股和美股兼容；如用户指定市场、币种、会计准则或模板，以用户输入为准。
- 数据来源必须遵守插件根目录 `../../DATA_SOURCES_CN.md`：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断缺少依据时不得下结论，只在数据源发现记录中列为未覆盖数据项。
- 所有产物必须遵守插件根目录 `../../CN_OUTPUT_FORMATTING.md`：`Source Han Serif CN`、中文日期、币种/单位、图表标题、表格表头、来源、风险提示和免责声明都要按中文机构材料处理。
- 用户模板和品牌规范优先，但不得突破中文可读性、来源脚注、币种/单位/日期/口径说明这些底线。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。


## 产物合同读取与输出门槛

生成正式输出前必须读取：
- 插件根目录 `../../DATA_SOURCES_CN.md`
- 插件根目录 `../../CN_OUTPUT_FORMATTING.md`
- 插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`
- 插件根目录 `../../CN_PPTX_OUTPUT_CONTRACT.md`（当输出 PPTX/PowerPoint 文件时）
- 插件根目录 `../../DATA_QUERY_ORDER_CN.md`（当任务需要外部数据查询、行情更新、财报抓取、行业/公司/宏观/监管材料检索时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、数据缺口和人工审阅边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 若本 skill 的既有输出包含 PPTX/PowerPoint 文件，最终回复前必须确认 PPTX 文件已生成、PPTX 文件路径存在、可打开或结构校验通过，并确保最终回复包含 PPTX 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `../../DATA_QUERY_ORDER_CN.md`，先生成“数据源发现记录”，列出可用/不可用 MCP、connector、授权源和用户文件；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物。若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须遵守插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`，并包含来源、口径限制、数据缺口和人工审阅边界。
- 生成或审查图表时，必须遵守插件根目录对应产物合同；柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线，除非用户明确要求或图表类型必须依赖网格线，否则不得显示 major/minor gridlines。


# pptx-author（PPTX 作者）

当处于**无界面**运行环境，且需要交付一份 PowerPoint 材料作为**文件产物**，而不是通过 `mcp__office__powerpoint_*` 编辑实时文档时，使用本 skill。

## 输出契约

- 写入 `./out/<name>.pptx`。如果 `./out/` 不存在，则创建该目录。
- 在最终消息中返回相对路径，便于编排层收集产物。

## 构建材料

编写一个简短 Python 脚本并用 Bash 运行。使用 `python-pptx`：

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation("./templates/firm-template.pptx")  # 如果提供了模板
# or: prs = Presentation()

slide = prs.slides.add_slide(prs.slide_layouts[5])    # title-only
slide.shapes.title.text = "估值摘要"
# ... add tables / charts / text boxes ...

prs.save("./out/pitch-<target>.pptx")
```

## 约定（对齐实时 Office 的 `pitch-deck` skill）

- **每页一个观点。** 标题表达结论，正文支撑该结论。
- **每个数字都能追溯到模型。** 如果数字来自 `./out/model.xlsx`，脚注应标明工作表和单元格。
- **优先使用机构模板。** 如果 `./templates/` 下挂载了模板，则使用该模板；否则使用默认版式。
- **图表。** 当保真度重要时，优先嵌入由模型渲染的 PNG，而不是使用原生 pptx 图表。
- **不做外部发送。** 本 skill 只写入文件，不发送邮件，也不上传。

## 不适用场景

如果 `mcp__office__powerpoint_*` 工具可用，优先使用这些工具；它们会驱动用户的实时文档并保留审阅节点。本 skill 是无界面运行时的文件生成 fallback。
