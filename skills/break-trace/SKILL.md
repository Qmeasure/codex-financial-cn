---
name: break-trace
description: 将对账差异追溯到来源交易或入账记录：从差异行沿审计轨迹回溯到两侧原始分录，说明差异内容和原因。用于 gl-recon 已完成差异分类之后。
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


# 差异根因追踪

给定单条差异行（key、总账值、子账值、分类、可能原因），追溯到来源并生成根因说明。

## 追踪路径

1. **拉取总账侧**：通过 internal-gl MCP 获取产生该总账行的会计分录或入账记录：分录 ID、入账日期、来源系统、批次 ID、制单人。
2. **拉取子账侧**：通过 subledger MCP 获取匹配交易：交易 ID、交易/结算日期、交易对手、来源 feed、使用的汇率。
3. **比较属性差异**：对齐入账日期、汇率/汇率日期、科目映射、数量符号、金额符号。不同的属性通常就是原因。

## 原因 → 说明

将根因写成一句话，格式为 **“⟨哪一侧⟩ ⟨做了什么⟩，因为 ⟨原因⟩”**，例如：

- “总账按结算日（T+2）入账，而子账按交易日入账：时间性差异，预计 2026-05-07 清除。”
- “子账使用 WM/R 16:00 汇率；总账使用 Bloomberg 收盘汇率：基础金额出现 12 bps 的 FX 差异。”
- “证券 ABC123 在映射表中对应总账科目 11420，但子账传入 11410：映射差异，升级给 reference-data。”
- “子账重复入账该笔交易（交易 ID 88412 和 88419 重复）：重复入账，抑制 88419。”

## 输出

对每条已追踪差异，返回：

```json
{
  "key": "...",
  "root_cause": "按上述格式写成一句话",
  "owner": "ops | reference-data | accounting | upstream-system",
  "expected_clear_date": "YYYY-MM-DD or null",
  "action": "monitor | adjust | raise-ticket | suppress"
}
```

只有 resolver 写入调整；本技能只诊断，不入账。
