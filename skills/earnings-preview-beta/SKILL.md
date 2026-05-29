---
name: earnings-preview-single
description: 为单家公司生成简洁的 4-5 页股票研究业绩预览。分析最近一期业绩会文字稿、竞争格局、估值和近期新闻，并产出专业 HTML 报告。
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
- 本 skill 本地 `references/cn-html-formatting.md`（当输出 HTML 文件时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、待确认项和人工复核边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `references/data-query-order.md`，并按“可用 MCP/已授权数据源优先，网页搜索其次”的顺序执行；若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须先读取 `references/cn-markdown-formatting.md`，并包含来源、口径限制、待确认项和人工复核边界。
- 若本 skill 的既有输出包含 HTML 文件，最终回复前必须确认 HTML 文件已生成、HTML 文件路径存在、可在浏览器打开或结构校验通过，并确保最终回复包含 HTML 文件路径。


# 单家公司业绩预览

为单家公司生成简洁、专业的股票研究业绩预览。输出是一个自包含 HTML 文件，目标打印长度为 4-5 页。报告信息密集，包含数字和数据，叙述紧凑并直达重点。

**数据来源（零例外）：** 唯一允许的数据来源是 **Kensho Grounding MCP**（`search`）和 **S&P Global MCP**（`kfinance`）。绝对不允许使用任何其他工具、数据来源或网页访问。具体要求：
- 不要使用 `WebSearch`、`WebFetch`、`web_search`、`brave_search`、`google_search` 或任何通用网页/互联网搜索工具，即使 Kensho 很慢、没有返回结果或暂时不可用也不行。
- 不要使用任何浏览器、URL 抓取或网页爬取工具。
- 如果 Kensho Grounding 对某个查询没有返回结果，尝试改写查询，或在报告中注明“数据不可得”。**绝不要退回使用网页搜索作为替代。**
- 报告中的每一项信息都必须能追溯到 `kfinance` MCP 函数调用或 Kensho `search` 调用。无法追溯到这两者之一的信息不得出现在报告中。

**关键规则：** 写报告任何部分前，必须先完成全部研究和数据收集（阶段 1-5）。

**中间文件规则：** MCP 工具调用返回后，所有原始数据都必须**立即**写入 `/tmp/earnings-preview/` 中的文件，再进入下一次调用。这是为了防止上下文窗口压缩导致数据丢失。不要只把数据保存在记忆里。阶段 1 开始时运行 `mkdir -p /tmp/earnings-preview` 创建目录。**生成 HTML 报告前（阶段 7），必须用 `cat` 命令把所有中间文件重新读回上下文。文件，而不是你对早先对话的记忆，是报告中每个数字、引文和来源 URL 的唯一事实来源。如果跳过读取文件，报告一定会出错。**

**财季规则：** 绝不要根据日历报告日期推断财季。很多公司的财年不是标准日历年（例如 Walmart 的 FY 截至 1 月 31 日，所以 2026 年 2 月的报告覆盖 Q4 FY2026，而不是 Q4 2025 或 Q1 2026）。始终使用 `get_next_earnings_from_identifiers` 或 `get_earnings_from_identifiers` 返回的业绩会名称中明确写出的财季和财年（例如 "Walmart Q4 FY2026 Earnings Call" 表示财季是 Q4 FY2026）。报告标题、标题栏、表格和所有引用都要逐字使用该口径。如果业绩会名称含糊，与 `get_financial_line_item_from_identifiers` 的期间标签交叉核对。

**长度规则：** 报告必须简洁。目标打印长度 4-5 页。不要写冗长的多段叙述。使用紧凑、有力的要点。每句话都必须有存在价值。如果能用更少字说明，就用更少字。

**逐字引用规则：** 在 `<blockquote>` 标签中引用管理层发言时，文本必须从业绩会文字稿中**逐字复制**，包括填充词和句子片段。不要意译、重排、合并文字稿不同位置的句子，也不要“润色”引文。如果不能在文字稿中找到准确短语，就不要把它呈现为直接引文。应改用自己的叙述语气进行转述，不使用 blockquote 格式（例如：“管理层表示数据中心需求仍然显著”）。每个 blockquote 都必须是可与文字稿核验的逐字复制片段。

**计算完整性规则：** 对任何多步骤计算（从年度指引推算季度数字、LTM P/E、y/y 增长率、分部 y/y 变化），逐步写出每一步，并在用于下一步前核验中间结果。如果你写 A + B + C = X，就要先核验 X 算术正确，再把 X 用到后续公式。如果附录中的求和与列出的组成部分不一致，报告就是错的。有疑问时，从原始数据重新计算，而不是复用先前算出的中间值。

**比率命名规则：** 所有估值比率必须明确标记为 **LTM**（过去十二个月）或 **NTM**（未来十二个月）。不要使用“过去口径”或“前瞻口径”等含糊说法；始终使用 LTM 或 NTM。LTM 比率使用最近 4 个已披露季度之和。NTM 比率使用 `get_consensus_estimates_from_identifiers` 返回的**未来 4 个季度一致预期平均 EPS 估计之和**，而不是单个年度数字。竞争对手比较表必须计算并展示 LTM 和 NTM P/E。

**超链接规则（严格执行）：** 报告中的每个论断，无论数字还是非数字，都必须包在 `<a href="#ref-N" class="data-ref">` 超链接中，指向附录中的对应条目。**这不是可选项。报告中的每一个数字都必须是可点击链接。** 包括：收入、EPS、利润率、增长率、市值、P/E、股票回报、目标价、分部收入和其他任何财务指标。也包括业绩会文字稿或 Kensho 搜索中的定性论断。每个唯一论断分配连续引用 ID（`ref-1`、`ref-2` 等）。超链接样式应克制：海军蓝、无下划线、悬停时点状下划线。**不要在报告正文中写任何没有 `<a>` 标签包裹的数字。** 示例：写 `<a href="#ref-1" class="data-ref">$152.3B</a>`，绝不要把 `$152.3B` 写成纯文本。

---

## 阶段 1：公司画像与设置

1. 从 `$ARGUMENTS` 解析单家公司 ticker（去除空白）。
2. 运行 `mkdir -p /tmp/earnings-preview` 创建工作目录。
3. 调用 `get_latest()` 建立当前报告期间语境。
4. 调用 `get_info_from_identifiers`，记录市值、行业。
5. 调用 `get_company_summary_from_identifiers`，记录业务描述。
6. 调用 `get_next_earnings_from_identifiers`，记录即将发布业绩的日期和财季名称。

**立即写入** `/tmp/earnings-preview/company-info.txt`：
```
TICKER: [股票代码]
COMPANY: [公司全称]
INDUSTRY: [行业]
市值：[数值]（截至[日期]）
NEXT_EARNINGS_DATE: [日期]
NEXT_EARNINGS_QUARTER: [API 原样返回的 Q# FY####]
BUSINESS_DESCRIPTION: [2-3 句摘要]
```

---

## 阶段 2：业绩会文字稿分析（强制，写作前完成）

1. 调用 `get_latest_earnings_from_identifiers` 获取最近已完成业绩会的 `key_dev_id`。
2. 对该文字稿调用 `get_transcript_from_key_dev_id`。
3. **立即写入** `/tmp/earnings-preview/transcript-extracts.txt`，包含以下章节。仍在上下文中保有文字稿时就写入，不要等待：

```
TRANSCRIPT_SOURCE: [业绩会名称，例如“2025 财年第 3 季度业绩会”]
KEY_DEV_ID: [key_dev_id]
CALL_DATE: [日期]
FISCAL_QUARTER: [Q# FY####]

=== 逐字引文（准确复制粘贴，不要意译） ===
QUOTE_1: "[文字稿中的准确文本]"
SPEAKER_1: [姓名], [职务]
CONTEXT_1: [用 1 句话说明出现位置：预先准备发言或问答]

QUOTE_2: "[文字稿中的准确文本]"
SPEAKER_2: [姓名], [职务]
CONTEXT_2: [语境]

QUOTE_3: "[文字稿中的准确文本]"
SPEAKER_3: [姓名], [职务]
CONTEXT_3: [语境]

QUOTE_4: "[文字稿中的准确文本]"
SPEAKER_4: [姓名], [职务]
CONTEXT_4: [语境]

=== 指引（仅限量化） ===
- [指标]: [管理层表述的区间或点估计]
- [指标]: [区间或点估计]

=== 关键驱动因素 ===
- [驱动因素 1，含支持数据点]
- [驱动因素 2，含支持数据点]
- [驱动因素 3，含支持数据点]

=== 逆风与风险 ===
- [风险 1，如可得则量化]
- [风险 2]

=== 分析师问答主题 ===
- [主题 1：分析师追问的内容]
- [主题 2]
- [主题 3]

=== 综合：下季度需关注的主题 ===
- [主题 1]
- [主题 2]
- [主题 3]
```

---

## 阶段 3：竞争对手分析

1. 调用 `get_competitors_from_identifiers`，参数 `competitor_来源="all"`。
2. 选择**最相关的前 5-7 家上市竞争对手**。
3. 对该公司和所有选定竞争对手，收集：
   - `get_prices_from_identifiers`，参数 `periodicity="day"`，最近 12 个月。
   - `get_financial_line_item_from_identifiers`，用于 `diluted_eps`，参数 `period_type="quarterly"`、`num_periods=8`。
   - `get_capitalization_from_identifiers`，参数 `capitalization="market_cap"`（最新）。
   - `get_consensus_estimates_from_identifiers`，参数 `period_type="quarterly"`、`num_periods_forward=4`；它会返回未来 4 个季度的一致预期平均 EPS，用于汇总计算 NTM EPS。

**每次工具调用返回后，立即把原始数据追加到对应中间文件：**

**写入** `/tmp/earnings-preview/prices.csv`，每个 (ticker, date, close) 一行。包含 `来源` 列，写出准确 MCP 函数调用。先写主体公司的价格，再按获取顺序写每个竞争对手：
```
ticker,date,close,来源
D,2025-02-19,55.67,get_prices_from_identifiers(identifier='D',periodicity='day')
D,2025-02-20,55.82,get_prices_from_identifiers(identifier='D',periodicity='day')
...
DUK,2025-02-19,111.79,get_prices_from_identifiers(identifier='DUK',periodicity='day')
...
```
说明：同一次调用返回的所有行 `来源` 值相同；每行都要写，确保始终可用。

**写入** `/tmp/earnings-preview/peer-eps.csv`，每个 (ticker, period, eps) 一行。每次 `diluted_eps` 调用后立即写入：
```
ticker,period,diluted_eps,来源
D,Q4 2024,1.09,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
D,Q1 2025,-0.11,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
...
DUK,Q4 2024,1.52,get_financial_line_item_from_identifiers(identifier='DUK',line_item='diluted_eps',period_type='quarterly')
...
```

**写入** `/tmp/earnings-preview/peer-market-caps.csv`，每个 ticker 一行。每次 `market_cap` 调用后立即写入：
```
ticker,market_cap,retrieval_date,来源
D,55900000000,2026-02-19,get_capitalization_from_identifiers(identifier='D',capitalization='market_cap')
DUK,98300000000,2026-02-19,get_capitalization_from_identifiers(identifier='DUK',capitalization='market_cap')
...
```

**写入** `/tmp/earnings-preview/consensus-eps.csv`，每个 (ticker, period, consensus mean EPS) 一行。每次 `get_consensus_estimates_from_identifiers` 调用后立即写入：
```
ticker,period,consensus_mean_eps,num_estimates,来源
D,Q4 2025,0.88,12,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
D,Q1 2026,0.72,10,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
D,Q2 2026,0.91,9,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
D,Q3 2026,1.05,8,get_consensus_estimates_from_identifiers(identifier='D',period_type='quarterly',num_periods_forward=4)
DUK,Q4 2025,1.48,14,get_consensus_estimates_from_identifiers(identifier='DUK',period_type='quarterly',num_periods_forward=4)
...
```

4. **此时不要计算 P/E 或回报。** 原始数据已经落盘。计算在阶段 6（核验）中读取这些文件完成。

**日期一致性规则（股票回报）：** 计算相对股票回报（YTD %、1-yr %、30d %、90d %）时，所有 ticker 必须使用**完全相同的起止日期**。把所有价格数据写入 `prices.csv` 后，识别所有 ticker 数据中共同存在的第一个交易日，并将其作为共同基准日期。不要对不同 ticker 使用不同基准日期（例如主体用 2 月 19 日，同业用 2 月 28 日）。如果某个 ticker 的数据起点更晚，则所有计算都使用第一个重叠日期。在附录中为每项回报计算说明共同基准日期。

**P/E 口径规则（LTM P/E）：** 计算每家公司 LTM P/E 时，使用该公司的**最近 4 个已披露季度**，来自 `peer-eps.csv`，不要把同一个固定日历窗口套用到所有公司。如果某个同业已披露 Q4 2025，而主体公司只披露到 Q3 2025，则该同业的 LTM EPS 应包含 Q4 2025。检查每家公司最新披露期间，并对每家公司使用其最近 4 个期间。在附录中说明每个 P/E 使用了哪 4 个季度。

**市值日期戳：** 报告市值时，使用 `peer-market-caps.csv` 中的 `retrieval_date`。如果它不同于报告日期，在附录中说明。

---

## 阶段 4：新闻、预期与行业情报（通过 Kensho Grounding）

对以下**每个**类别运行这些 `search` 查询。不要跳过任何一个。

**关键 — 捕获来源 URL：** 每个 Kensho `search` 结果都包含底层文章、报告或数据页的**来源 URL**。必须把 URL 与每条发现一起记录。

**每次 search 调用后，立即用以下格式追加结果到** `/tmp/earnings-preview/kensho-findings.txt`。不要等所有搜索完成后再写；每次调用后就写：

```
=== 搜索："[使用的查询]" ===
DATE_RUN: [今日日期]
CATEGORY: [预期|分析师评级|风险|新闻|行业]

FINDING_1: [关键发现或摘录]
URL_1: [搜索结果中的来源 URL]
SOURCE_1: [发布机构名称，如可得则含日期]

FINDING_2: [关键发现或摘录]
URL_2: [来源 URL]
SOURCE_2: [发布机构名称，日期]

[……继续记录本次搜索的所有相关结果……]
```

**业绩预期与分析师情绪：**
1. 对“[TICKER] 业绩预期 一致预期 EPS 收入 即将发布季度”执行 `search`。
   - 记录：一致预期 EPS、一致预期收入、过去 90 天预期修正方向。
   - **立即追加到 kensho-findings.txt。**
2. 对“[TICKER] 分析师评级 目标价 上调 下调”执行 `search`。
   - 记录：近期上调/下调评级、目标价区间、牛/熊逻辑摘要。
   - **立即追加到 kensho-findings.txt。**
3. 对“[TICKER] 风险 熊方案例 投资者担忧”执行 `search`。
   - 记录：关键争议、熊方论点、即将发布业绩的 swing factors。
   - **立即追加到 kensho-findings.txt。**

**近期新闻（强制，不要跳过）：**
4. 对“[TICKER] [公司名称] 近期新闻 进展”执行 `search`。
   - 记录过去 60 天的重要新闻：M&A、产品发布、高管变动、监管行动、合作伙伴、法律进展、关税，或任何可能影响即将发布业绩或未来指引的事件。
   - 对每项记录日期、标题、潜在业绩影响。
   - **立即追加到 kensho-findings.txt。**

**行业语境：**
5. 对“[公司行业/板块] 行业展望 趋势”执行 `search`。
   - 记录行业层面的顺风/逆风、宏观数据、竞争动态。
   - **立即追加到 kensho-findings.txt。**

---

## 阶段 5：财务数据收集

**季度财务数据（最近 8 个季度）：**
`get_financial_line_item_from_identifiers`，参数 `period_type="quarterly"`、`num_periods=8`，用于：
`revenue`、`gross_profit`、`operating_income`、`ebitda`、`net_income`、`diluted_eps`

**每个 line item 调用返回后，立即追加到** `/tmp/earnings-preview/financials.csv`。按返回原样写入原始值，不要四舍五入或转换。包含 `来源` 列，写出准确 MCP 函数调用及参数：
```
ticker,period,line_item,value,来源
D,Q4 2024,revenue,3941000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q1 2025,revenue,3400000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q2 2025,revenue,4076000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q3 2025,revenue,3810000000,get_financial_line_item_from_identifiers(identifier='D',line_item='revenue',period_type='quarterly')
D,Q4 2024,diluted_eps,1.09,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
D,Q1 2025,diluted_eps,-0.11,get_financial_line_item_from_identifiers(identifier='D',line_item='diluted_eps',period_type='quarterly')
...
```

**此时不要计算利润率或增长率。** 只写原始数据。计算在阶段 6 进行。

**分部数据：**
- `get_segments_from_identifiers`，参数 `segment_type="business"`、`period_type="quarterly"`、`num_periods=8`。
- 需要 8 个季度（不是 4 个），因为 y/y 比较需要上一年同期。要计算 Q3 2025 的 y/y，需要 Q3 2024，也就是往前第 5 个季度。**如果 API 响应中没有上一年同期分部数据，不要估算或编造。在报告中写 "y/y not available"。**

**立即写入** `/tmp/earnings-preview/segments.csv`：
```
ticker,period,segment_name,revenue,来源
D,Q3 2024,Dominion Energy Virginia,2762000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2024,Dominion Energy South Carolina,848000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2024,Contracted Energy,260000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2025,Dominion Energy Virginia,3311000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2025,Dominion Energy South Carolina,945000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
D,Q3 2025,Contracted Energy,297000000,get_segments_from_identifiers(identifier='D',segment_type='business',period_type='quarterly')
...
```

**业绩历史（用于股价图标注）：**
- `get_earnings_from_identifiers` — 收集 12 个月价格窗口内的过往业绩日期。
- **立即写入** `/tmp/earnings-preview/earnings-dates.csv`：
```
ticker,earnings_date,call_name,来源
D,2025-05-02,Q1 2025 Earnings Call,get_earnings_from_identifiers(identifier='D')
D,2025-08-01,Q2 2025 Earnings Call,get_earnings_from_identifiers(identifier='D')
D,2025-10-31,Q3 2025 Earnings Call,get_earnings_from_identifiers(identifier='D')
...
```

---

## 阶段 6：核验与计算（强制，不要跳过）

生成报告前，重新读取所有中间文件，并从干净数据执行计算。本阶段通过使用文件而不是压缩后的对话上下文来确保数据完整性。

1. **使用 bash `cat` 命令读取所有中间文件：**
   - `cat /tmp/earnings-preview/company-info.txt`
   - `cat /tmp/earnings-preview/transcript-extracts.txt`
   - `cat /tmp/earnings-preview/financials.csv`
   - `cat /tmp/earnings-preview/segments.csv`
   - `cat /tmp/earnings-preview/prices.csv`
   - `cat /tmp/earnings-preview/peer-eps.csv`
   - `cat /tmp/earnings-preview/peer-market-caps.csv`
   - `cat /tmp/earnings-preview/consensus-eps.csv`
   - `cat /tmp/earnings-preview/kensho-findings.txt`
   - `cat /tmp/earnings-preview/earnings-dates.csv`

2. **基于现在已读入上下文的原始数据计算派生指标：**
   - 毛利率 % = gross_profit / revenue（按季度）。
   - 经营利润率 % = operating_income / revenue（按季度）。
   - 收入 y/y 增长率 % = (current Q revenue - year-ago Q revenue) / year-ago Q revenue。
   - EPS y/y 增长率 % = 同一逻辑；如果基数为负，用“无意义”。
   - 分部 y/y 增长率 % = 按分部名称匹配上一年同期；如果缺失，注明“y/y 不可得”。
   - 每家公司 LTM P/E = 最新价格 / 最近 4 个季度 EPS 之和（使用 `peer-eps.csv` 检查每个 ticker 可用的 4 个季度）。
   - 每家公司 NTM P/E = 最新价格 / NTM EPS，其中 **NTM EPS = `consensus-eps.csv` 中未来 4 个季度一致预期平均 EPS 之和**。对每个 ticker 把 4 个季度的 consensus_mean_eps 全部相加。如果某个同业少于 4 个未来季度，则 NTM P/E 标记为 "n/a"。在附录中说明相加的是哪 4 个季度。
   - 股票回报（YTD、1-yr、30d、90d）= 在 `prices.csv` 中找到**所有 ticker 共同的第一个日期**，并从该日期计算回报。

3. **交叉检查：**
   - 核验每个 segment y/y 都在 `segments.csv` 中有真实上一年同期行。如果没有，标记 "y/y not available"。
   - 核验所有股票回报基准日期在所有 ticker 间完全一致。
   - 对任何多步骤计算重新汇总组成部分（例如 LTM EPS 之和等于 4 个季度值）。
   - 核验 `transcript-extracts.txt` 中所有逐字引文都是准确复制（不是意译）。

4. **写入** `/tmp/earnings-preview/calculations.csv`，包含所有派生值：
```
ticker,metric,value,formula,components
D,gross_margin_Q3_2025,32.5%,gross_profit/revenue,"gross_profit=1238100000,revenue=3810000000"
D,revenue_yoy_Q3_2025,+9.3%,(Q3_2025-Q3_2024)/Q3_2024,"Q3_2025=3810000000,Q3_2024=3486000000"
D,ltm_pe,24.2x,price/ltm_eps,"price=65.46,ltm_eps=2.70,quarters=Q4_2024+Q1_2025+Q2_2025+Q3_2025"
D,ntm_pe,18.5x,price/ntm_eps,"price=65.46,ntm_eps=3.56,quarters=Q4_2025(0.88)+Q1_2026(0.72)+Q2_2026(0.91)+Q3_2026(1.05),来源=get_consensus_estimates_from_identifiers"
D,yoy_return,+17.6%,(end-start)/start,"end=65.46,start=55.67,base_date=2025-02-19"
DUK,yoy_return,+13.0%,(end-start)/start,"end=126.32,start=111.79,base_date=2025-02-19"
...
```

这个文件会成为报告中所有数字的唯一事实来源。

---

## 阶段 7：生成 HTML 报告

**停止 — 写任何 HTML 前，必须读取所有中间文件。这是阻塞性前置条件。**

这不是可选项。必须将下面每条 `cat` 命令作为**单独 bash 工具调用**运行（不要合并为一条命令）。这样可确保每个文件内容都单独加载并在对话中可见。不要合并，不要跳过。

逐条运行以下命令，每条都是独立 bash 调用：

1. `cat /tmp/earnings-preview/company-info.txt`
2. `cat /tmp/earnings-preview/transcript-extracts.txt`
3. `cat /tmp/earnings-preview/financials.csv`
4. `cat /tmp/earnings-preview/segments.csv`
5. `cat /tmp/earnings-preview/prices.csv`
6. `cat /tmp/earnings-preview/peer-eps.csv`
7. `cat /tmp/earnings-preview/peer-market-caps.csv`
8. `cat /tmp/earnings-preview/consensus-eps.csv`
9. `cat /tmp/earnings-preview/kensho-findings.txt`
10. `cat /tmp/earnings-preview/earnings-dates.csv`
11. `cat /tmp/earnings-preview/calculations.csv`

**读取全部文件后，必须向用户打印摘要消息**，列出每个文件及状态。严格使用以下格式：

```
--- 数据文件核验 ---
1. company-info.txt        ✓ 已加载（[N] 行）
2. transcript-extracts.txt ✓ 已加载（[N] 行）
3. financials.csv          ✓ 已加载（[N] 行）
4. segments.csv            ✓ 已加载（[N] 行）
5. prices.csv              ✓ 已加载（[N] 行）
6. peer-eps.csv            ✓ 已加载（[N] 行）
7. peer-market-caps.csv    ✓ 已加载（[N] 行）
8. consensus-eps.csv       ✓ 已加载（[N] 行）
9. kensho-findings.txt     ✓ 已加载（[N] 行）
10. earnings-dates.csv     ✓ 已加载（[N] 行）
11. calculations.csv       ✓ 已加载（[N] 行）

所有中间数据文件均已成功加载。
正在使用文件数据作为唯一事实来源生成报告。
---
```

如果任何文件缺失或为空，停止并告诉用户哪个文件失败。不要在数据缺失时继续生成报告。

**HTML 报告中的每个数字、引文、来源 URL 和 MCP 函数调用引用都必须来自这些文件，而不是来自你对早先对话轮次的记忆。** 文件是唯一事实来源。早先对话上下文可能已经被压缩或摘要化，依赖它会导致错误。如果某个数据点不在文件中，就不应出现在报告中。

完整 HTML 模板、CSS 和 Chart.js 配置见 [report-template.md](report-template.md)。

**强制 — 图表必须使用模板辅助函数：**
`report-template.md` 提供了预构建且已调试的 Chart.js 辅助函数。必须使用这些准确函数创建图表。不要编写自定义内联 Chart.js 代码。辅助函数包括：
- `createRevEpsChart(canvasId, labels, revenueData, epsData, revLabel)` — 用于图 1
- `createMarginChart(canvasId, labels, grossMargins, opMargins)` — 用于图 2
- `createRevGrowthChart(canvasId, labels, growthData)` — 用于图 3
- `createAnnotatedPriceChart(canvasId, labels, prices, earningsDates, ticker)` — 用于图 5
- `createCompPerfChart(canvasId, labels, datasets)` — 用于图 6
- `createPEChart(canvasId, companies)` — 用于图 7

每个图表调用都必须放在自己的 `<script>` 标签中，并包在 try-catch 块里。这样一个图表的 bug 不会阻止其他图表渲染。示例：
```html
<script>
try {
  createRevEpsChart('chart-rev-eps', [...], [...], [...], '收入 ($B)');
} catch(e) { console.error('图 1 错误：', e); }
</script>
<script>
try {
  createMarginChart('chart-margins', [...], [...], [...]);
} catch(e) { console.error('图 2 错误：', e); }
</script>
```

### 报告结构（总计 4-5 页）

报告分为两部分：**叙述**（第 1-2 页）和**图表**（第 3-5 页）。保持两者紧密整合。

---

**AI 免责声明（强制 — 必须出现在 3 个位置）：**
HTML 报告中必须包含以下免责声明文本。这不是可选项；没有它，报告不完整：

> **“分析由 AI 生成，请核验所有输出”**

它必须准确出现在以下 3 个位置：
1. **页眉横幅** — 在封面页眉之前，作为居中的黄色横幅：`<div class="ai-disclaimer">分析由 AI 生成，请核验所有输出</div>`
2. **页脚** — 放在 page-footer div 内，作为醒目的黄色横幅：`<div class="footer-disclaimer">分析由 AI 生成，请核验所有输出</div>`
3. **附录** — 在附录章节第一行、表格之前：`<div class="ai-disclaimer">分析由 AI 生成，请核验所有输出</div>`

---

**第 1 页：封面与投资逻辑**

- **AI 免责声明横幅**（黄色、居中；见 AI 免责声明规则）。
- **页眉**：公司名称（TICKER）| 行业 | 报告日期。
- **标题**：贴合本季度的主题化标题（例如“沃尔玛 (WMT) 2026 财年第 4 季度业绩预览：节日季收成，Furner 首份成绩单能否确认 1 万亿美元逻辑？”）。
- **执行层投资逻辑**（最多 2-3 个短段落，并配要点）：
  - 用 1-2 句话说明我们对本次业绩的预期。
  - 4-6 条要点覆盖：我们的 EPS 估计 vs 一致预期、指引预期、需关注的关键指标、什么会推动股价、关键争议。
  - 直接且有观点；给出判断，不要处处对冲。
- 将最近一期业绩会中的**关键管理层引文**自然融入叙述中作为支持证据。不要放在单独标题下。格式为缩进 blockquote。

---

**第 2 页：预期、主题与新闻**

- **一致预期表**（单表，标记为图表）：
  - 列：指标 | 一致预期 | 我们的预测 | 同比变化。
  - 行：收入、EPS、毛利率、营业利润，以及 2-3 个对公司最重要的特定 KPI（例如可比店销售额、电子商务增长、会员收入，取决于市场关注点）。
  - **颜色编码严格机械执行：** 如果同比变化为负，使用 `class="neg"`（红色）。如果为正，使用 `class="pos"`（绿色）。如果为零或 N/A，使用 `class="neutral"`。由数字符号决定 class；不要基于解读覆盖。-1.1% 永远是红色，即使降幅很小。
  - 这是唯一的指引/预期章节。不要在其他地方重复预期数据。

- **EPS 之外的关键指标**（3-5 条要点）：
  - 除 EPS 数字外，决定本季度好坏的具体指标。
  - 每项说明：指标是什么、一致预期/管理层预期是什么、为什么重要。
  - 要具体：“Walmart Connect 广告收入增长（一致预期约同比 +30%，第 3 季度为 33%）”。

- **需要关注的主题**（3-5 条要点）：
  - 即将发布报告的前瞻性观察项。
  - 管理层需要兑现什么、可能有什么惊喜、熊方关注什么。
  - 每个主题最多 1-2 句话。

- **近期新闻与进展**（3-5 条要点）：
  - 过去 60 天的重要新闻，每项一行。
  - 日期 + 标题 + 简短影响评估。
  - 只纳入可能影响即将发布业绩或指引的事项。

---

**第 3-5 页：图表（全部图表和表格）**

所有图表按顺序编号。每个图表都有标题和来源行。

- **图 1：季度收入与摊薄 EPS** — 柱线组合图，8 个季度。
- **图 2：利润率趋势（毛利率与营业利润率）** — 双线图，8 个季度。
- **图 3：收入同比增速 %** — 柱状图，绿色/红色条件着色。**只纳入当前期和上一年同期数据都存在的季度**（通常为抓取的 8 个季度中的最近 4 个）。不要纳入无法计算 y/y 的季度；图表应有 4 个柱，而不是 8 个。
- **图 4：业务分部收入** — 表格：分部 | 最近季度收入（百万美元） | 占总收入比例 | 同比变化。
- **图 5：过去 1 年股价及业绩日期** — 价格折线，业绩日期用垂直标注线，标记季度和业绩后 1 日股价变化。
- **图 6：股价表现与可比公司对比（指数化至 100）** — 多线图，主体公司为加粗实线，竞争对手为较细虚线。
- **图 7：LTM P/E 与可比公司对比** — 横向条形图，主体公司用海军蓝高亮。
- **图 8：可比公司对比表** — 股票代码 | 公司 | 市值 | LTM P/E | NTM P/E | YTD % | 1 年 %。

---

**附录：数据来源与计算（强制，不要跳过或缩写）**

附录必须以 AI 免责声明横幅开头：`<div class="ai-disclaimer">分析由 AI 生成，请核验所有输出</div>`

报告最后一页必须包含一个附录表，记录报告中引用的**每一项论断**，包括数字和非数字。**报告正文中出现的每个数字都必须在附录中有对应行，并且正文中的每个数字都必须是可点击 `<a href="#ref-N">` 超链接，点击后跳转到附录行。** 如果数字出现在报告中但没有链接到附录，报告不完整。

- **表格列**：编号 | 事实 | 数值 | 来源与推导
- **编号**：与报告正文超链接锚点匹配的顺序 ID（`ref-1`、`ref-2` 等）。每行都有 `id="ref-N"` 属性，方便超链接滚动到对应行。
- **事实**：可读标签（例如“2026 财年第 3 季度收入”、“LTM P/E — WMT”、“管理层提示关税压力”、“Barclays 将评级上调至增持”）。
- **数值**：报告中展示的准确数字（例如 "$152.3B"、"24.5%"、"28.1x"）。非数字事实可留空或写 "N/A"。
- **来源与推导**：这是关键列。**每行都必须有具体、详细的来源，不只是标签。** 严格遵守以下规则：

  **对于来自 S&P Capital IQ 的原始财务数据（收入、EPS、毛利、营业利润、净利润、EBITDA、价格、市值等）：**
  - 写明使用的 MCP 函数及关键参数。格式：`S&P Capital IQ — [function_name](identifier='[TICKER]', line_item='[item]', period_type='[type]', period='[Q# FY####]')`
  - 示例：
    - `S&P Capital IQ — get_financial_line_item_from_identifiers(identifier='WMT', line_item='revenue', period_type='quarterly', period='Q3 FY2026')`
    - `S&P Capital IQ — get_financial_line_item_from_identifiers(identifier='WMT', line_item='diluted_eps', period_type='quarterly', period='Q3 FY2026')`
    - `S&P Capital IQ — get_prices_from_identifiers(identifier='WMT', periodicity='day')`
    - `S&P Capital IQ — get_capitalization_from_identifiers(identifier='WMT', capitalization='market_cap')`
  - **不要只写 "S&P Capital IQ" 而不写细节。** 读者必须知道哪个工具调用产生了哪个数据点。

  **对于计算值（利润率、增长率、P/E、回报、y/y 变化）：**
  - 展示完整公式，并且**公式组成部分必须带超链接**；每个组成部分都必须是 `<a href="#ref-N">`，链接到附录中对应原始数据行。这一点很关键：读者必须能从计算值点击到每个输入。
  - 示例：`毛利率 = <a href='#ref-5'>毛利 $37.2B</a> / <a href='#ref-1'>收入 $152.3B</a> = 24.4%。来源：S&P Capital IQ（计算值）`
  - 示例：`LTM P/E = <a href='#ref-20'>价格 $172.35</a> / (<a href='#ref-8'>第 1 季度 EPS $1.47</a> + <a href='#ref-9'>第 2 季度 EPS $1.84</a> + <a href='#ref-10'>第 3 季度 EPS $1.53</a> + <a href='#ref-11'>第 4 季度 EPS $1.80</a>) = $172.35 / $6.64 = 25.9x`
  - 示例：`收入同比增长 = (<a href='#ref-12'>2026 财年第 3 季度收入 $165.8B</a> - <a href='#ref-3'>2025 财年第 3 季度收入 $160.8B</a>) / <a href='#ref-3'>2025 财年第 3 季度收入 $160.8B</a> = +3.1%`
  - **公式中的每个组成部分都必须是可点击超链接。** 不要写包含纯文本数字的公式。

  **对于文字记录来源论断（引文、管理层评论、指引）：**
  - 写出文字记录中的**逐字摘录句子**。
  - 用完整文字记录名称和用于获取它的 `key_dev_id` 引用该文字记录。
  - 格式：`"[逐字引文]" — [发言人], [职务]。来源：[Q# FY#### 业绩会文字记录]（key_dev_id: [ID]）`
  - 示例：`“我们预计第 4 季度可比销售额增长 3-4%。” — CEO John Furner。来源：2026 财年第 3 季度业绩会文字记录（key_dev_id: 12345678）`

  **对于 Kensho Grounding 搜索结果（新闻、分析师评级、一致预期）：**
  - 写出搜索结果中的关键发现或摘录。
  - **强制：包含 Kensho `search` 工具返回的来源 URL**，作为可点击 `<a href="[URL]" target="_blank">` 超链接。这是最重要的部分；读者必须能点击到原始来源。
  - 格式：`"[发现/摘录]" — <a href="[URL]" target="_blank">[来源标题或发布机构]</a>。查询：search("[使用的查询]")`
  - 示例：`“Barclays 于 2026 年 1 月 15 日将 WMT 上调至增持，目标价 210 美元。” — <a href="https://www.investing.com/news/barclays-upgrades-wmt" target="_blank">Investing.com，2026 年 1 月 15 日</a>。查询：search("WMT 分析师评级 目标价 上调 下调")`
  - 如果某条结果没有返回 URL，写“来源 URL 不可得”，并仍包含 search query。

**完整性检查：** 最终确认报告前，扫描报告正文中的每个数字。如果任何数字没有包在 `<a href="#ref-N" class="data-ref">` 中，修复它。如果任何附录行的“来源与推导”只是 "S&P Capital IQ" 这种裸标签而没有函数调用细节，修复它。如果任何计算值公式缺少带超链接的组成部分，修复它。如果任何 Kensho 来源论断缺少来源 URL，修复它。

按章节对附录行分组（财务数据、估值、预测与一致预期、文字稿论断、新闻与分析师评论、股价表现），并加小标题。使用较小字号（10-11px）。

---

## 阶段 8：输出

1. 将完整 HTML 文件写入当前工作目录中的 `earnings-preview-[TICKER]-YYYY-MM-DD.html`。
2. 在浏览器中打开：`open earnings-preview-[TICKER]-YYYY-MM-DD.html`。
3. 告诉用户文件已经创建，并总结关键发现。
