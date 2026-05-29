---
name: nav-tieout
description: 将 LP statement 与基金 NAV pack 勾稽：基于 NAV 组成重新计算 LP 资本账户，并标记任何不一致行。用于 LP statement 分发前。
---

## 中文版执行契约

- 默认使用中国大陆金融语境：A股优先，港股和美股兼容；如用户指定市场、币种、会计准则或模板，以用户输入为准。
- 数据来源必须遵守插件根目录 `../../DATA_SOURCES_CN.md`：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断无依据时写“需确认”。
- 所有产物必须遵守插件根目录 `../../CN_OUTPUT_FORMATTING.md`：中文字体栈、中文日期、币种/单位、图表标题、表格表头、来源脚注、风险提示和免责声明都要按中文机构材料处理。
- 用户模板和品牌规范优先，但不得突破中文可读性、来源脚注、币种/单位/日期/口径说明这些底线。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。


## 产物合同读取与输出门槛

生成正式输出前必须读取：
- 插件根目录 `../../DATA_SOURCES_CN.md`
- 插件根目录 `../../CN_OUTPUT_FORMATTING.md`
- 插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`
- 本 skill 本地 `references/cn-markdown-formatting.md`（聊天摘要、正式 Markdown 或最终交付说明）
- 本 skill 本地 `references/data-query-order.md`（当任务需要外部数据查询、行情更新、财报抓取、行业/公司/宏观/监管材料检索时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、待确认项和人工复核边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `references/data-query-order.md`，并按“可用 MCP/已授权数据源优先，网页搜索其次”的顺序执行；若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须先读取 `references/cn-markdown-formatting.md`，并包含来源、口径限制、待确认项和人工复核边界。


# NAV 勾稽

给定已生成的 LP statement 和本期 NAV pack（通过 nav MCP），独立重新计算 LP 资本账户，并逐行比较。

> **已生成 statement 是被测试对象。** NAV pack 是事实来源。

## 重新计算 LP 资本账户

```
期初资本（上期 statement 期末数）
  + 出资（本期已缴 capital calls）
  − 分配（现金 + 实物）
  + 分配净收益 /（亏损）
      = LP% ×（已实现 + 未实现 P&L − 管理费 − 基金费用）
  − 附带权益分配（如本期已 crystallize）
期末资本
```

每项输入都从 NAV pack 拉取：LP commitment %、基金层面 P&L 组成、费用合计、waterfall 输出。

## 比较

将 statement 上每一行与重新计算值比较。容差：`0.01`。对每个不一致项，说明由哪个输入驱动（例如“分配 P&L 不一致：statement 使用 12.40% ownership，NAV pack 显示 Q1 转让后为 12.38%”）。

## 额外检查

- 本 statement 的期末资本 = 下期草稿的期初资本（如可用）。
- 所有 LP 期末资本合计 = 基金 NAV（允许四舍五入差异）。
- 出资承诺、未出资和可召回金额与出资承诺台账一致。

## 输出

逐行输出通过/失败、重新计算值与 statement 值，并列出 flags。不要编辑 statement；publisher 会在审阅后处理这些 flags。
