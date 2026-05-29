---
name: fsi-strip-profile
description: |
  为 pitch book、交易材料和客户演示创建专业投行 strip profile（公司简介）。生成 1-4 页信息密集型幻灯片，采用象限布局、图表和表格。
---

## 中文版执行契约

- 默认使用中国大陆金融语境：A股优先，港股和美股兼容；如用户指定市场、币种、会计准则或模板，以用户输入为准。
- 数据来源必须遵守插件根目录 `../../DATA_SOURCES_CN.md`：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断缺少依据时不得下结论，只在数据源发现记录中列为未覆盖数据项。
- 所有产物必须遵守插件根目录 `../../CN_OUTPUT_FORMATTING.md`：中文字体栈、中文日期、币种/单位、图表标题、表格表头、来源脚注、风险提示和免责声明都要按中文机构材料处理。
- 用户模板和品牌规范优先，但不得突破中文可读性、来源脚注、币种/单位/日期/口径说明这些底线。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。


## 产物合同读取与输出门槛

生成正式输出前必须读取：
- 插件根目录 `../../DATA_SOURCES_CN.md`
- 插件根目录 `../../CN_OUTPUT_FORMATTING.md`
- 插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`
- 插件根目录 `../../CN_PPTX_OUTPUT_CONTRACT.md`（当输出 PPTX/PowerPoint 文件时）
- 本 skill 本地 `references/cn-markdown-formatting.md`（聊天摘要、正式 Markdown 或最终交付说明）
- 本 skill 本地 `references/data-query-order.md`（当任务需要外部数据查询、行情更新、财报抓取、行业/公司/宏观/监管材料检索时）
- 本 skill 本地 `references/cn-pptx-formatting.md`（当输出 PPTX/PowerPoint 文件时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、数据缺口和人工审阅边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 若本 skill 的既有输出包含 PPTX/PowerPoint 文件，最终回复前必须确认 PPTX 文件已生成、PPTX 文件路径存在、可打开或结构校验通过，并确保最终回复包含 PPTX 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `references/data-query-order.md`，先生成“数据源发现记录”，列出可用/不可用 MCP、connector、授权源和用户文件；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物。若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须先读取 `references/cn-markdown-formatting.md`，并包含来源、口径限制、数据缺口和人工审阅边界。
- 生成或审查图表时，必须先读取对应本地格式 reference；柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线，除非用户明确要求或图表类型必须依赖网格线，否则不得显示 major/minor gridlines。


## 工作流

### 1. 明确需求
- **询问用户**：单页还是多页（3-4 页）？
- **询问用户**：是否有特定重点领域或需要强调的话题？
- **只有在用户确认后**，再开始研究

### 2. 研究与规划
**数据来源：**
- **主要来源**：公司披露文件（BamSEC、SEC EDGAR - "Item 1. Business"、MD&A）、投资者演示、公司官网；A股/港股优先使用交易所公告、定期报告、招股书和公司公告
- **市场数据**：Bloomberg、FactSet、CapIQ（股价、股本、市值、净债务、EV、股权结构）；A股/港股可使用已授权 MCP 或官方/交易所数据
- **预测**：FactSet/CapIQ consensus 的 NTM 收入、EBITDA、EPS；境内市场需标明一致预期来源
- **新闻**：过去 90 天新闻稿、M&A 活动、指引变化

**必需指标：**
- **财务指标**：前后约 3 年的收入、EBITDA、利润率（%）、EPS、FCF
- **估值指标**：市值、EV、EV/收入、EV/EBITDA、P/E multiples
- **增长指标**：同比增速（%）
- **股权结构**：前五大股东及持股比例
- **分部信息**：产品组合和/或地域组合（百分比拆分）

**归一化：**
- 将所有金额统一到一致币种，并显式标注币种
- 单位保持一致（例如全篇使用百万元或十亿元，不要混用；A股材料默认万元/亿元）

**制作前：**
- 在聊天中输出大纲，每个项目 4-5 个要点（使用真实数字，不使用占位符）
- 输出样式选择：字体、颜色（hex codes）、每组数据的图表类型
- 获得用户确认：“这个大纲和视觉策略是否符合你的预期？”

### 3. 逐页创建
**关键：必须一次只创建一页，并在进入下一页前获得用户批准。**

**每一页都必须：**
1. 只用 PptxGenJS 创建当前这一页
2. **强制：转换为图片供审阅** - 必须把幻灯片转换为图片，以便进行视觉校验：
   ```bash
   soffice --headless --convert-to pdf presentation.pptx
   pdftoppm -jpeg -r 150 -f 1 -l 1 presentation.pdf slide
   ```
3. **强制视觉审阅**：进入下一步前必须仔细查看渲染后的幻灯片图片：
   - **文本重叠检查**：逐一扫描所有文本元素，标签、要点或标题是否互相碰撞？
   - **文本截断检查**：是否有文本在边界处被截断？所有文字是否完整可见？
   - **图表边界检查**：图表是否在容器内？所有轴标签是否完整可见？
   - **象限完整性**：某一象限的内容是否溢出到相邻象限？
4. **如果发现任何重叠或截断**：按顺序立即修复：
   - **第一步**：减小字号（降低 1-2pt）
   - **第二步**：缩短文本（用缩写、删除较不重要信息）
   - **第三步**：调整元素位置或容器尺寸
   - **重新渲染并再次校验**，直到所有文本都干净放入后才能继续
5. 向用户展示幻灯片图片和下载链接
6. **停止并等待用户明确批准**，然后才能创建下一页。用户确认前不得继续。

**每页都必须检查以下具体问题：**
- 表格行是否与下方文本碰撞
- 图表 x 轴标签是否在底部被截断
- 过长要点是否换行挤入相邻内容
- 象限内容是否溢出到相邻象限
- 标题文本是否与下方内容重叠
- 图例文本是否与图表元素重叠
- 页脚/来源文本是否与主体内容碰撞

---

## 幻灯片格式要求

### 信息密度至关重要

**首要目标是最大化信息密度。** 忙碌的高管应能在 30 秒内理解完整公司故事。每个象限都要尽可能装满有效信息。

**每个象限目标：**
- **公司概览**：至少 6-8 个要点（总部、成立时间、员工数、CEO/CFO、市值、ticker、行业、关键数据）
- **业务与定位**：6-8 个要点（收入驱动因素、产品、市场份额、竞争壁垒、客户数量、地域组合）
- **关键财务**：8-10 行表格，或图表 + 4-5 个关键指标（收入、EBITDA、利润率、EPS、FCF、增速、估值 multiples）
- **第四象限**：5-7 个要点（持股比例、近期 M&A、业务进展、催化剂）

**信息压缩技巧：**
- 合并相关事实：“总部：Austin, TX；成立：2003；员工 14 万人”
- 始终包含数字：“收入 500 亿美元”，不要写“收入规模较大”
- 添加上下文：“EBITDA 利润率：25%（行业均值 18%）”
- 包含同比变化：“收入：1.25 亿美元（同比 +28%）”
- 使用百分比：“企业业务：占收入 62%”

**如果某个象限显得稀疏，补充更多信息：**
- 带百分比的分部拆分
- 地域收入拆分
- 客户集中度（前十大 = X%）
- 近期合同赢单及金额
- 指引 vs. 一致预期
- 内部人持股比例

**行距 - 每个章节使用单个文本框：**
```python
def add_section(slide, x, y, w, header_text, bullets, header_size=10, bullet_size=8):
    """标题 + 要点放在同一个文本框中，使用自然段落间距"""
    tb = slide.shapes.add_textbox(x, y, w, Inches(len(bullets) * 0.18 + 0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    # 标题段落
    p = tf.paragraphs[0]
    p.text = header_text
    p.font.bold = True
    p.font.size = Pt(header_size)
    p.font.color.rgb = RGBColor(0, 51, 102)
    p.space_after = Pt(6)  # 标题后的小间距

    # 要点段落
    for bullet in bullets:
        p = tf.add_paragraph()
        p.text = bullet
        p.font.size = Pt(bullet_size)
        p.space_after = Pt(3)
    return tb
```

**关键间距原则：**
- 标题 + 要点放在同一个文本框（不要单独创建标题文本框）
- 标题后使用 `space_after = Pt(6)`，要点之间使用 `Pt(3)`
- 不要硬编码空隙，让段落间距自然处理
- 如果内容溢出，先把字号降低 1pt，而不是删除内容

---

- **3-4 页高密度幻灯片**：使用象限、分栏、表格和图表
- **所有正文都用要点**：绝不写成段落。**每个章节使用一个文本框并放入所有要点**，不要为每个要点单独创建文本框。使用 PptxGenJS bullet 格式：
  ```javascript
  // 正确：单个文本框包含要点列表，每个数组项变成一个要点
  // 位置在左上象限（公司概览），放在带强调色条的标题之后
  slide.addText(
    [
      { text: '总部：Austin, Texas；成立于 2003 年', options: { bullet: { indent: 10 }, breakLine: true } },
      { text: '员工：全球 6 大洲 140,000+ 人', options: { bullet: { indent: 10 }, breakLine: true } },
      { text: 'CEO：Elon Musk；CFO：Vaibhav Taneja', options: { bullet: { indent: 10 }, breakLine: true } },
      { text: '市值：8,500 亿美元（全球市值第 6）', options: { bullet: { indent: 10 }, breakLine: true } },
      { text: '分部：汽车（85%）、能源（10%）、服务（5%）', options: { bullet: { indent: 10 } } }
    ],
    { x: 0.45, y: 0.95, w: 4.5, h: 2.6, fontSize: 11, fontFace: 'Microsoft YaHei', valign: 'top', paraSpaceAfter: 6 }
  );

  // 错误：为每个要点创建多个独立文本框，会造成对齐问题
  // slide.addText('Headquarters: Austin', { x: 0.5, y: 1.0, bullet: true });
  ```

  **要点格式提示：**
  - `bullet: { indent: 10 }`：控制要点缩进（越小越紧凑）
  - `paraSpaceAfter: 6`：每个段落后的间距，单位为 point
  - 将多个相关事实压缩进同一个要点（例如“总部：Austin；成立：2003”）
  - 包含具体数字和百分比，以提高信息密度
- **标题使用 Title Case**（不要 ALL CAPS），左对齐
- **字体保持一致**，表格也要一致；中文材料优先使用中文字体栈
- **公司品牌色**：创建幻灯片前必须研究公司真实品牌色。不要猜测或假设颜色。
- **如用户提供品牌指南，必须遵循**

### 视觉参考
参考 `examples/Nike_Strip_Profile_Example.pptx` 获取布局灵感。颜色需适配每家公司的品牌。

---

## 首页布局

必须通过面向忙碌高管的“30 秒理解测试”。

### 幻灯片设置（关键）
**使用 4:3 宽高比**（标准投行 pitch book 格式）：
```javascript
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_4x3';  // 10" wide × 7.5" tall - MUST USE THIS
```

### 幻灯片坐标系
PptxGenJS 使用英寸。4:3 幻灯片 = **10" 宽 × 7.5" 高**。
- **x**：距左边缘的水平位置（0 = 最左，10 = 最右）
- **y**：距上边缘的垂直位置（0 = 顶部，7.5 = 底部）
- **内容必须保持在边界内**，四边至少留 0.3" 边距

### 首页定位（英寸）
```
┌─────────────────────────────────────────────────────────────────┐
│ y=0.2  标题：Company Name (Ticker)                              │
├────────────────────────────┬────────────────────────────────────┤
│ y=0.6  公司概览            │ y=0.6  业务与定位                 │
│ x=0.3, w=4.7               │ x=5.0, w=4.7                       │
│ h=3.0                      │ h=3.0                              │
├────────────────────────────┼────────────────────────────────────┤
│ y=3.7  关键财务            │ y=3.7  股价/近期进展               │
│ x=0.3, w=4.7               │ x=5.0, w=4.7                       │
│ h=3.5                      │ h=3.5                              │
└────────────────────────────┴────────────────────────────────────┘
                                                            y=7.5
```

### 标题部分（y=0.2）
**Company Name (Ticker)**，例如：`Tesla, Inc. (TSLA)`
```javascript
slide.addText('Tesla, Inc. (TSLA)', { x: 0.3, y: 0.2, w: 9.4, h: 0.35, fontSize: 18, bold: true });
```

### 四象限布局（y=0.6 至 y=7.2）

| 象限 | 位置 | 内容 |
|----------|----------|---------|
| **1** | x=0.3, y=0.6, w=4.7, h=3.0 | **公司概览**：总部、成立时间、关键数据、业务摘要（4-5 个要点） |
| **2** | x=5.0, y=0.6, w=4.7, h=3.0 | **业务与定位**：收入驱动因素、产品/服务、竞争地位、增长驱动因素（4-5 个要点） |
| **3** | x=0.3, y=3.7, w=4.7, h=3.5 | **关键财务**：收入、EBITDA、利润率、EPS、FCF + 估值（市值、EV、multiples）— **表格或图表二选一，不要同时放** |
| **4** | x=5.0, y=3.7, w=4.7, h=3.5 | **上市公司**：1 年股价图 + 前几大股东。**非上市公司**：近期进展或股权/M&A 历史 |

### 字号 - 使用这些精确值
| 元素 | 字号 | 说明 |
|---------|------|-------|
| 幻灯片标题 | 24pt | 加粗，公司品牌色 |
| 象限标题 | 14pt | 加粗，带强调色条 |
| 正文/bullet 文本 | 11pt | 常规字重 |
| 表格文本 | 10pt | 高密度表格可用 9pt |
| 图表标签 | 9pt | 标签保持简短 |
| 来源/页脚 | 8pt | 位于幻灯片底部 |

**关键：如果文本溢出，将字号降低 1pt 并重新渲染。**

### 视觉强调（必需）
每个象限标题左侧都必须有彩色强调条：
```javascript
// 为象限标题添加强调色条
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0.3, y: 0.6, w: 0.08, h: 0.25,
  fill: { color: 'E31937' }  // 使用公司品牌色
});
slide.addText('公司概览', {
  x: 0.45, y: 0.6, w: 4.5, h: 0.3, fontSize: 14, bold: true, fontFace: 'Microsoft YaHei'
});
```

**需要包含的视觉元素：**
- 所有章节标题旁都有强调色条（品牌色）
- 上下象限之间使用细水平分割线
- 如可获得，公司 logo 放在右上角
- 表格使用浅灰色细网格线（#CCCCCC）

### 首页格式
- **字体**：中文材料优先使用 `Microsoft YaHei` / `PingFang SC` / `Noto Sans CJK SC` 等中文字体栈；若用户或品牌指南另有指定，以其为准
- **象限标题**：中文标题自然表达，英文公司名保留原文；不要使用 ALL CAPS
- **Bullets**：开头关键词加粗，例如“**市场地位：** 全球领先制造商……”
- 只使用白色背景，不使用方框、填充或阴影
- Section headers：加粗文本，样式遵循品牌指南
- 所有象限尺寸一致并对齐

---

## 后续页面：自由布局

- 双栏布局（40/60 或 50/50）、整页图表或侧边栏布局
- 每页展开首页内容
- 保持一致的排版和配色方案
- 建议顺序：产品/市场 → 财务分析 → 管理层

---

## 图表（多页 profile）

**多页 profile**：包含 2-3 个真实 PptxGenJS 图表。绝不使用占位 div 或静态图片。

**单页 profile**：财务信息使用表格（更节省空间）。只有当图表替代表格时才添加图表，不要同时添加。

| 数据类型 | 图表类型 |
|-----------|------------|
| 收入趋势 | 折线图或柱状图（多年） |
| 地域拆分 | 横向条形图 |
| 产品组合 | 带百分比的饼图 |
| 财务对比 | 柱状图 |
| 股价（1 年日频） | 折线图 |

### 图表代码示例

**横向条形图（适合 4:3 幻灯片右下象限）：**
```javascript
slide.addChart(pptx.charts.BAR, [{
  name: 'FY2024 按地区收入',
  labels: ['北美', 'EMEA', '中国', 'APLA'],
  values: [21.4, 13.6, 7.6, 6.7]
}], {
  x: 5.0, y: 4.1, w: 4.5, h: 3.0,  // 适合右下象限（4:3）
  barDir: 'bar', chartColors: ['FF6B35'], showValue: true,
  dataLabelFontSize: 10, catAxisLabelFontSize: 10, valAxisLabelFontSize: 10,
  dataLabelFormatCode: '$#,##0.0B',
  title: '按地域收入', titleFontSize: 12, titleBold: true
});
```

**饼图（适合 4:3 幻灯片右下象限）：**
```javascript
slide.addChart(pptx.charts.PIE, [{
  name: '产品组合',
  labels: ['鞋履', '服装', '装备'],
  values: [68, 29, 3]
}], {
  x: 5.0, y: 4.1, w: 4.5, h: 3.0,  // 适合右下象限（4:3）
  showPercent: true, showLegend: true, legendPos: 'r',
  dataLabelFontSize: 10, legendFontSize: 10,
  chartColors: ['FF6B35', '2C2C2C', '4A4A4A'],
  title: 'FY24 收入结构', titleFontSize: 12, titleBold: true
});
```

**折线图（适合后续页面整页宽度）：**
```javascript
slide.addChart(pptx.charts.LINE, [{
  name: '收入（十亿美元）',
  labels: ['FY21', 'FY22', 'FY23', 'FY24', 'FY25E'],
  values: [44.5, 46.7, 48.5, 51.4, 54.2]
}], {
  x: 0.3, y: 1.2, w: 9.4, h: 5.5,  // 4:3 幻灯片整页宽度
  chartColors: ['FF6B35'], showValue: true, lineSmooth: true,
  dataLabelFontSize: 11, catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  title: '收入趋势与预测', titleFontSize: 14, titleBold: true
});
```

---

## 财务数据格式

**始终使用原生 PptxGenJS 表格或图表，绝不要使用纯文本段落或 HTML 表格。**

财务数据使用 `slide.addTable()`（适合 4:3 幻灯片左下象限）：
```javascript
// 先添加带强调色条的标题
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0.3, y: 3.7, w: 0.08, h: 0.25, fill: { color: 'E31937' }
});
slide.addText('关键财务与估值', {
  x: 0.45, y: 3.7, w: 4.5, h: 0.3, fontSize: 14, bold: true, fontFace: 'Microsoft YaHei'
});

// 财务数据表
slide.addTable([
  [{ text: '指标', options: { bold: true, fill: '003366', color: 'FFFFFF' } },
   { text: 'FY24', options: { bold: true, fill: '003366', color: 'FFFFFF' } },
   { text: 'FY25E', options: { bold: true, fill: '003366', color: 'FFFFFF' } }],
  ['收入', '$51.4B', '$54.2B'],
  ['同比增长', '+6.0%', '+5.5%'],
  ['EBITDA', '$8.9B', '$9.5B'],
  ['EBITDA 利润率', '17.3%', '17.5%'],
  ['EPS', '$3.42', '$3.75'],
  ['市值', '$185B', '—'],
  ['EV/EBITDA', '12.5x', '11.7x']
], {
  x: 0.45, y: 4.1, w: 4.3, h: 3.0,  // 左下象限标题下方
  fontFace: 'Microsoft YaHei', fontSize: 10,
  border: { pt: 0.5, color: 'CCCCCC' },
  valign: 'middle',
  colW: [1.8, 1.25, 1.25]  // 列宽
});
```

❌ **错误：** 使用 `注释：2024 财年收入增长 +1.0%，净利润 51 亿美元……` 这类纯文本  
❌ **错误：** 使用无法正确转换到 PowerPoint 的 HTML 表格

预测数据使用结构化表格呈现熊市/基准/牛市三种情景。

---

## 质量检查清单

### 首页
- [ ] 标题区包含公司名称、ticker、行业
- [ ] 标题下方正好 4 个等大象限
- [ ] 全部使用要点，不使用段落，每条最多 1 行
- [ ] 财务信息用表格或图表呈现（二选一，不要两者同时出现）

### 所有幻灯片
- [ ] 没有文本溢出或截断
- [ ] 全篇字体和颜色一致
- [ ] 图表正确渲染
- [ ] 没有占位文本，全部使用真实数据
- [ ] 单位口径一致（例如百万元或十亿元，不混用；A股材料默认万元/亿元）
- [ ] 已标注来源
- [ ] 达到投行质量（GS/MS/JPM 标准）

**注意：** 创建 PowerPoint 文件时参考 **PPTX skill**。
