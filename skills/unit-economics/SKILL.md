---
name: unit-economics
description: 分析 PE 标的的单位经济，包括 ARR cohort、LTV/CAC、净留存、回本周期、收入质量和利润率瀑布。对软件/SaaS、经常性收入和订阅业务尤其重要。用于评估收入质量、构建 cohort analysis 或评估客户经济性。触发语包括“unit economics”“cohort analysis”“ARR analysis”“LTV CAC”“net retention”“revenue quality”或“customer economics”。
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
- 插件根目录 `../../CN_XLSX_OUTPUT_CONTRACT.md`（当输出 XLSX/Excel 文件时）
- 本 skill 本地 `references/cn-markdown-formatting.md`（聊天摘要、正式 Markdown 或最终交付说明）
- 本 skill 本地 `references/data-query-order.md`（当任务需要外部数据查询、行情更新、财报抓取、行业/公司/宏观/监管材料检索时）
- 本 skill 本地 `references/cn-xlsx-formatting.md`（当输出 XLSX/Excel 文件时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、待确认项和人工复核边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 若本 skill 的既有输出包含 XLSX/Excel 文件，最终回复前必须确认 XLSX 文件已生成、XLSX 文件路径存在、可打开或结构校验通过，并确保最终回复包含 XLSX 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `references/data-query-order.md`，并按“可用 MCP/已授权数据源优先，网页搜索其次”的顺序执行；若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须先读取 `references/cn-markdown-formatting.md`，并包含来源、口径限制、待确认项和人工复核边界。


# 单位经济分析

## 工作流

### 步骤 1：识别商业模式

先判断收入模式，以定制分析：
- **SaaS / 订阅**：ARR、净留存、cohorts
- **经常性服务**：合同价值、续约率、upsell
- **交易 / 用量计费**：单笔交易收入、交易量趋势、take rate
- **混合模式**：按收入流拆分

### 步骤 2：核心指标

#### ARR / 收入质量
- **ARR bridge**：期初 ARR → 新增 → 扩张 → 收缩 → 流失 → 期末 ARR
- **按 cohort 拆分 ARR**：vintage 分析，即每个年度 cohort 如何留存和增长
- **收入集中度**：Top 10/20/50 客户占总收入比例
- **按类型拆分收入**：经常性 vs. 非经常性 vs. 专业服务
- **合同结构**：ACV 分布、多年合同比例、自动续约比例

#### 客户经济性
- **CAC（客户获取成本）**：总 S&M 支出 / 新增客户数
- **LTV（客户生命周期价值）**：(ARPU × 毛利率) / 流失率
- **LTV:CAC 比率**：健康业务目标 >3x
- **CAC 回本周期**：回收获客成本所需月数
- **混合 vs. 分群**：按客户分群拆分（enterprise vs. SMB vs. mid-market）

#### 留存与扩张
- **Gross retention**：期初 ARR 中保留比例（不含扩张）
- **Net retention (NDR)**：含扩张后的期初 ARR 保留比例
- **Logo churn**：流失客户比例
- **Dollar churn**：流失收入比例（通常不同于 logo churn）
- **Expansion rate**：upsell + cross-sell 占期初 ARR 比例

#### Cohort 分析
构建 cohort 矩阵：

| Cohort | 第 0 年 | 第 1 年 | 第 2 年 | 第 3 年 | 第 4 年 |
|--------|--------|--------|--------|--------|--------|
| 2020 | $1.0M | $1.1M | $1.2M | $1.1M | |
| 2021 | $1.5M | $1.7M | $1.8M | | |
| 2022 | $2.0M | $2.3M | | | |
| 2023 | $3.0M | | | | |

同时展示绝对金额和指数化视图（第 0 年 = 100%）。

#### 利润率瀑布
- 收入 → 毛利 → Contribution Margin → EBITDA
- 全口径单位经济：获取、服务和留住一个客户分别需要多少成本？
- 按收入流拆分毛利率（订阅 vs. 服务 vs. 其他）

### 步骤 3：基准比较

与相关基准比较单位经济：
- **SaaS Rule of 40**：增长率 + EBITDA 利润率 > 40%
- **SaaS Magic Number**：净新增 ARR / 前期 S&M 支出 > 0.75x
- **NDR 基准**：Best-in-class >120%，良好 >110%，需关注 <100%
- **LTV:CAC**：Best-in-class >5x，良好 >3x，需关注 <2x
- **Gross retention**：Best-in-class >95%，良好 >90%，需关注 <85%
- **CAC 回本周期**：Best-in-class <12 个月，良好 <18 个月，需关注 >24 个月

### 步骤 4：收入质量评分

综合形成收入质量评估：

| 因素 | 评分（1-5） | 备注 |
|------|-------------|------|
| 经常性收入比例 | | |
| 净留存 | | |
| 客户集中度 | | |
| Cohort 稳定性 | | |
| 增长耐久性 | | |
| 利润率画像 | | |
| **总体** | | |

### 步骤 5：输出

- Excel 工作簿，包含 ARR bridge、cohort 矩阵、单位经济 dashboard
- 带关键指标和基准的摘要页
- 红旗事项和需要进一步尽调的领域

## 重要说明

- 如可获得，始终要求客户级原始数据；汇总指标可能掩盖问题。
- NDR 高于 100% 也可能掩盖高 gross churn，只要扩张足够强即可；始终同时展示两者。
- Cohort 分析是判断收入质量最重要的视角；应尽力获取该数据。
- 区分合同 ARR 与实际确认收入。
- 对用量计费模式，重点关注使用量趋势和扩张模式，而不是传统 ARR 指标。
- 专业服务收入应单独评估；它不是经常性收入，利润率通常更低。
