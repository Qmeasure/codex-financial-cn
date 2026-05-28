---
name: funding-digest
description: "生成一页精美 PowerPoint，汇总用户关注行业或公司近期融资轮次与重要资本市场活动的核心要点。当用户要求交易流摘要、周度融资回顾、融资动态、交易汇总或资本市场简报时使用本 skill。触发示例包括：“本周交易流摘要”“[行业] 周度融资回顾”“本周 [行业] 发生了什么”“交易汇总”“资本市场更新”，或任何将近期融资活动整理为简报幻灯片的请求。产出包含关键结论、估值数据和 Capital IQ 交易链接的专业单页 PPTX。"
---

## 中文版执行契约

- 默认使用中国大陆金融语境：A股优先，港股和美股兼容；如用户指定市场、币种、会计准则或模板，以用户输入为准。
- 数据来源必须遵守根目录 `DATA_SOURCES_CN.md`：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断无依据时写“需确认”。
- 所有产物必须遵守根目录 `CN_OUTPUT_FORMATTING.md`：中文字体栈、中文日期、币种/单位、图表标题、表格表头、来源脚注、风险提示和免责声明都要按中文机构材料处理。
- 用户模板和品牌规范优先，但不得突破中文可读性、来源脚注、币种/单位/日期/口径说明这些底线。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。


**AI 免责声明（强制）：**
你必须在 PowerPoint 页脚中加入以下免责声明文字。此要求不可省略；缺少该说明时，报告视为不完整：

> **“分析由 AI 生成，请确认所有输出”**

**页脚** — 在生成幻灯片底部放置醒目的黄色横幅：“分析由 AI 生成，请确认所有输出”

---

# 周度交易流摘要

生成分析师质量的**单页 PowerPoint**，使用 S&P Global Capital IQ 数据汇总用户关注行业或公司近期融资轮次的核心结论。每笔交易都链接回其 Capital IQ 页面，方便快速下钻核查。

## 何时使用

遇到以下任一请求时触发：
- “给我一份本周交易流摘要”
- “做一份 [行业] 周度融资回顾”
- “[行业/公司] 最近有哪些交易完成？”
- “交易汇总”或“融资动态”
- “我覆盖范围的资本市场更新”
- “汇总近期融资活动”
- 任何关于交易、募资或融资轮次的周期性简报请求

## 嵌套 Skills

本 skill 产出一页 PPTX 简报：
- 生成 PowerPoint 前，先使用 Codex Presentations 技能或当前会话可用的 PPTX 工具确认创建、渲染和 QA 流程。

## 实体识别与工具稳健性

S&P Global 的标识符系统会把公司名称解析为法律实体。多数公司都能正确解析，但也存在会导致空结果的已知失败模式。**整个工作流必须应用以下规则，避免静默丢失数据。**

### 规则 0：查询融资前预校验所有标识符

调用任何融资工具之前，先把每个标识符传入 `get_info_from_identifiers`。这是提前发现问题成本最低、可靠性最高的方式。检查返回中的两项：

1. **是否成功解析？** 如果标识符返回空值或错误，说明该名称在 S&P Global 中不存在。尝试 `references/sector-seeds.md` 中的别名、法律实体名称，或直接使用 `company_id`。
2. **`status` 字段是什么？**
   - `"Operating"` → 可以安全查询融资轮次。
   - `"Operating Subsidiary"` → 公司存在但由母公司持有。它会返回**零个融资轮次**。在摘要中作为背景说明（例如“已被 [母公司] 收购”），但不要查询其融资。
   - 其他状态（例如已关闭、非活跃）→ 公司已不再运营。可能存在历史数据，但不会有新的融资活动。

**这一步预校验可以避免大多数空结果问题。** 将所有候选公司批量放入一次 `get_info_from_identifiers` 调用中（该工具能很好处理大批量），然后先分流再继续。

### 规则 1：没有 fallback 前，不要信任空结果

如果 `get_rounds_of_funding_from_identifiers` 对一个预期有数据的公司返回空结果：
1. **尝试法律实体名称或 `company_id`。** 品牌名通常可用，但并非总是可用。已知不匹配项见 `references/sector-seeds.md` 的别名表。常见模式是：“[品牌] AI” → “[法律名称], Inc.”（例如 Together AI → “Together Computer, Inc.”，Character.ai → “Character Technologies, Inc.”，Runway ML → “Runway AI, Inc.”）。
2. **验证该公司是否存在于 S&P。** 如果跳过了规则 0，现在调用 `get_info_from_identifiers(identifiers=["Company"])`；如果这里也返回空，说明公司可能阶段太早或尚未被收录。

### 规则 2：子公司没有独立融资轮次

大型公司旗下部门或全资子公司（例如 Alphabet 旗下 DeepMind、Microsoft 旗下 GitHub、Voodoo 旗下 BeReal）会返回**零个融资轮次**。它们的资本事件通常在母公司层面追踪。

**检测方式：** `get_info_from_identifiers` 返回的 `status` 字段会显示 `"Operating Subsidiary"`。`references/sector-seeds.md` 也会用 ⚠️ 标记已知子公司。融资查询时跳过这些公司。

### 规则 3：以 `get_rounds_of_funding_from_identifiers` 为主工具，而不是 `get_funding_summary_from_identifiers`

摘要工具速度更快，但可靠性较低；即使存在详细融资轮次，它也可能返回错误或不完整数据。始终把详细轮次工具作为主要数据来源。摘要工具只适合快速做聚合检查（总融资额、轮次数），且当结果偏低时必须用轮次工具核验。

### 规则 4：谨慎批处理并校验

处理大型公司池（50+ 家公司）时，每批 15–20 家。每批完成后检查返回空结果的公司，并先执行规则 1 中的 fallback，再继续下一批。

### 规则 5：`role` 参数至关重要

- `company_raising_funds` → “X 公司融资了哪些轮次？”（公司视角）
- `company_investing_in_round_of_funding` → “投资人 Y 投了哪些项目？”（投资人视角）

用错 role 会静默返回空结果。交易流摘要几乎总是使用 `company_raising_funds`。只有在明确分析某个投资人的组合活动时，才使用投资人 role。

### 规则 6：标识符解析不区分大小写，但严格依赖拼写

S&P Global 能处理大小写差异（“openai” = “OpenAI”），但对拼写和标点很严格。“Character AI” 可能失败，而 “Character.ai” 成功。不确定时使用 `company_id`（例如 `C_1829047235`），它可以保证解析。

## 工作流

### 步骤 1：确定覆盖范围与期间

确定摘要应覆盖什么内容。存在两种情况：

**老用户（已有关注清单）：**
如果用户此前已经定义过需要跟踪的行业或公司，使用该清单。检查对话历史中的既有 watchlist。

**新用户：**
询问以下信息：

| 参数 | 默认值 | 说明 |
|-----------|---------|-------|
| **行业** | *至少一个* | 例如“AI、金融科技、生物医药” |
| **具体公司** | 可选 | 补充行业层面的覆盖 |
| **时间区间** | 最近 7 天 | “本周”“最近 2 周”“本月” |

根据时间区间计算精确的 `start_date` 和 `end_date`。

### 步骤 2：构建公司池

对每个指定行业，使用经校验的自举方法构建公司池：

1. 使用领域知识提供**种子公司**（见 `references/sector-seeds.md`）
   - 注意 seeds 文件中的 ⚠️ 警告和别名说明；一些知名公司是子公司、已被收购，或必须使用特定法律名称才能解析。
   - seeds 文件为已知别名不匹配项提供了 `company_id`。如果品牌名失败，直接使用这些 ID。

2. **立即预校验所有种子公司**（规则 0）：
   ```
   get_info_from_identifiers(identifiers=[all_seeds_for_this_sector])
   ```
   将结果分成两个桶：
   - ✅ **已解析且仍在运营**（`status` = "Operating"）→ 继续扩展竞争对手
   - ❌ **未解析或子公司** → 使用 seeds 文件中的别名/法律名称重试；子公司只作为背景说明，排除在融资查询之外

3. **通过竞争对手扩展**（只使用 ✅ 已解析种子）：
   ```
   get_competitors_from_identifiers(identifiers=[resolved_seeds], competitor_来源="all")
   ```

4. **校验扩展后的公司池：**
   ```
   get_info_from_identifiers(identifiers=[new_competitors])
   ```
   应用相同分流规则。按与目标行业匹配的 `simple_industry` 过滤。删除所有未解析公司和子公司。

如果用户提供具体公司，直接加入公司池，但仍必须做预校验分流。不要跳过校验；即使是知名品牌名，也可能静默失败。

保持公司池规模可控：每个行业目标为 15–40 家**已解析、仍在运营**的公司。多行业摘要总量可能达到 50–100+ 家公司。

### 步骤 3：拉取融资轮次

对公司池中的所有公司执行：

```
get_rounds_of_funding_from_identifiers(
    identifiers=[batch],
    role="company_raising_funds",
    start_date="YYYY-MM-DD",
    end_date="YYYY-MM-DD"
)
```

如果公司池较大，按每批 15–20 家处理。

**每批之后，识别返回空结果的公司。** 对任何预期应有活动的公司：
1. 使用法律实体名称或替代标识符重试（见上方实体识别规则）。
2. 只有在 fallback 用尽后，才将该公司记录为“无数据”。

收集成功结果中的所有 `transaction_id`，然后用详细轮次信息补充：

```
get_rounds_of_funding_info_from_transaction_ids(
    transaction_ids=[all_funding_ids]
)
```

把所有 transaction ID 放入一次调用（或少量调用），而不是每笔交易调用一次；该工具能高效处理批量。

**从每笔融资中提取以下字段（对幻灯片至关重要）：**
- `transaction_id` — Capital IQ 交易链接所需
- **公告日** — 该轮融资公开宣布的日期
- **交割日** — 该轮融资正式完成的日期
- 募集金额
- **投前估值**（如披露）
- **投后估值**（如披露）
- 领投方
- 轮次类型（Series A、B、C 等）
- SAFE 条款
- 顾问
- 定价趋势（up-round / down-round / flat）

> **日期为必填。** 公告日和交割日必须始终出现在最终幻灯片的交易表中。如果只有一个日期可用，展示该日期，并将另一个标为“—”。

### 步骤 4：为重要交易拉取公司背景

对涉及重要交易的公司（大额融资、估值显著变化等），获取简短描述：

```
get_company_summary_from_identifiers(identifiers=[notable_companies])
```

这会为叙事补充背景（例如“该公司是一家成立于 2021 年的 AI 基础设施初创公司，正在扩展至……”）。

### 步骤 5：识别亮点与趋势

设计幻灯片前，先分析数据并提炼故事线：

**标记为“重要”的情况：**
- 单轮融资 ≥ 1 亿美元
- Down round（定价趋势 = down）
- 新独角兽（投后估值跨过 10 亿美元）
- 估值显著跃升（投后估值 ≥ 上一轮已知估值的 2 倍）
- 短期重复融资（同一公司 6 个月内再次融资）
- 投资人 syndicate 异常庞大

**识别趋势：**
- 本期总资本投放量相对典型水平的变化（如果有历史数据）
- 哪些子行业最热（轮次数最多、融资金额最高）
- 融资阶段分布（早期还是后期占主导？）
- 摘要覆盖范围内最活跃的投资人
- 地理集中度
- 估值趋势（投前估值在压缩还是扩张？）

**选择关键结论（3–5 条）：**
将最重要的信号提炼为 3–5 条简洁 bullet 风格结论。这些结论是幻灯片中心内容。每条结论应为一句话，表达有力，并由数据支撑。

示例：
- “AI 行业本周 8 轮融资合计 24 亿美元，为上周 3 倍；[公司] 以 120 亿美元投后估值完成 8 亿美元 mega-round，成为主要驱动。”
- “[公司] 完成 2 亿美元 Series D，投前估值 35 亿美元，高于 Series C 的 18 亿美元，显示 AI 开发者工具需求仍强。”
- “Down round 活动升温：6 笔后期轮次中有 2 笔低于上一轮估值定价。”

### 步骤 6：生成公司 Logo

为关键结论或重要交易中出现的每家公司生成 logo，使用两层本地 pipeline。**不要使用 Clearbit**（`logo.clearbit.com`）；它已废弃且稳定失败。外部 logo CDN（Brandfetch、logo.dev、Google Favicons）通常需要 API key 或会被网络限制阻断。改用以下方式：

#### 第一层：`simple-icons` npm 包（3,300+ 品牌 SVG，无需网络）

`simple-icons` 包内置数千个知名品牌的高质量 SVG 图标。它完全离线运行，不需要 API key，也不需要网络调用。配合 `sharp` 做 SVG → PNG 转换：

```bash
npm install simple-icons sharp
```

**查找策略：**

```javascript
const si = require('simple-icons');
const sharp = require('sharp');

// 通过精确标题匹配查找 icon（不区分大小写）
function findSimpleIcon(companyName) {
    // 先尝试精确匹配
    for (const [key, val] of Object.entries(si)) {
        if (!key.startsWith('si') || !val || !val.title) continue;
        if (val.title.toLowerCase() === companyName.toLowerCase()) return val;
    }
    // 再尝试移除常见后缀（AI、Inc.、Corp.）
    const stripped = companyName.replace(/\s*(AI|Inc\.?|Corp\.?|Ltd\.?)$/i, '').trim();
    if (stripped !== companyName) {
        for (const [key, val] of Object.entries(si)) {
            if (!key.startsWith('si') || !val || !val.title) continue;
            if (val.title.toLowerCase() === stripped.toLowerCase()) return val;
        }
    }
    return null;
}

// 使用品牌官方颜色把 SVG 转为 PNG
async function simpleIconToPng(icon, outputPath) {
    const coloredSvg = icon.svg.replace('<svg', `<svg fill="#${icon.hex}"`);
    await sharp(Buffer.from(coloredSvg))
        .resize(128, 128, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
        .png()
        .toFile(outputPath);
}
```

**覆盖率：** 典型交易流公司约 43% 可覆盖（对 Stripe、Anthropic、Databricks、Snowflake、Discord、Shopify、SpaceX、Mistral AI、Hugging Face 等大型科技品牌覆盖较好；对垂直金融科技、生物医药或早期公司覆盖较弱）。

#### 第二层：通过 `sharp` 生成首字母兜底 Logo（100% 覆盖）

对 `simple-icons` 未命中的公司，生成干净的首字母 PNG logo：

```javascript
async function generateInitialLogo(companyName, outputPath) {
    const initial = companyName.charAt(0).toUpperCase();
    const svg = `
    <svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
        <circle cx="64" cy="64" r="64" fill="#BDBDBD"/>
        <text x="64" y="64" font-family="Arial, Helvetica, sans-serif"
              font-size="56" font-weight="bold" fill="#FFFFFF"
              text-anchor="middle" dominant-baseline="central">${initial}</text>
    </svg>`;
    await sharp(Buffer.from(svg)).png().toFile(outputPath);
}
```

#### 完整 Pipeline

```javascript
async function fetchLogo(companyName, outputDir) {
    const fileName = companyName.toLowerCase().replace(/[\s.]+/g, '-') + '.png';
    const outPath = path.join(outputDir, fileName);

    // 第一层：尝试 simple-icons
    const icon = findSimpleIcon(companyName);
    if (icon) {
        await simpleIconToPng(icon, outPath);
        return { path: outPath, source: 'simple-icons' };
    }

    // 第二层：生成首字母兜底
    await generateInitialLogo(companyName, outPath);
    return { path: outPath, source: 'initial-fallback' };
}
```

**Logo 规范：**
- 所有 logo 保存至当前工作区的 `out/logos/[company-name].png`
- 所有 logo 为 128×128 PNG，透明背景
- 幻灯片中 logo 高度设为 0.35"–0.5"；它们是点缀，不是视觉焦点
- 首字母兜底圆形使用灰色（`BDBDBD`）填充、白色文字，与单色调色板保持一致
- 不要随机混用 logo 风格；如果多数公司使用品牌 icon，少数兜底也应自然融入

### 步骤 7：生成单页 PPTX

创建幻灯片前，确认当前会话可用的 PPTX 创建工具、渲染工具和 QA 流程。

使用 `pptxgenjs` 创建**单页** PowerPoint。幻灯片应信息密度高但视觉清爽：像“高管仪表盘”，而不是“文字墙”。

#### 幻灯片布局

```
┌─────────────────────────────────────────────────────────────┐
│  交易流摘要                                                  │
│  [期间] · [行业]                                [日期]       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  $X.XB  │  │  N      │  │  $X.XB  │  │  $X.XB  │       │
│  │ 融资额  │  │ 轮次数  │  │平均投前 │  │最大轮次 │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                             │
│  关键结论                                                    │
│  ─────────────────────────────────────────────────          │
│  [Logo] 结论 1 文案……                                       │
│  [Logo] 结论 2 文案……                                       │
│  [Logo] 结论 3 文案……                                       │
│  [Logo] 结论 4 文案……                                       │
│                                                             │
│  重点交易                                                    │
│  ┌──────────────────────────────────────────────────────────┐│
│  │公司│轮次│公告日│交割日│金额│投前│投后│领投方│🔗│        │
│  │────│────│──────│──────│────│────│────│──────│──│        │
│  │ ...│ ...│ ...  │ ...  │ ...│ ...│ ...│ ...  │🔗│        │
│  └──────────────────────────────────────────────────────────┘│
│                                                             │
│  [页脚：交易流摘要 · 来源：S&P Global Capital IQ]           │
│  [页脚：AI 免责声明]                                        │
└─────────────────────────────────────────────────────────────┘
```

#### 设计规范

**色彩原则：极简、单色优先。** 幻灯片应呈现高端金融简报质感，主要使用黑、白、灰。颜色**只在承载含义时使用**（例如 down round 用红色标记，突出指标用绿色标记），或用于读者自然预期的元素（公司 logo）。不要把颜色用于背景填充、强调条、渐变等纯装饰用途。

**调色板 — 单色高管风格：**
- 主背景：`FFFFFF`（白色）— 清爽、开放的幻灯片底色
- 标题栏：`1A1A1A`（近黑色）— 为标题区域提供强对比
- 主文字：`1A1A1A`（近黑色）— 正文、指标数字、关键结论
- 次级文字：`6B6B6B`（中灰）— 标签、说明、页脚、日期
- 边框与分隔线：`D0D0D0`（浅灰）— 细结构线、卡片边框、表格边框
- 卡片背景：`F5F5F5`（类白/极浅灰）— 指标卡片、表格隔行底色
- 链接文字：`2B5797`（克制蓝）— 表格中的 Capital IQ 交易链接（整页唯一蓝色）
- **语义色（谨慎使用）：**
  - Down round 或负面信号：`C0392B`（克制红）— 只作为小圆点、标签或单词高亮；绝不要作为填充或背景
  - 突出正面指标（新独角兽、超大额融资）：`2E7D32`（克制绿）— 同样只用在小圆点、小标签或单个高亮数字
  - 如果没有数据点需要颜色提示，**不要使用颜色**。全单色幻灯片完全正确。

**排版：**
- 标题：28–32pt，加粗，近黑标题栏上的白色文字
- 指标数字：36–44pt，加粗，近黑
- 指标标签：10–12pt，中灰（`6B6B6B`）
- 关键结论文字：12–14pt，近黑，左对齐
- 表格文字：9–11pt，近黑；次要列用灰色（`6B6B6B`）
- 链接文字：9–10pt，克制蓝（`2B5797`）
- 页脚：8pt，中灰

**指标卡片（顶部行）：**
- 4 个关键指标作为大数字 callout：总融资额、轮次数、平均投前估值、最大单轮融资
- 每个指标放入 `F5F5F5` 填充、细 `D0D0D0` 边框的卡片；无阴影、无彩色填充
- 如果某个指标异常或极端（例如成交量为正常水平 3 倍、创纪录交易），可在单个数字旁放置小色点或下划线；否则保持全单色
- 如果多数交易未披露投前估值，用其他指标替代（例如融资金额中位数、新独角兽数量）

**关键结论（中部）：**
- 3–5 条单行结论，每条前置相关公司 logo（小号，约 0.35" 高）
- 如果没有 logo，使用**灰色圆形**加白色公司首字母，而不是彩色圆形
- 左对齐，并保留足够行距
- Down round 或负面结论可使用小红点前缀；其他情况不使用颜色
- 如有估值数据，加入估值上下文（例如“投后估值 50 亿美元”）

**重点交易表（底部）：**
- 紧凑表格，展示 4–6 笔最重要交易
- 列：公司、轮次类型（Series X）、公告日、交割日、金额（$M）、投前估值（$M）、投后估值（$M）、领投方、交易链接
- **公告日**和**交割日**列使用中文日期格式（例如“1月15日”）。这两列必填且必须始终存在。如果日期不可得，显示“—”。
- **交易链接**列包含可点击文字“查看 →”，链接到 Capital IQ：
  ```
  https://www.capitaliq.spglobal.com/web/client?#offering/capitalOfferingProfile?id=<transaction_id>
  ```
  其中 `<transaction_id>` 来自 `get_rounds_of_funding_from_identifiers` 返回的 `transaction_id`。
- 如果未披露投前或投后估值，对应单元格显示“—”
- 表头行使用近黑（`1A1A1A`）填充与白色文字；表体用 `F5F5F5` 和 `FFFFFF` 隔行
- **表格在幻灯片中水平居中。** 计算表格总宽度，然后设置 `x`，使其居中于幻灯片宽度：`x = (slideWidth - tableWidth) / 2`。对 16:9 布局（13.33" 宽），如果表格宽 12"，使用 `x = 0.67`。不要把表格贴到幻灯片左边缘。
- 保持紧凑；这部分是参考信息，不是视觉焦点
- 表格单元格不使用彩色填充。如果某笔交易是 down round，可在金额旁加入小红色文字标签“（↓ 下调）”；这是表格中唯一允许的颜色。

**交易链接实现（pptxgenjs）：**
在 pptxgenjs 中，使用单元格对象的 `options.hyperlink` 属性为表格单元格添加超链接：
```javascript
// 带 Capital IQ 交易链接的表格单元格
{
  text: "查看 →",
  options: {
    hyperlink: {
      url: `https://www.capitaliq.spglobal.com/web/client?#offering/capitalOfferingProfile?id=${transactionId}`
    },
    color: "2B5797",
    fontSize: 9,
    fontFace: "Arial"
  }
}
```

**表格居中（pptxgenjs）：**
始终将交易表在幻灯片上居中。动态计算 x 坐标：
```javascript
const SLIDE_W = 13.33; // 16:9 幻灯片宽度
const TABLE_W = 12.5;  // 表格总宽度（所有列宽之和）
const TABLE_X = (SLIDE_W - TABLE_W) / 2; // ≈ 0.42"

slide.addTable(tableRows, {
  x: TABLE_X,
  y: tableY,
  w: TABLE_W,
  colW: [1.8, 0.9, 0.9, 0.9, 1.0, 1.1, 1.2, 1.6, 0.7], // 公司、轮次、公告日、交割日、金额、投前、投后、领投方、链接
  // ... 其他选项
});
```
可按需调整 `colW`，但必须始终用 `(SLIDE_W - sum(colW)) / 2` 重新计算 `TABLE_X`，确保表格居中。

**页脚：**
- 使用中灰小字号文字：“交易流摘要 · [期间] · 来源：S&P Global Capital IQ · 生成日期 [日期]”

**通用颜色规则（严格执行）：**
- 公司 logo 是整页唯一允许“全彩”的元素；保持来源原貌。
- 交易链接使用克制蓝（`2B5797`）；这是除语义红/绿之外唯一的非单色文字。
- 除 logo 和链接外，幻灯片应在黑白打印时依然正确。
- 不要给背景、强调条、装饰形状或章节分隔线使用颜色。
- 不确定时，使用灰色。

#### 代码结构

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "交易流摘要";

const slide = pres.addSlide();
const SLIDE_W = 13.33; // 16:9 幻灯片宽度（英寸）

// 1. 深色标题栏，包含标题和期间
// 2. 指标卡片行（4 张卡片：总融资额、轮次数、平均投前估值、最大轮次）
// 3. 带 logo 的关键结论区（包含估值上下文）
// 4. 重点交易表，包含公告日、交割日、投前、投后列和 Capital IQ 交易链接
//    - 表格居中：x = (SLIDE_W - tableWidth) / 2
// 5. 页脚

pres.writeFile({ fileName: "out/deal-flow-digest.pptx" });
```

按照 pptxgenjs 常见陷阱指南，对阴影和重复样式使用工厂函数，不要复用同一个可变对象。

### 步骤 8：QA 幻灯片

遵循 PPTX skill 的 QA 流程：

1. **内容 QA：** `python -m markitdown deal-flow-digest.pptx` — 核对所有文字、数字、公司名称、估值数据和交易链接是否正确
2. **视觉 QA：** 转为图片并检查：
   ```bash
   soffice --headless --convert-to pdf deal-flow-digest.pptx
   pdftoppm -jpeg -r 200 deal-flow-digest.pdf slide
   ```
   检查元素重叠、文字溢出、对齐问题、低对比度文字、logo 尺寸问题，以及交易链接文字是否可见。
3. **链接 QA：** 确认表格中的 Capital IQ URL 使用了正确的 transaction ID 且格式正确。
4. **修正并重新验证** — 宣布完成前至少执行一轮“修正—复验”。

### 步骤 9：交付结果

1. 将最终 `.pptx` 复制到 `/mnt/用户-data/outputs/`
2. 使用 `present_files` 共享幻灯片
3. 提供 2–3 句口头摘要：
   - “本摘要覆盖 [行业] 的 X 笔融资，合计融资 Y。”
   - 点出最重要的一笔交易及其估值
   - 标记任何值得关注的趋势（down round、估值压缩等）

## 错误处理

### 实体识别失败
- **知名公司返回空结果：** 先检查 `get_info_from_identifiers`；如果失败，尝试 `references/sector-seeds.md` 中的别名或直接使用 `company_id`。常见品牌→法律名称不匹配包括：Together AI → “Together Computer, Inc.”，Character.ai → “Character Technologies, Inc.”，Runway ML → “Runway AI, Inc.”。
- **子公司：** DeepMind、GitHub、Instagram、WhatsApp、YouTube、BeReal 等是子公司，没有独立融资轮次。将其作为“已收购/子公司”背景说明，不要报告为“无活动”。
- **已停运公司：** Convoy 等公司（2023 年 10 月关闭）仍可在 S&P Global 中解析，但不会有新活动。`references/sector-seeds.md` 会标记这些公司；纳入前先检查。
- **`get_funding_summary_from_identifiers` 报错或返回零：** 回退到 `get_rounds_of_funding_from_identifiers`；摘要工具可靠性较低。不要把摘要工具作为唯一数据来源。
- **`role` 参数错误：** 如果投资人视角查询返回空，确认正在使用 `company_investing_in_round_of_funding`，而不是 `company_raising_funds`；反之亦然。

### 数据质量问题
- **期间内无活动：** 如果某行业在期间内没有融资轮次，在幻灯片中明确说明（“[行业] 在该期间未记录交易”）；没有活动本身也是信息。
- **估值数据稀疏：** 如果多数交易未披露投前和投后估值，在页脚注释数据限制，并在表格中使用“—”。将指标卡片调整为其他指标（例如融资金额中位数），不要使用平均投前估值。
- **Logo 获取失败：** `simple-icons` npm 包对典型交易流公司约有 43% 覆盖率。其余公司使用 `sharp` 生成首字母兜底。保持图标风格一致，不要混用随机方案。如果 `simple-icons` 或 `sharp` 安装失败，回退到基于 pptxgenjs 图形的首字母方案（灰色椭圆 + 白字），不需要外部依赖。
- **一页放不下太多交易：** 如果重要交易超过 6 笔，在表格中展示前 6 笔，并添加脚注：“另有 N 笔交易未列示。”按交易规模优先排序。
- **大型公司池：** 对 100+ 家公司的多行业摘要，所有 API 调用按 15–20 家分批。对重要交易优先做深度，不追求小额交易的完全展开。
- **种子过旧：** 如果某行业的竞争对手扩展返回结果很少，种子公司可能过于小众。增加 2–3 个更知名公司后重新扩展。
- **交易链接的 transaction ID 无效：** 如果融资工具返回的 `transaction_id` 无法生成有效 Capital IQ URL，省略该行链接单元格，不要包含坏链接。

## 示例请求

- “给我一份 AI 和金融科技的周度交易流摘要”
- “汇总本周生物医药融资情况”
- “做一份我覆盖范围的交易汇总：网络安全、云基础设施和开发者工具，时间为最近 2 周”
- “我关注的所有行业里，本周一级市场发生了什么？”
- “做一页本月 climate tech 交易流幻灯片”
