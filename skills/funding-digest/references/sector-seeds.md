> Reference 链路：执行本文件前，先读取本 skill 的 `references/data-query-order.md`、`references/cn-markdown-formatting.md`、`references/cn-pptx-formatting.md`；本文件只描述业务 workflow 或参考口径，不承载新增中文格式正文。

# 行业种子公司参考

当用户只指定行业、没有指定具体公司时，使用这些种子清单启动公司 universe 构建。这些只是起点；必须始终通过 `get_competitors_from_identifiers` 扩展，并用 `get_info_from_identifiers` 核验。

> **下方所有种子都已通过 S&P Global 标识符系统核验。** 如果某个种子无法解析，请先尝试括号中的别名，再决定是否剔除。

## 科技 / 软件

### AI / 机器学习
种子：OpenAI, Anthropic, Databricks, Scale AI, Cohere, Hugging Face, Mistral AI, xAI, Perplexity AI, Runway ML（别名："Runway AI, Inc."）, Together AI（别名："Together Computer, Inc."）, Character.ai（别名："Character Technologies, Inc."）, Groq, Stability AI, Aleph Alpha, Magic AI

⚠️ **排除项（不要作为种子使用）：**
- *Inflection AI* — 核心团队已被 Microsoft 吸收（2024 年 3 月）。存在历史融资轮次，但没有新的独立活动。
- *Adept AI* — 大部分团队已被 Amazon 吸收（2024 年）。原因同上。
- *DeepMind* — Alphabet 子公司。没有独立融资轮次。

### 网络安全
种子：CrowdStrike, Palo Alto Networks, Wiz, Snyk, SentinelOne, Abnormal Security, Netskope

### 云基础设施 / DevTools
种子：Snowflake, HashiCorp, Datadog, Confluent, Vercel, Supabase, PlanetScale

### 金融科技
种子：Stripe, Plaid, Brex, Ramp, Mercury, Affirm, Marqeta, Navan

### 垂直 SaaS
种子：ServiceTitan, Toast, Procore, Veeva Systems, Blend Labs

## 医疗健康 / 生命科学

### 生物科技 / 制药
种子：Moderna, BioNTech, Recursion Pharmaceuticals, Tempus AI, Insitro, AbCellera

### 数字健康
种子：Teladoc, Hims & Hers, Ro, Noom, Color Health

⚠️ **排除项（不要作为种子使用）：**
- *Cerebral* — 仍在运营，但曾面临重大监管问题；仅在用户明确要求时纳入。

### 医疗器械
种子：Intuitive Surgical, Butterfly Network, Outset Medical

⚠️ **排除项（不要作为种子使用）：**
- *Shockwave Medical* — 已被 Johnson & Johnson 收购（2024 年 5 月）。现在是子公司，没有独立融资轮次。

## 能源 / 气候

### 气候科技
种子：Redwood Materials, Form Energy, Commonwealth Fusion, Sila Nanotechnologies, Climeworks

### 清洁能源
种子：Enphase Energy, First Solar, Rivian, QuantumScape, Sunnova

## 消费

### 电商 / 平台
种子：Shopify, Faire, Whatnot, Fanatics

⚠️ **排除项（不要作为种子使用）：**
- *Temu (PDD Holdings)* — PDD Holdings 是大型上市集团，其融资活动体现在公开股票市场，而不是风险融资轮次。

### 消费社交 / 媒体
种子：Discord, Reddit, Substack

⚠️ **排除项（不要作为种子使用）：**
- *BeReal* — 已被 Voodoo 收购（2024 年 6 月）。现在是子公司。
- *Lemon8* — 品牌名 "Lemon8" 在 S&P Global 中会解析到一家小型荷兰公司（Lemon8 B.V.），**不是** 字节跳动旗下社交媒体应用。字节跳动应用均为子公司，没有独立融资轮次。不要使用。

## 工业 / 物流

### 物流 / 供应链
种子：Flexport, Samsara, Project44, FourKites

⚠️ **排除项（不要作为种子使用）：**
- *Convoy* — 已停止运营（2023 年 10 月）。该标识符仍可解析，也能看到历史融资轮次，但不会出现新的活动。

### 机器人 / 自动化
种子：Figure AI, Agility Robotics, Locus Robotics, Symbotic, Covariant

### 航天 / 航空
种子：SpaceX, Relativity Space, Rocket Lab, Planet Labs, Astra

## 标识符别名参考

一些知名品牌名与 S&P Global 中的法律实体名称不一致。如果品牌名通过 `get_info_from_identifiers` 返回空结果，请尝试别名：

| 品牌名 | S&P Global 法律实体名称 | company_id |
|---|---|---|
| Together AI | Together Computer, Inc. | C_1860042219 |
| Character.ai | Character Technologies, Inc. | C_1829047235 |
| Runway ML | Runway AI, Inc. | C_633706980 |
| Adept AI | Adept AI Labs Inc. | C_1780739313 |
| xAI | X.AI LLC | C_1863863313 |

> **提示：** 当品牌名失败时，用法律实体名称调用 `get_info_from_identifiers`。如果仍失败，该公司可能尚未被索引。最后手段是直接使用 `company_id` 作为标识符。

## 说明

- 这些清单偏向美国公司。做地域筛选（欧洲、亚洲等）时，竞品扩展步骤尤其重要。
- 对于未列出的细分小行业，请让用户提供 2-3 家示例公司作为种子。
- 始终核验种子公司是否仍然活跃且相关；公司会转型、合并或关闭。
- **刷新频率：** 这些种子应每季度审查一次。AI 行业种子尤其变化很快，受收购和新进入者影响明显。
- 标记为子公司或已被收购的种子仍可在 `get_info_from_identifiers` 中解析（status = "Operating Subsidiary"），但会返回零条融资轮次。融资查询应跳过这些公司。
