---
name: tear-sheet
description: "通过 Kensho LLM-ready API MCP server 使用 S&P Capital IQ 数据生成专业公司速览。当用户要求公司速览、公司单页、公司画像、事实表、公司快照或公司概览文档时使用本技能，尤其是用户提到具体公司名称或股票代码时。用户要求股票研究摘要、M&A 公司画像、企业发展目标画像、销售/BD 会议准备文档，或任何简洁单家公司财务摘要时也触发。本技能支持四类受众：股票研究、投资银行/M&A、企业发展，以及销售/业务发展。如果用户未指定受众，应询问。适用于上市和非上市公司。"
---

## 中文版执行契约

- 默认使用中国大陆金融语境：A股优先，港股和美股兼容；如用户指定市场、币种、会计准则或模板，以用户输入为准。
- 数据来源必须遵守插件根目录 `../../DATA_SOURCES_CN.md`：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断缺少依据时不得下结论，只在数据源发现记录中列为未覆盖数据项。
- 所有产物必须遵守插件根目录 `../../CN_OUTPUT_FORMATTING.md`：`Source Han Serif CN`、中文日期、币种/单位、图表标题、表格表头、来源、风险提示和免责声明都要按中文机构材料处理。
- 用户模板和品牌规范优先，但不得突破中文可读性、来源脚注、币种/单位/日期/口径说明这些底线。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。


## 产物合同读取与输出门槛

生成正式输出前必须读取：
- 插件根目录 `../../DATA_SOURCES_CN.md`
- 插件根目录 `../../CN_OUTPUT_FORMATTING.md`
- 插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`
- 插件根目录 `../../CN_DOCX_OUTPUT_CONTRACT.md`（当输出 DOCX/Word 文件时）
- 插件根目录 `../../DATA_QUERY_ORDER_CN.md`（当任务需要外部数据查询、行情更新、财报抓取、行业/公司/宏观/监管材料检索时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、数据缺口和人工审阅边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 若本 skill 的既有输出包含 DOCX/Word 文件，最终回复前必须确认 DOCX 文件已生成、DOCX 文件路径存在、可打开或结构校验通过，并确保最终回复包含 DOCX 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `../../DATA_QUERY_ORDER_CN.md`，先生成“数据源发现记录”，列出可用/不可用 MCP、connector、授权源和用户文件；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物。若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须遵守插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`，并包含来源、口径限制、数据缺口和人工审阅边界。


# 金融公司速览生成器

通过 S&P Global MCP 工具从 S&P Capital IQ 拉取实时数据，并将结果格式化为专业 Word 文档，生成面向不同受众的公司速览。

## 样式配置

以下是合理默认值。若要适配公司品牌，可修改本节；常见改动包括替换色板、修改字体（许多投行标准使用 Calibri）以及更新免责声明文本。

**颜色：**
- 主色（页眉横幅背景、章节标题文字）：#1F3864
- 强调色（标志性章节高亮）：#2E75B6
- 表格表头行填充：#D6E4F0
- 表格交替行填充：#F2F2F2
- 表格边框：#CCCCCC
- 页眉横幅文字：#FFFFFF

**排版（docx-js 使用半点字号）：**
- 字体族：Arial
- 公司名称：18pt 加粗（size: 36）
- 章节标题：11pt 加粗（size: 22），主色
- 正文：9pt（size: 18）
- 表格文字：8.5pt（size: 17）
- 页脚/免责声明：7pt 斜体（size: 14）
- 每个参考文件的格式说明中会指定模板级覆盖项。

**公司页眉横幅：**
- 页眉是一个海军蓝（#1F3864）横幅，跨整页宽度，公司名称为白色。
- **横幅下方的键值信息必须渲染为一个跨整页宽度的两列表格，且无边框。** 左列：公司标识（股票代码、总部、成立时间、员工数、行业）。右列：财务标识（市值、EV、股价、流通股数）。每个单元格包含同一行上的加粗标签和常规字重数值（例如 "**市值** $124.7B"）。不要把所有字段左对齐堆在单列中；这会浪费横向空间，并显得不专业。两列展开是区分专业公司速览和默认文档的最重要视觉信号。
  - **实现：** 创建 2 列表格，所有单元格设置 `borders: none` 和 `shading: none`。列宽各 50%。左列字段（股票代码、总部、成立时间、员工数）作为左侧单元格中的独立段落。右列字段（市值、EV、股价、流通股数）放在右侧单元格。每个字段是一个段落：标签用加粗文本，值用常规字重文本。
  - 每列中的具体字段按受众变化；详见参考文件的页眉规范。原则始终是：跨页面展开，而不是堆在左侧。
- **不要为页眉键值区块使用带边框表格。** 带边框表格只用于财务数据。
- 页眉中的关键指标（市值、EV、股价）应显示为行内键值对，而不是单独带边框表格。
- **股票研究受众的上市公司速览**：在公司名称横幅和必要公司元数据下方、第一张财务表或正文表格之前，放置该股票 12-24 个月原始股价图。图表不得归一化，不得重设起点为 100；必须标注最新价格、52 周区间、数据日期和来源。非上市公司按既有规则跳过股价、52 周区间、beta、股票表现和交易可比公司。

**章节标题：**
- 每个章节标题下方都有一条水平线（细线，#CCCCCC，0.5pt），用于在章节之间形成干净的视觉分隔。
- **将该线渲染为标题段落自身的底部边框**，不要为横线插入单独段落。单独段落会自带前后间距，导致章节标题下方留白过大。
- **实现：** 在 docx-js 中，通过 `paragraph.borders.bottom = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" }` 给章节标题段落添加底部边框。不要使用带单独 horizontal rule 元素的 `doc.addParagraph()`。不要使用 `thematicBreak`。边框必须位于标题段落自身，且标题段落后间距为 0pt，让横线紧贴标题文字。
- 间距：标题段落前 12pt、标题段落后 0pt、下一个内容元素前 4pt。

**项目符号格式：**
- 所有公司速览类型的项目符号内容统一使用单一符号（•）。不要在同一份或多份公司速览中混用 •、-、▸ 或编号列表。
- **综合/分析类项目符号**（业绩亮点、战略契合、整合考虑、谈话切入点）：使用缩进块样式，左缩进 360 DXA（0.25"），并为项目符号字符设置悬挂缩进。这些内容应在视觉上区别于正文；它们属于解释性内容，应与数据表和叙述段落不同。
- **关系章节中的信息类项目符号**：使用标准正文缩进（180 DXA），无悬挂缩进。
- **不要给任何项目符号章节添加左边框强调。** 左边框样式在 docx-js 中渲染不一致，并会产生视觉伪影。使用缩进和字号差异来区分标志性章节。

**表格（仅用于财务数据）：**
- 表头行：表头填充色（#D6E4F0），深色加粗文字。
- 正文行：白色 / 表格交替行填充色（#F2F2F2）交替。
- 边框：表格边框色（#CCCCCC），细线（BorderStyle.SINGLE，size 1）。
- 单元格内边距：上/下 40 DXA，左/右 80 DXA。
- 数据表按列位置统一对齐：表头行居中，首列左对齐，首列之外所有列居中。页眉下方的无边框两列 key-value 表是布局表例外，仍按页眉布局规则处理。
- 始终使用 ShadingType.CLEAR（绝不要使用 SOLID；SOLID 会导致黑色背景）。

**布局：**
- US Letter 竖版，0.75" 页边距（四边 1080 DXA）。

**数字格式：**
- 货币：美元。默认使用百万，除非公司收入 > $50B（此时使用十亿，一位小数）。单位写在列表头中（例如 "收入 ($M)"），不要写在单个单元格里。
- **表格单元格使用带逗号的纯数字，不带美元符号。** 示例：收入单元格显示 "4,916"，不是 "$4,916"。单位由列表头承载。
- 财年：使用实际年份（FY2022、FY2023、FY2024），不要用相对标签（FY-2、FY-1）。
- 负数：使用括号，例如 (2.3%)。
- 百分比：一位小数。
- 大数字：使用逗号作为千分位分隔符。

**页脚（文档页脚，不是正文行内文本）：**
将来源归因和免责声明放在真实文档页脚中（每页重复），不要作为正文底部的行内文字。页脚固定为两行，居中，出现在每一页：
- 第 1 行：“数据：S&P Capital IQ，经 Kensho 提供 | 分析：AI 生成 | [年-月-日]”
- 第 2 行：“仅供信息参考。不构成投资建议。”
- 样式：7pt 斜体，居中，#666666 文字色。
- 同一家公司所有公司速览类型的页脚文字必须完全一致。不要因受众不同改变措辞。
- **每份公司速览、每类受众、每一页都必须有该页脚。** 不要省略。

## 组件函数

**必须使用以下准确函数创建文档元素。不要写自定义 docx-js 样式代码。** 将这些函数复制到生成的 Node 脚本中并调用。上方样式配置文字作为文档说明；这些函数是执行机制。

```javascript
const docx = require("docx");
const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType,
  Header, Footer, PageNumber, HeadingLevel, TableLayoutType,
  convertInchesToTwip
} = docx;

// ── 颜色常量 ──
const COLORS = {
  PRIMARY: "1F3864",
  ACCENT: "2E75B6",
  TABLE_HEADER_FILL: "D6E4F0",
  TABLE_ALT_ROW: "F2F2F2",
  TABLE_BORDER: "CCCCCC",
  HEADER_TEXT: "FFFFFF",
  FOOTER_TEXT: "666666",
};

const FONT = "Arial";

// ── 1. createHeaderBanner ──
// 返回 docx 元素数组：[横幅段落，键值表]
function createHeaderBanner(companyName, leftFields, rightFields) {
  // leftFields / rightFields: arrays of { label: string, value: string }
  const banner = new Paragraph({
    children: [
      new TextRun({
        text: companyName,
        bold: true,
        size: 36, // 18pt
        color: COLORS.HEADER_TEXT,
        font: FONT,
      }),
    ],
    shading: { type: ShadingType.CLEAR, color: "auto", fill: COLORS.PRIMARY },
    spacing: { after: 0 },
    alignment: AlignmentType.LEFT,
  });

  function buildCellParagraphs(fields) {
    return fields.map(
      (f) =>
        new Paragraph({
          children: [
            new TextRun({ text: f.label + "  ", bold: true, size: 18, font: FONT }),
            new TextRun({ text: f.value, size: 18, font: FONT }),
          ],
          spacing: { after: 40 },
        })
    );
  }

  const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
  const noShading = { type: ShadingType.CLEAR, color: "auto", fill: "FFFFFF" };

  const kvTable = new Table({
    rows: [
      new TableRow({
        children: [
          new TableCell({
            children: buildCellParagraphs(leftFields),
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: noBorders,
            shading: noShading,
          }),
          new TableCell({
            children: buildCellParagraphs(rightFields),
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: noBorders,
            shading: noShading,
          }),
        ],
      }),
    ],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });

  return [banner, kvTable];
}

// ── 2. create章节Header ──
// Returns a single Paragraph with bottom border rule
function create章节Header(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 22, // 11pt
        color: COLORS.PRIMARY,
        font: FONT,
      }),
    ],
    spacing: { before: 240, after: 0 }, // 12pt before, 0pt after
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    },
  });
}

// ── 3. createTable ──
// 表头：string[]，行：string[][]，选项：{ accentHeader?, fontSize? }
function createTable(headers, rows, options = {}) {
  const fontSize = options.fontSize || 17; // 8.5pt 默认
  const headerFill = options.accentHeader ? COLORS.ACCENT : COLORS.TABLE_HEADER_FILL;
  const headerTextColor = options.accentHeader ? COLORS.HEADER_TEXT : "000000";

  const cellBorders = {
    top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    left: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    right: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
  };

  const cellMargins = { top: 40, bottom: 40, left: 80, right: 80 };

  // 表头行
  const headerRow = new TableRow({
    children: headers.map(
      (h) =>
        new TableCell({
          children: [
            new Paragraph({
              children: [
                new TextRun({
                  text: h,
                  bold: true,
                  size: fontSize,
                  color: headerTextColor,
                  font: FONT,
                }),
              ],
              alignment: AlignmentType.CENTER,
            }),
          ],
          shading: { type: ShadingType.CLEAR, color: "auto", fill: headerFill },
          borders: cellBorders,
          margins: cellMargins,
        })
    ),
  });

  // 带交替底纹的数据行
  const dataRows = rows.map((row, rowIdx) => {
    const fill = rowIdx % 2 === 1 ? COLORS.TABLE_ALT_ROW : "FFFFFF";
    return new TableRow({
      children: row.map((cell, colIdx) => {
        const align = colIdx === 0 ? AlignmentType.LEFT : AlignmentType.CENTER;
        return new TableCell({
          children: [
            new Paragraph({
              children: [
                new TextRun({ text: cell, size: fontSize, font: FONT }),
              ],
              alignment: align,
            }),
          ],
          shading: { type: ShadingType.CLEAR, color: "auto", fill: fill },
          borders: cellBorders,
          margins: cellMargins,
        });
      }),
    });
  });

  return new Table({
    rows: [headerRow, ...dataRows],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

// ── 4. createBulletList ──
// items: string[], style: "synthesis" | "informational"
function createBulletList(items, style = "synthesis") {
  const indent =
    style === "synthesis"
      ? { left: 360, hanging: 180 }   // 360 DXA left, hanging indent for bullet
      : { left: 180 };                 // 180 DXA, no hanging

  return items.map(
    (item) =>
      new Paragraph({
        children: [
          new TextRun({ text: "•  ", font: FONT, size: 18 }),
          new TextRun({ text: item, font: FONT, size: 18 }),
        ],
        indent: indent,
        spacing: { after: 60 },
      })
  );
}

// ── 5. createFooter ──
// date: string (e.g., "February 23, 2026")
function createFooter(date) {
  return new Footer({
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: `数据：S&P Capital IQ，经 Kensho 提供 | 分析：AI 生成 | ${date}`,
            italics: true,
            size: 14, // 7pt
            color: COLORS.FOOTER_TEXT,
            font: FONT,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: "仅供信息参考。不构成投资建议。",
            italics: true,
            size: 14,
            color: COLORS.FOOTER_TEXT,
            font: FONT,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
    ],
  });
}
```

**生成脚本中的用法：**
1. 将上方全部函数和常量复制到生成的 Node.js 脚本中。
2. 调用 `createHeaderBanner(...)`，不要手动构建横幅段落和表格。
3. 每个章节标题都调用 `create章节Header(...)`，绝不要手动设置段落边框。
4. 所有表格数据都调用 `createTable(...)`，包括财务摘要、交易可比公司、M&A 活动、关系表、融资历史等。IB/M&A 模板中的 M&A 活动表传入 `{ accentHeader: true }`。该函数按列位置统一对齐：表头居中、首列左、其余列居中。
5. 对业绩亮点、战略契合、整合考虑和谈话切入点调用 `createBulletList(items, "synthesis")`。
6. 对关系条目调用 `createBulletList(items, "informational")`。
7. 将 `createFooter(date)` 传给 Document 构造函数的 `footers.默认` 属性。

**这些函数会消除：**
- 黑底表格（全局强制 `ShadingType.CLEAR`）。
- 章节标题下方单独横线段落（强制在标题段落自身使用 `border.bottom`）。
- 页眉中带边框的键值表格（强制 `borders: none`）。
- 不一致的项目符号样式（强制只使用 `•`）。
- 缺失页脚（提供准确页脚结构）。

## 工作流

### 步骤 1：识别输入

继续前最多收集四项信息：

1. **公司** — 名称或股票代码。如果只有股票代码，用初始查询解析完整公司名称（例如使用公司信息工具）。
2. **受众** — 四类之一：
   - **股票研究** — 面向评估投资的买方/卖方分析师。
   - **IB / M&A** — 面向在交易语境中分析公司的投行人士。
   - **公司发展 / 并购拓展** — 面向评估收购目标的内部战略团队。
   - **销售 / BD** — 面向准备客户会议的商业团队。
3. **可比公司**（可选）— 如果用户有特定可比公司，记录下来。否则技能会从 S&P Global 数据识别同业。这对股票研究、IB/M&A 和企业发展公司速览很重要。
4. **页数偏好**（可选）— 默认值按受众变化（见下文），但用户可覆盖。

如果用户未指定受众，询问用户。

### 步骤 2：读取受众特定参考文件

从本技能目录读取对应参考文件：

- 股票研究 → `references/equity-research.md`
- IB / M&A → `references/ib-ma.md`
- 公司发展 / 并购拓展 → `references/corp-dev.md`
- 销售 / BD → `references/sales-bd.md`

每个参考文件定义章节、查询计划、格式指引和默认页数。

### 步骤 3：通过 S&P Global MCP 拉取数据

**首先：** 创建中间文件目录：
```bash
mkdir -p /tmp/tear-sheet/
```

使用 **S&P Global** MCP 工具（也称 Kensho LLM-ready API）。Codex 将能访问用于财务数据、公司信息、市场数据、一致预期、业绩会文字记录、M&A 交易和商业关系的结构化工具。每个参考文件中的查询计划会说明每个章节需要检索哪些数据；将其映射到当前对话中可用的 S&P Global 工具。

**每个查询步骤后，立即将获取的数据写入参考文件查询计划指定的中间文件。** 不要延后写入；落盘数据可防止长对话中的上下文退化。

**查询策略：**
每个参考文件都包含 4-6 个数据检索步骤的查询计划。这些是起点，不是僵硬约束。数据完整性优先于减少调用次数：

- **始终拉取 4 个财年财务数据**，即使只展示 3 年。第 4 个（最早）年份用于计算第一个展示年份的同比收入增长。没有它，最早年份增长率会显示 "N/A"，看起来像缺失数据，而不是设计选择。
- 按查询计划执行，使用能够匹配所需数据的 S&P Global 工具。
- 如果某次工具调用返回不完整结果，尝试替代工具或更窄查询。例如 company summary 不含分部细节时，直接尝试 segments 工具。
- 如果有针对性重试后仍未返回某个数据点，继续推进，并标注为 "N/A" 或“未披露”。
- 绝不要编造数据。如果工具没有返回数字，不要用训练知识估算。

**用户指定的可比公司：** 如果用户提供了可比公司，应逐个明确查询其财务数据和倍数。如果未提供可比公司，使用工具返回的同业数据，或通过竞争对手工具从公司所在行业识别同业。

**来自用户的可选语境：** 留意用户自然提供的额外语境。如果他们提到收购方是谁（“我们正为自己的平台评估这家公司”）、他们销售什么（“我们向银行销售数据分析产品”）、或潜在买方是谁（“这家公司可能会吸引 Salesforce 或 Microsoft”），将这些语境纳入相关综合章节（战略契合、谈话切入点、交易角度）。不要主动追问这些信息；若用户提供则使用。

**非上市公司处理：**
CIQ 包含非上市公司数据，因此查询方式相同。但预期结果更稀疏。为非上市公司生成时：
- 跳过：股价、52 周区间、beta、股票表现、一致预期、交易可比公司。
- 重点放在：业务概览、关系、所有权结构、可获取的财务数据。
- 在页眉醒目标注 "Private Company"。

### 步骤 3b：计算派生指标

所有数据收集完成且中间文件写入后，在一个专门步骤中计算全部派生指标。这是纯计算步骤，不做新的 MCP 查询。

**将所有中间文件重新读回上下文**，然后计算：

- **利润率：** 毛利率 %、EBITDA 利润率 %、FCF 利润率 %、经营利润率 %。
- **增长率：** 同比收入增长、同比分部收入增长、同比 EPS 增长。
- **效率比率：** FCF 转化率（FCF/EBITDA）、R&D 占收入比例、Capex 占收入比例。
- **资本结构：** 净债务（总债务 − 现金及等价物）、净债务 / EBITDA。
- **分部结构：** 每个分部收入占合并总收入比例（按数据完整性规则 8，以合并收入为分母）。

**校验（从算术校验移至此处）：** 本计算步骤中执行所有算术检查：

- **利润率计算：** 核验 EBITDA 利润率 = EBITDA / 收入，毛利率 = 毛利 / 收入等。如果计算利润率与原始数字不匹配，使用基于原始组成部分的计算值。
- **增长率：** 核验同比增长 =（本期 − 上期）/ 上期。如果已有底层值，不要依赖预先计算的增长率。
- **分部合计：** 如果展示按分部收入，核验分部合计与总收入一致（允许四舍五入误差）。如果不一致，省略合计行，而不是发布不一致数学结果。
- **百分比列：** 核验“占总额比例”列合计约为 100%。
- **估值交叉检查：** 如果同时展示 EV 和 EV/收入，核验 EV / 收入 ≈ 所示倍数。

如果校验失败：尝试从原始数据重新计算。如果仍不一致，将该指标标记为 "N/A"，不要发布错误数字。公司速览中隐蔽的数学错误会摧毁可信度。

**将结果写入** `/tmp/tear-sheet/calculations.csv`，列为：`metric,value,formula,components`

示例行：
```
metric,value,formula,components
gross_margin_fy2024,72.4%,gross_profit/revenue,"9524/13159"
revenue_growth_fy2024,12.3%,(current-prior)/prior,"13159/11716"
net_debt_fy2024,2150,total_debt-cash,"4200-2050"
```

### 步骤 3c：核验数据文件

生成文档前，核验所有中间文件存在且有内容。

**通过单独读取操作读取每个中间文件**，并打印核验摘要：

```
=== 公司速览数据核验 ===
company-profile.txt: ✓（12 个字段）
financials.csv:      ✓（36 行）
segments.csv:        ✓（8 行）
valuation.csv:       ✓（5 行）
calculations.csv:    ✓（18 行）
earnings.txt:        ✓（已填充）
relationships.txt:   ⚠ 缺失
peer-可比公司.csv:      ✓（12 行）
================================
```

**软门禁：** 如果当前受众类型预期使用的任何文件缺失或为空，打印警告但继续。公司速览会用 "N/A" 和跳过章节优雅处理缺失数据。不过警告可确保清楚知道哪些数据丢失。

**关键规则：文件，而不是你对早先对话的记忆，是文档中每个数字的唯一事实来源。** 在步骤 4 生成 DOCX 时，从中间文件读取值。不要依赖对话上下文中的财务数据。

### 步骤 4：格式化为 DOCX

使用 Codex Documents 技能或当前会话可用的 DOCX 工具创建文档；应用上方样式配置，以及参考文件中的章节特定格式。

**默认页数（用户可覆盖）：**
- 股票研究：1 页（高密度是惯例）。
- IB / M&A：1-2 页。
- 企业发展：1-2 页。
- 销售 / BD：1-2 页。

如果内容超过目标，每个参考文件都说明了先删哪些章节。

**输出文件名：** `[公司名称]_公司速览_[受众]_[YYYYMMDD].docx`  
示例：`Nvidia_公司速览_企业发展_20260220.docx`

保存到 `/mnt/用户-data/outputs/` 并呈现给用户。

## 数据完整性规则

这些规则覆盖其他所有内容：
1. **S&P Global 工具是财务数据的唯一来源。** 不要用训练知识填补缺口；它可能过期或错误。
2. **标注无法找到的内容。** 使用“N/A”或“未披露”，不要静默省略行。
3. **日期重要。** 标注财年结束日或报告期间。不要假设日历年 = 财年。市场数据（股价、市值）应包含“截至”日期。
4. **不要混用报告期间。** 如果有 FY2023 收入和 LTM EBITDA，应分别清楚标注。
5. **优先使用 MCP 返回字段，而非手工计算。** 如果 S&P Global 工具返回预计算字段（例如净债务、EBITDA、FCF），直接使用该值，而不是从组成部分计算。只有工具不返回字段时才手工计算派生指标。这能减少差异。
6. **确保不同公司速览类型之间一致。** 如果同一会话为同一公司生成多份公司速览（例如股票研究和 IB/M&A），相同底层数据点在所有输出中必须产生完全相同的值。净债务、收入、EBITDA、利润率和增长率必须完全匹配。不要为每份报告独立重新查询或重新计算；复用同一组已获取值。
7. **绝不要降级已知交易价值。** 如果 M&A 工具返回某笔交易的交易价值，该值必须出现在输出中。不要把已知交易价值替换为“未披露”。只有工具确实没有返回交易价值时，才使用“未披露”。
8. **分部百分比用合并收入作分母。** 计算分部表中的“占总额比例”时，每个分部收入除以合并总收入（利润表披露口径），不要除以分部收入之和。分部收入合计常因内部抵消而超过合并收入。使用合并收入可确保百分比与文档中展示的总收入一致。
9. **可用时始终包含前瞻（NTM）倍数。** 如果工具返回过去口径和前瞻口径估值倍数，两个都必须出现在输出中。前瞻倍数是股票研究、IB/M&A 和企业发展受众的主要估值参考。可用前瞻数据时绝不要只展示过去口径倍数。
10. **没有任何 S&P Global 工具返回高管或管理层数据。** 不要用训练数据填充管理层姓名、职务或履历；这违反规则 1，并会产生过期信息。如果模板中出现管理层章节，应完全省略。只有工具返回时，才可包含所有权结构（机构持有人、内部人持股比例、PE sponsor），并用“数据允许”作为门槛。

## 中间文件规则

MCP 工具获取的所有数据都必须在生成文档前持久化到结构化中间文件。这些文件，而不是对话上下文，是文档中每个数字的唯一事实来源。

**设置：** 步骤 3 开始时创建工作目录：
```
mkdir -p /tmp/tear-sheet/
```

**查询后立即写入要求：** 每个 MCP 查询步骤完成后，立即把获取的数据写入适当中间文件。不要等所有查询结束后再写。每个参考文件的查询计划都会指定每一步后写入哪些文件。

**文件结构：**

| 文件 | 格式 | 列 / 结构 | 使用者 |
|---|---|---|---|
| `/tmp/tear-sheet/company-profile.txt` | 键值文本 | 名称、股票代码、交易所、总部、板块、行业、成立时间、员工数、市值、企业价值、股价、52 周高点、52 周低点、流通股数、beta、所有权 | 全部 |
| `/tmp/tear-sheet/financials.csv` | CSV | `period,line_item,value,来源` | 全部 |
| `/tmp/tear-sheet/segments.csv` | CSV | `period,segment_name,revenue,来源` | ER, IB, CD |
| `/tmp/tear-sheet/valuation.csv` | CSV | `metric,trailing,forward,来源` | ER, IB, CD |
| `/tmp/tear-sheet/consensus.csv` | CSV | `metric,fy_year,value,来源` | ER |
| `/tmp/tear-sheet/earnings.txt` | 结构化文本 | 季度、日期、关键引文、指引、关键驱动因素 | ER, IB, Sales |
| `/tmp/tear-sheet/relationships.txt` | 结构化文本 | 客户、供应商、合作伙伴、竞争对手 — 每项都带描述 | IB, CD, Sales |
| `/tmp/tear-sheet/peer-可比公司.csv` | CSV | `ticker,metric,value,来源` | ER, IB, CD |
| `/tmp/tear-sheet/ma-activity.csv` | CSV | `date,target,deal_value,type,rationale,来源` | IB, CD |
| `/tmp/tear-sheet/calculations.csv` | CSV | `metric,value,formula,components` | 全部（步骤 3b 写入） |

**缩写：** ER = 股票研究，IB = IB/M&A，CD = 企业发展，Sales = 销售/BD。

并非每种受众类型都使用每个文件；参考文件会定义适用查询步骤。与当前受众无关的文件不需要创建。

**只存原始值。** 中间文件保存工具返回的原始值。不要在这些文件里预先计算利润率、增长率或其他派生指标；这些在步骤 3b 完成。

**页数预算执行：** 每个参考文件都指定默认页数和编号删减顺序。如果渲染后的文档超过目标，按指定顺序删减；不要把字号或页边距压到模板最低值以下。删减顺序是严格优先级栈：完整删掉第 1 个章节后，才能动第 2 个章节。
