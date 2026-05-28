# Financial Services CN

面向中国大陆投资者和机构金融工作流的中文 Codex 金融服务插件。它参考 `anthropics/financial-services` 的 README 信息架构，并按本仓库实际能力改写：A 股优先，兼容港股和美股，覆盖建模、估值、投行材料、权益研究、私募股权、财富管理、基金运营、KYC、LSEG 和 S&P Global 数据工作流。

> [!IMPORTANT]
> 本仓库不构成投资、法律、税务、会计或监管建议。所有技能只用于辅助起草分析材料、模型、备忘录、研究笔记、核对表、报告包和演示材料，输出必须由具备资质的专业人员复核。技能不会作出投资建议、执行交易、绑定风险、入账、批准客户准入或对外分发材料。

## 安装到 Codex

Codex 插件需要先来自一个已配置的 marketplace，再通过插件名安装。本仓库根目录是插件源，不是 marketplace 根目录；不要把普通插件目录直接传给 `codex plugin add`。

### 从已发布 marketplace 安装

如果插件已经发布到某个 marketplace，按以下顺序安装：

```bash
codex plugin marketplace add <marketplace-source>
codex plugin list --marketplace <marketplace-name>
codex plugin add financial-services-cn@<marketplace-name>
```

其中：

- `<marketplace-source>` 可以是本地 marketplace 路径、`owner/repo[@ref]`、HTTPS Git URL 或 SSH Git URL。
- `<marketplace-name>` 是 marketplace manifest 中声明的名称；先用 `codex plugin list --marketplace <marketplace-name>` 确认能看到 `financial-services-cn`。
- `codex plugin add` 的选择器必须是 `PLUGIN@MARKETPLACE`，也可以写成 `codex plugin add PLUGIN --marketplace MARKETPLACE`。

安装后，建议开启一个新 Codex 线程，让 Codex 重新加载插件技能和 MCP 配置。

### 本地 checkout 开发安装

本仓库当前保持“根目录就是插件源”的形态。做本地开发安装时，不要在本仓库内新增 marketplace 包装层；应让你的个人 marketplace 指向这个 checkout。

推荐做法：

1. 将本仓库 checkout 以 `financial-services-cn` 这个目录名放入或链接到你的个人插件目录。
2. 在个人 marketplace 文件中新增或合并一个 entry，entry 名称为 `financial-services-cn`，本地 source 指向上一步的 checkout，安装策略为可安装，认证策略为安装时确认，类别为 `Finance`。
3. 运行：

```bash
codex plugin add financial-services-cn@personal
```

如果你使用的不是默认个人 marketplace，而是团队或仓库级 marketplace，则先将该 marketplace 根目录加入 Codex：

```bash
codex plugin marketplace add <marketplace-source>
codex plugin list --marketplace <marketplace-name>
codex plugin add financial-services-cn@<marketplace-name>
```

## 仓库里有什么

- **一个 Codex 插件**：根级 `.codex-plugin/plugin.json` 声明 `financial-services-cn`。
- **66 个扁平技能**：所有 source skills 直接位于 `skills` 目录，每个技能目录包含 `SKILL.md`。
- **根级 MCP 配置**：`.mcp.json` 集中声明机构数据源和中国市场相关入口。
- **中文金融规则文档**：`DATA_SOURCES_CN.md` 规定数据来源优先级，`CN_OUTPUT_FORMATTING.md` 规定中文金融产物格式。
- **校验脚本**：`scripts` 目录提供结构检查、中文化门禁、中文产物样例检查和版本辅助脚本。

本仓库不内置旧式多插件包装层、独立代理包、显式动作入口或托管代理模板。安装、使用和维护都围绕 `financial-services-cn` 进行。

## 仓库结构

```text
.codex-plugin/plugin.json      Codex 插件 manifest
.mcp.json                      MCP server 配置入口
skills                         66 个中文金融技能
scripts                        结构校验、中文化门禁和产物样例校验
DATA_SOURCES_CN.md             中国市场数据来源规则
CN_OUTPUT_FORMATTING.md        中文金融产物格式规则
OPTIONAL_MCP_TEMPLATES.md      可选 MCP 接入说明
ACCEPTANCE_SAMPLES_CN.md       中文产物验收样例
THIRD_PARTY_NOTICES.md         第三方许可说明
```

## 如何使用

安装后，在 Codex 中用自然语言描述任务即可触发相关技能，例如：

- “按 A 股优先口径分析这家公司，并标注港股和美股可比口径。”
- “把这些披露材料整理成中文投研或投行交付物，补充来源脚注和风险提示。”
- “使用已授权数据源生成中文金融模型、表格或演示材料，并说明币种、单位、日期和口径。”

所有输出默认遵守：

- A 股优先，港股和美股兼容。
- 官方披露、用户文件和已授权数据源优先。
- 监管、会计、KYC、基金文件、月结和客户适当性判断缺少依据时写“需确认”。
- DOCX、PPTX、XLSX、Markdown、表格、图表、脚注和最终摘要必须使用中文金融语境。
- DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写保留。

## 它们如何配合

| 组成 | 作用 | 位置 |
|---|---|---|
| 插件 manifest | 声明插件名称、版本、展示信息、技能目录和 MCP 配置入口 | `.codex-plugin/plugin.json` |
| 技能 | 写入金融领域方法、执行步骤、产物要求和中文执行契约 | `skills` |
| MCP servers | 将 Codex 连接到机构数据源、中国市场工具或本地数据服务 | `.mcp.json` |
| 数据来源规则 | 约束来源优先级、授权判断、缺失依据时的“需确认”表达 | `DATA_SOURCES_CN.md` |
| 中文产物规则 | 约束中文字体、日期、币种、单位、表格、图表、免责声明和摘要 | `CN_OUTPUT_FORMATTING.md` |
| 校验脚本 | 防止旧架构残留、英文模板残留、manifest 错误和中文产物样例退化 | `scripts` |

## 技能领域

| 领域 | 能力摘要 |
|---|---|
| 金融分析 | DCF、LBO、三表模型、可比公司、Excel 审计、PPT 质检、数据清洗 |
| 投资银行 | CIM、teaser、买方名单、并购模型、流程函、交易跟踪、数据包和 pitch deck 填充 |
| 权益研究 | 业绩分析、业绩预览、首次覆盖、模型更新、晨会纪要、行业报告、催化剂跟踪 |
| 私募股权 | 项目来源、项目筛选、尽调清单、尽调会议准备、投委会备忘录、组合监控、价值创造计划 |
| 财富管理 | 客户回顾、财务规划、投资建议书、组合再平衡、客户报告、税损收割 |
| 基金运营 | 总账对账、差异追踪、预提明细、滚动表、NAV 勾稽、波动说明 |
| KYC 与运营 | KYC 文件解析、KYC/AML 规则评估、缺失项和升级事项标记 |
| LSEG 数据工作流 | 债券相对价值、期货基差、掉期曲线、外汇套息、期权波动率、固收组合、宏观利率监控 |
| S&P Global 数据工作流 | 公司速览、融资摘要、业绩预览和 Capital IQ 相关材料 |

## MCP 集成

`.mcp.json` 当前声明以下 MCP 入口。实际可用性取决于用户本地环境、账号、token、订阅和数据授权；无法确认时，技能必须写“需确认”。

| 名称 | 类型 | 入口 |
|---|---|---|
| `daloopa` | 机构数据源 | `https://mcp.daloopa.com/server/mcp` |
| `morningstar` | 机构数据源 | `https://mcp.morningstar.com/mcp` |
| `sp-global` | S&P Global / Kensho | `https://kfinance.kensho.com/integrations/mcp` |
| `factset` | 机构数据源 | `https://mcp.factset.com/mcp` |
| `moodys` | Moody's 数据源 | `https://api.moodys.com/genai-ready-data/m1/mcp` |
| `mtnewswire` | 新闻数据源 | `https://vast-mcp.blueskyapi.com/mtnewswires` |
| `aiera` | 会议和文字稿数据源 | `https://mcp-pub.aiera.com` |
| `lseg` | LSEG 分析入口 | `https://api.analytics.lseg.com/lfa/mcp` |
| `lseg-server-cl` | LSEG server-cl 入口 | `https://api.analytics.lseg.com/lfa/mcp/server-cl` |
| `pitchbook` | PitchBook 数据源 | `https://premium.mcp.pitchbook.com/mcp` |
| `chronograph` | Chronograph 数据源 | `https://ai.chronograph.pe/mcp` |
| `egnyte` | 文档数据源 | `https://mcp-server.egnyte.com/mcp` |
| `openbb-cn-market` | 本地中国市场工具 | `http://127.0.0.1:8001/mcp` |
| `tushare-pro` | 本地 Tushare Pro 工具 | `python -m tushare_mcp_server.main`，通过 `TUSHARE_TOKEN` 读取 token |
| `akshare-one` | 本地 AKShare 工具 | `uvx akshare-one-mcp` |

机构数据源通常需要订阅或 API key。OpenBB、Tushare 和 AKShare 相关入口只在用户确认本地服务、依赖和授权可用后使用。

## 中国大陆投资者优化

- **A 股优先**：未指定市场时，默认按 A 股公司、人民币、A 股交易日、交易所公告和中国会计语境处理。
- **跨市场可比**：涉及港股、美股或 ADR 时，必须标注交易所、币种、会计准则、数据日期、汇率来源和是否统一口径。
- **中文产物格式**：中文标题、表头、脚注、图例、来源说明和免责声明不得沿用英文默认版式。
- **来源可追溯**：每个关键结论应能追溯到用户文件、官方披露、MCP/数据库名称、公告日期、数据日期或页码。
- **谨慎边界**：缺少官方材料、用户政策或授权数据支持的监管、会计、KYC、税务、基金运营和客户适当性判断，一律写“需确认”。

## Making It Yours

这些技能是中文金融工作流模板。落地到具体机构时，建议按以下方式调整：

- **替换数据源**：将 `.mcp.json` 指向你有授权的数据平台、内部数据库或本地市场数据服务。
- **加入机构语境**：把公司术语、投资标准、KYC 政策、审批流程和材料规范写进相关技能。
- **带入模板**：用用户提供的 PPT、Excel、DOCX 模板约束版式，但保留中文来源脚注、币种、单位和免责声明。
- **调整技能边界**：只扩展真实需要的工作流，不引入与本仓库单插件形态冲突的旧架构入口。
- **保留审计链**：模型、报告和演示材料必须说明数据来源、口径限制和待人工复核事项。

## 本地开发与校验

修改本仓库后，至少运行：

```bash
python3 scripts/check.py
python3 scripts/check_cn_localization.py
python3 scripts/check_cn_artifact_samples.py
python3 /Users/lesterbot/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

这些检查会覆盖：

- 根级 Codex manifest、MCP 配置和技能目录结构。
- 禁止的旧架构目录或文本残留。
- 中文化门禁、中文金融规则引用和英文模板残留。
- XLSX、PPTX、Markdown 中文产物样例。
- Codex 插件 manifest schema。

如果 `python3 scripts/check_cn_artifact_samples.py` 因本机缺少 `python-pptx` 或 `openpyxl` 失败，可以在临时 venv 中安装这两个包后重跑该脚本；不要为了跑样例检查而把临时依赖写进仓库。

## 贡献规则

- 新增或改写技能时，必须包含“中文版执行契约”，并引用 `DATA_SOURCES_CN.md` 和 `CN_OUTPUT_FORMATTING.md`。
- 不修改技能目录名、schema key、环境变量名、MCP server 名称或既有 URL，除非同时说明迁移方案。
- 不默认启用付费源、机构源或本地 MCP；需要用户确认授权和可用性。
- 不使用 LiteLLM 或外部翻译 API 做本仓库中文化。
- 不引入旧多插件包装层、独立代理包、显式动作入口或托管代理模板。
- 改完必须运行结构检查、中文化门禁、中文产物样例检查和 Codex manifest 校验。

## 许可证

仓库根目录遵守 [`LICENSE`](./LICENSE)。部分 S&P Global/Kensho 技能保留原 Apache 2.0 许可文件，详见 [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)。
