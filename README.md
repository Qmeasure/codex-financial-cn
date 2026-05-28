# Financial Services CN

这是一个 Superpowers 风格的单一 Codex 插件，基于 `anthropics/financial-services` 重建为中文金融服务技能集合。仓库根目录本身就是插件源，默认面向中国大陆投资者和机构金融工作流，A 股优先，兼容港股和美股。

> [!IMPORTANT]
> 本仓库不构成投资、法律、税务、会计或监管建议。所有技能只用于起草分析材料、模型、备忘录、研究笔记、核对表和报告包，输出必须由具备资质的专业人员复核。技能不会作出投资建议、执行交易、绑定风险、入账、批准客户准入或对外分发材料。

## 中国大陆投资者优化

- **A 股优先，港股和美股兼容**：未指定市场时默认按 A 股语境处理；跨市场比较必须标注交易所、币种、会计准则、数据日期和来源。
- **中文产物格式**：所有 XLSX、PPTX、DOCX、Markdown、表格、图表、脚注和最终摘要必须遵守 [`CN_OUTPUT_FORMATTING.md`](./CN_OUTPUT_FORMATTING.md)。
- **数据来源分层**：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断无依据时写“需确认”。详见 [`DATA_SOURCES_CN.md`](./DATA_SOURCES_CN.md)。
- **国内市场 MCP 适配**：根级 [` .mcp.json`](./.mcp.json) 保留机构数据源入口，并加入 OpenBB、Tushare、AKShare 等 A 股/港股相关 MCP 配置。实际调用取决于用户本地安装、token 和授权。详见 [`OPTIONAL_MCP_TEMPLATES.md`](./OPTIONAL_MCP_TEMPLATES.md)。
- **专业缩写保留**：DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等保留原缩写并用中文解释。

## 仓库结构

```text
.codex-plugin/plugin.json   # Codex 插件 manifest
.mcp.json                   # 根级 MCP 配置入口
skills/                     # 66 个扁平化金融技能
scripts/                    # 结构校验、中文化门禁和产物样例校验
```

本仓库不再内置多插件市场包装。发布或本地安装时，由外部 Codex marketplace 指向本仓库根目录；仓库内只保留单插件结构。

## 安装与开发

如果本仓库已经由外部 marketplace 发布或登记，安装方式为：

```bash
codex plugin add financial-services-cn@<marketplace-name>
```

本地开发时先校验根插件：

```bash
python3 scripts/check.py
python3 scripts/check_cn_localization.py
python3 scripts/check_cn_artifact_samples.py
python3 /Users/lesterbot/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

如需本地 marketplace 包装，应在仓库外创建 marketplace 配置指向本仓库根目录，不要把包装层放回本仓库。

## 技能范围

| 领域 | 能力 |
|---|---|
| 金融分析 | DCF、LBO、三表、可比公司、Excel 审计、PPT 质检 |
| 投资银行 | CIM、teaser、买方名单、并购模型、流程信函、交易跟踪 |
| 权益研究 | 业绩分析、首次覆盖、模型更新、晨会、行业报告和催化剂跟踪 |
| 私募股权 | 项目来源、筛选、尽调、投委会备忘录、组合监控和价值创造计划 |
| 财富管理 | 客户回顾、财富规划、投资建议书、再平衡和客户报告 |
| 基金运营 | 总账核对、差异追踪、应计、滚动表、NAV 勾稽和差异说明 |
| 金融运营 | KYC 文件解析和规则网格评估 |
| LSEG | 债券、外汇、掉期、期权、固定收益组合和宏观利率分析 |
| S&P Global | 公司速览、融资摘要和业绩预览 |

## 使用原则

- 用自然语言调用技能，不使用旧平台命令入口。
- 用户模板优先，但不得覆盖中文可读性、字体 fallback、来源脚注、币种/单位/日期/口径说明。
- 跨市场材料必须显式标注币种、汇率、会计准则、交易所、披露来源和数据日期。
- A 股默认使用人民币、万元/亿元；港股默认使用港元；美股默认使用美元；除非用户要求，不默认强制折算。
- 没有官方披露、用户文件或授权数据来源支撑的判断必须写“需确认”。

## 数据与授权

- 机构数据源包括 Daloopa、Morningstar、S&P Global、FactSet、Moody's、MT Newswires、Aiera、LSEG、PitchBook、Chronograph 和 Egnyte。
- 国内市场入口包括 `openbb-cn-market`、`tushare-pro` 和 `akshare-one`。
- LSEG 工作流需要用户拥有有效 LSEG 数据授权。
- S&P Global 工作流需要用户拥有 Capital IQ Pro、S&P Global LLM-ready API 或其他相应授权。
- 免费或第三方公开源只作辅助；监管、会计、KYC、基金文件和月结判断不得只依赖免费源。

## 校验

本仓库应通过：

```bash
python3 scripts/check.py
python3 scripts/check_cn_localization.py
python3 scripts/check_cn_artifact_samples.py
python3 /Users/lesterbot/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

`scripts/check.py` 会校验根级 Codex manifest、根级 MCP、技能目录、禁止的旧架构残留和关键文档引用。

## 许可证

仓库根目录遵守 [`LICENSE`](./LICENSE)。部分 S&P Global/Kensho 技能保留原 Apache 2.0 许可文件，详见 [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)。
