# 第三方许可和数据源说明

本仓库根目录遵守 `LICENSE`。部分技能来自或适配自第三方伙伴示例，保留其原始许可文件和数据授权要求。

## S&P Global / Kensho

- `skills/earnings-preview-beta/`
- `skills/funding-digest/`
- `skills/tear-sheet/`

以上目录内保留原 Apache 2.0 许可文件。相关技能按现状提供，不保证生成输出或数据一定正确，必须由专业人员核验。

使用 S&P Global 数据前，用户必须确认已拥有 Capital IQ Pro、S&P Global LLM-ready API 或其他相应授权。通过 MCP 连接时，只能使用用户已授权的服务。

## LSEG

LSEG 相关技能面向债券、利率曲线、外汇、期权、固定收益组合和宏观利率分析场景。使用前必须确认用户拥有有效 LSEG 数据授权，并在产物中标注数据来源、日期、币种、单位和口径。

## 国内市场数据源

`openbb-cn-market`、`tushare-pro` 和 `akshare-one` 只作为可选 MCP 配置入口。使用前必须确认安装来源、许可证、token、数据授权、频率限制和字段口径。免费或第三方公开源只作辅助，不得替代官方披露、用户文件或已授权数据库。
