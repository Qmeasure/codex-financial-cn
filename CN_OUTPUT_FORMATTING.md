# 中文金融产物格式规则

所有通过本仓库技能、代理或命令生成的 XLSX、PPTX、DOCX、Markdown、HTML、表格、图表、脚注和最终摘要必须遵守本文件。更细的文件类型规则见同目录的 `CN_DOCX_OUTPUT_CONTRACT.md`、`CN_XLSX_OUTPUT_CONTRACT.md`、`CN_PPTX_OUTPUT_CONTRACT.md`、`CN_MARKDOWN_OUTPUT_CONTRACT.md`、`CN_HTML_OUTPUT_CONTRACT.md` 和 `CN_CHART_OUTPUT_CONTRACT.md`。

## 1. 默认风格

- 默认采用中国大陆机构投研/投行材料风格：克制、清晰、可审计，避免英文模板残留。
- 用户提供的公司模板、品牌规范和版式优先；但中文可读性、来源、币种/单位/日期/口径说明和免责声明不得省略。
- 不使用外部翻译 API。中文表述由模型自身能力完成。

## 2. 字体与排版

- 唯一指定字体为 `Source Han Serif CN`（思源宋体 CN）。DOCX、PPTX、XLSX、HTML、图表图片和导出 PDF 都必须使用该字体。
- 仅使用 Regular 和 Bold 两种字重：正文、表体、来源、注释和免责声明使用 Regular；标题、表头、图表下方编号和需要强调的关键标签使用 Bold。
- 不提供多字体选项，不使用替代字体口径。生成或校验前若当前用户环境缺少 `Source Han Serif CN` Regular/Bold，必须先安装字体或明确标记主交付物未完成。
- 字体来源固定为 Adobe Source Han Serif 官方仓库：`https://github.com/adobe-fonts/source-han-serif`；安装文件固定使用 `SubsetOTF/CN/SourceHanSerifCN-Regular.otf` 和 `SubsetOTF/CN/SourceHanSerifCN-Bold.otf`。
- HTML 使用在线 CDN 定义字体，font-family 仍固定为 `Source Han Serif CN`。

## 3. 日期、币种和单位

- 日期默认格式：`YYYY年M月D日` 或 `YYYY-MM-DD`，同一产物内保持一致。
- A股默认人民币，单位优先“万元/亿元”；港股默认港元；美股默认美元。
- 跨市场比较必须显式标注币种、汇率、折算日期、会计准则和数据日期。
- 不默认强制折算成人民币；用户要求折算时必须写明汇率来源和日期。

## 4. 表格和模型

- 中文表头必须清楚标注指标、期间、币种和单位，例如“收入（人民币百万元）”“EV/EBITDA（倍）”。
- Excel 输入值使用蓝色字体，公式使用黑色字体，跨表/外链使用绿色字体；派生值不得硬编码。
- 每个模型必须包含来源/假设区和检查区；检查失败必须以中文说明原因和数据缺口。
- 负数默认使用括号；百分比保留 1 位小数；倍数保留 1 位小数并使用“x”或“倍”，同一产物内一致。
- 表格字体、行高、行距和对齐方式必须遵守对应文件类型合同；不得只靠默认 Office 自动样式。

## 5. PPT 和图表

- 每页只表达一个核心结论，标题用中文陈述结论，不使用只有名词堆叠的英文标题。
- 图表标题、轴标签、图例、数据标签、注释和来源必须中文化，并使用 `Source Han Serif CN`。
- 图表必须在图表内部标注数据日期和来源；涉及估算、预测或未经审计数据时必须标注“估算”“预测”或“未经审计”。
- DOCX 中图表下方只允许居中标注 `图表 N：<主题>`，不得再在图表下方另写来源小字。来源信息必须进入图表内部或“数据来源与口径说明”。
- 图表内部来源固定为 7pt Regular、`#666666`，只保留最重要来源和数据日期；多来源清单放入“数据来源与口径说明”或参考资料。
- 正式产物的正文、表格、脚注、来源、caption 和超链接显示文本不得出现固定校验标签；正式表格缺失值显示 `—`，说明性限制放入“数据来源与口径说明”。
- 柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线；保留坐标轴、刻度和必要数据标签。除非用户明确要求或图表类型必须依赖网格线，否则不得显示 major/minor gridlines。
- 表格必须使用真正的表格对象或可审计的 Excel 区域，不得用空格/制表符伪造表格。

## 6. DOCX、PPTX、XLSX、HTML、Markdown 和最终摘要

- 报告结构默认为：摘要、关键结论、数据来源与口径、正文分析、风险与数据缺口、免责声明。
- 投委会、研究、KYC、财富管理和 LP 报告必须使用中文章节名和中文风险提示。
- DOCX 主交付物必须遵守 `CN_DOCX_OUTPUT_CONTRACT.md`，落实 `Source Han Serif CN`、OOXML 字体属性、表格几何、真实编号、图表编号和可用的 render QA。
- XLSX、PPTX、Markdown、HTML 和独立图表主交付物必须分别遵守 `CN_XLSX_OUTPUT_CONTRACT.md`、`CN_PPTX_OUTPUT_CONTRACT.md`、`CN_MARKDOWN_OUTPUT_CONTRACT.md`、`CN_HTML_OUTPUT_CONTRACT.md` 和 `CN_CHART_OUTPUT_CONTRACT.md`。
- 最终摘要不得只返回英文文件路径或英文状态；必须说明产物内容、数据来源、口径限制和主要未覆盖数据项。

## 7. 免责声明

默认免责声明：

> 本材料由 Codex 金融服务（中国版）辅助生成，仅供具备资质的专业人员审阅和进一步核验，不构成投资、法律、税务、会计或监管建议。任何交易、签批、入账、客户准入或对外分发均需由授权人员独立审阅并批准。
