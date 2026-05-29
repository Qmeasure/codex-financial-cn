> Reference 链路：执行本文件前，先读取本 skill 的 `references/data-query-order.md`、`references/cn-markdown-formatting.md`、`references/cn-html-formatting.md`；本文件只描述业务 workflow 或参考口径，不承载新增中文格式正文。

# HTML 报告模板参考

使用此模板作为单家公司业绩预览 HTML 报告的基础。请根据第 1-5 阶段收集的研究资料，定制数据、图表和叙述内容。

## HTML 结构

报告是一个独立的 HTML 文件，包含：
- 内嵌 CSS（不依赖外部样式表）
- 通过 CDN 加载 Chart.js，用于交互式图表
- 通过 `@media print` 提供适合打印的样式
- 同时适配屏幕浏览和打印输出的响应式布局
- 目标长度：打印后 4-5 页

## 完整模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>业绩预览 — [COMPANY] ([TICKER]) — [DATE]</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js" integrity="sha384-vsrfeLOOY6KuIYKDlmVH5UiBmgIdB1oEf7p01YgWHuqmOHfZr374+odEv96n9tNC" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.1.0/dist/chartjs-plugin-annotation.min.js" integrity="sha384-3N9GHhCtN3CQef6tNfqgZlv7sQLYIkcChN+uaTZ7xVdzKYp/SjBNPxa92+hM7EAY" crossorigin="anonymous"></script>
  <style>
    /* ── 重置与基础样式 ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { font-size: 15px; }
    body {
      font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', Arial, sans-serif;
      color: #1a1a2e;
      background: #fff;
      line-height: 1.6;
    }

    /* ── 版式 ── */
    .page {
      max-width: 1100px;
      margin: 0 auto;
      padding: 40px 48px;
    }
    .page-break {
      page-break-before: always;
      border-top: 2px solid #1a1a4e;
      margin-top: 48px;
      padding-top: 32px;
    }

    /* ── 页眉 / 封面 ── */
    .cover-header {
      border-bottom: 3px solid #1a1a4e;
      padding-bottom: 16px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .cover-header .brand {
      font-size: 24px;
      font-weight: bold;
      color: #1a1a4e;
      letter-spacing: 2px;
      text-transform: uppercase;
    }
    .cover-header .sector {
      font-size: 13px;
      color: #555;
    }
    .cover-header .date {
      font-size: 14px;
      color: #333;
      text-align: right;
    }
    .report-title {
      font-size: 26px;
      font-weight: bold;
      color: #1a1a2e;
      margin: 20px 0 16px 0;
      line-height: 1.3;
    }

    /* ── 核心观点 ── */
    .executive-summary {
      font-size: 14px;
      line-height: 1.65;
      color: #222;
      margin-bottom: 16px;
    }
    .executive-summary p {
      margin-bottom: 10px;
      text-align: justify;
    }
    .executive-summary ul {
      margin: 8px 0 10px 20px;
      font-size: 13.5px;
    }
    .executive-summary ul li {
      margin-bottom: 5px;
      line-height: 1.5;
    }
    blockquote {
      border-left: 3px solid #b0b8c8;
      padding: 6px 14px;
      margin: 8px 0 8px 12px;
      font-style: italic;
      color: #444;
      background: #f9fafb;
      font-size: 12.5px;
      line-height: 1.5;
    }

    /* ── 章节标题 ── */
    h2.section-title {
      font-size: 18px;
      font-weight: 700;
      color: #1a1a4e;
      border-bottom: 2px solid #1a1a4e;
      padding-bottom: 5px;
      margin: 28px 0 14px 0;
    }
    h3.subsection-title {
      font-size: 14px;
      font-weight: 600;
      color: #1a1a4e;
      margin: 16px 0 8px 0;
    }
    h4.figure-title {
      font-size: 12px;
      font-weight: 600;
      color: #444;
      margin: 14px 0 6px 0;
    }

    /* ── 表格 ── */
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin: 10px 0 16px 0;
    }
    thead th {
      background: #1a1a4e;
      color: #fff;
      padding: 7px 10px;
      text-align: left;
      font-weight: 600;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    tbody td {
      padding: 6px 10px;
      border-bottom: 1px solid #e0e0e0;
    }
    tbody tr:nth-child(even) {
      background: #f9fafb;
    }
    tbody tr:hover {
      background: #eef0f5;
    }
    .num { text-align: right; font-variant-numeric: tabular-nums; }
    .pos { color: #0d7a3e; font-weight: 600; }
    .neg { color: #c0392b; font-weight: 600; }
    .neutral { color: #555; }
    .highlight-row { background: #e8eaf6 !important; font-weight: 600; }

    /* ── 图表容器 ── */
    .chart-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin: 12px 0 20px 0;
    }
    .chart-container {
      position: relative;
      background: #fafbfc;
      border: 1px solid #e8e8e8;
      border-radius: 4px;
      padding: 14px;
    }
    .chart-container canvas {
      max-height: 260px;
    }
    .chart-full {
      grid-column: 1 / -1;
    }

    /* ── 紧凑列表 ── */
    .key-metrics ul, .themes ul, .news-list ul {
      margin: 6px 0 6px 18px;
      font-size: 13px;
      line-height: 1.55;
    }
    .key-metrics li, .themes li, .news-list li {
      margin-bottom: 5px;
    }

    /* ── 数据引用链接 ── */
    a.data-ref {
      color: #1a1a4e;
      text-decoration: none;
      border-bottom: 1px dotted transparent;
      transition: border-color 0.15s;
    }
    a.data-ref:hover {
      border-bottom-color: #1a1a4e;
    }

    /* ── 附录 ── */
    .appendix table {
      font-size: 10.5px;
    }
    .appendix thead th {
      font-size: 10px;
      padding: 5px 8px;
    }
    .appendix tbody td {
      padding: 4px 8px;
      font-size: 10.5px;
      vertical-align: top;
      line-height: 1.45;
    }
    .appendix .ref-id {
      font-weight: 600;
      color: #1a1a4e;
      white-space: nowrap;
    }
    .appendix .source-detail {
      font-size: 10px;
      color: #444;
    }
    .appendix .source-detail .formula {
      font-family: 'Courier New', monospace;
      font-size: 9.5px;
      color: #555;
    }
    .appendix .source-detail .excerpt {
      font-style: italic;
      color: #555;
    }
    .appendix .source-detail .src-label {
      font-weight: 600;
      color: #1a1a4e;
      font-size: 9.5px;
    }
    .appendix .source-detail a.data-ref {
      font-weight: 600;
    }
    .appendix a.src-url {
      color: #3366cc;
      text-decoration: underline;
      font-size: 10px;
      word-break: break-all;
    }
    .appendix a.src-url:hover {
      color: #1a1a4e;
    }
    .appendix .transcript-ref {
      font-weight: 600;
      color: #1a1a4e;
      font-size: 10px;
    }
    .appendix-group {
      font-size: 11px;
      font-weight: 700;
      color: #1a1a4e;
      background: #f0f1f5;
      padding: 4px 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* ── 来源 / 页脚 ── */
    .source {
      font-size: 10px;
      color: #999;
      margin-top: 3px;
      font-style: italic;
    }
    .ai-disclaimer {
      background-color: #fff3cd;
      border: 1px solid #ffc107;
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      color: #664d03;
      text-align: center;
      margin-bottom: 12px;
    }
    .page-footer {
      border-top: 2px solid #1a1a4e;
      padding-top: 10px;
      margin-top: 32px;
      text-align: center;
    }
    .page-footer .footer-disclaimer {
      font-size: 11px;
      font-weight: 600;
      color: #664d03;
      background-color: #fff3cd;
      border: 1px solid #ffc107;
      border-radius: 4px;
      padding: 4px 10px;
      display: inline-block;
      margin-bottom: 4px;
    }
    .page-footer .footer-meta {
      font-size: 10px;
      color: #888;
    }

    /* ── 打印样式 ── */
    @media print {
      body { font-size: 11px; }
      .page { padding: 16px; max-width: none; }
      .chart-container { break-inside: avoid; }
      table { break-inside: avoid; }
      .page-break { margin-top: 0; }
      .no-print { display: none; }
    }
  </style>
</head>
<body>
<div class="page">

  <!-- ════════════════════════════════════════════ -->
  <!-- 第 1 页：封面与核心观点                       -->
  <!-- ════════════════════════════════════════════ -->
  <div class="ai-disclaimer">分析由 AI 生成，请核验所有输出</div>
  <div class="cover-header">
    <div>
      <div class="brand">业绩预览</div>
      <div class="sector">[行业] | [TICKER]</div>
    </div>
    <div class="date">[完整日期]</div>
  </div>

  <h1 class="report-title">[公司名称] ([TICKER]) [Q# FY####] 业绩预览：[主题副标题]</h1>

  <div class="executive-summary">
    <!-- 核心观点：2-3 个短段落 + 要点列表。
         写清我们的预期、EPS 预测与一致预期对比、指引预期、
         需要关注的关键指标、可能驱动股价的因素和主要分歧。
         在支撑论点的位置嵌入 3-4 条管理层引述，使用 blockquote。
         不要另建“关键管理层引述”章节。 -->

    <p>[开头 1-2 句：说明我们对此次业绩发布的核心预期。]</p>

    <ul>
      <li><strong>EPS：</strong>我们预计 <a href="#ref-1" class="data-ref">$X.XX</a>，一致预期为 <a href="#ref-2" class="data-ref">$X.XX</a>，[理由]</li>
      <li><strong>收入：</strong>我们预计 <a href="#ref-3" class="data-ref">$XX.XB</a>，一致预期为 <a href="#ref-4" class="data-ref">$XX.XB</a>，[理由]</li>
      <li><strong>指引：</strong>[对前瞻指引的预期]</li>
      <li><strong>关键指标：</strong>[最需要关注的非标题指标]</li>
      <li><strong>股价催化：</strong>[业绩发布后可能推动股价上行/下行的因素]</li>
      <li><strong>核心分歧：</strong>[多空双方的主要争议点]</li>
    </ul>

    <blockquote>“[支撑某一论点的关键管理层引述]” — [发言人]，[Q# FY####] 业绩会</blockquote>

    <p>[用 1-2 句话串联观点，给出对此次业绩前交易背景的整体判断。]</p>

    <blockquote>“[另一条支撑性引述]” — [发言人]，[Q# FY####] 业绩会</blockquote>
  </div>

  <!-- ════════════════════════════════════════════ -->
  <!-- 第 2 页：一致预期、关注主题与近期新闻         -->
  <!-- ════════════════════════════════════════════ -->
  <div class="page-break">

    <!-- 一致预期表（图表标签内嵌） -->
    <h2 class="section-title">一致预期 — [Q# FY####]</h2>
    <h4 class="figure-title">[Q# FY####] 一致预期</h4>
    <table>
      <thead>
        <tr>
          <th>指标</th>
          <th class="num">一致预期</th>
          <th class="num">我们的预测</th>
          <th class="num">同比变化</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>收入</td><td class="num"><a href="#ref-N" class="data-ref">$[XX.X]B</a></td><td class="num"><a href="#ref-N" class="data-ref">$[XX.X]B</a></td><td class="num [pos|neg]"><a href="#ref-N" class="data-ref">[+/-X.X%]</a></td></tr>
        <tr><td>摊薄 EPS</td><td class="num"><a href="#ref-N" class="data-ref">$[X.XX]</a></td><td class="num"><a href="#ref-N" class="data-ref">$[X.XX]</a></td><td class="num [pos|neg]"><a href="#ref-N" class="data-ref">[+/-X.X%]</a></td></tr>
        <tr><td>毛利率</td><td class="num"><a href="#ref-N" class="data-ref">[XX.X%]</a></td><td class="num"><a href="#ref-N" class="data-ref">[XX.X%]</a></td><td class="num [pos|neg]"><a href="#ref-N" class="data-ref">[+/-XXbps]</a></td></tr>
        <tr><td>营业利润</td><td class="num"><a href="#ref-N" class="data-ref">$[X.X]B</a></td><td class="num"><a href="#ref-N" class="data-ref">$[X.X]B</a></td><td class="num [pos|neg]"><a href="#ref-N" class="data-ref">[+/-X.X%]</a></td></tr>
        <!-- 在下方增加 2-3 个公司特定 KPI（例如同店销售、电商增长、会员收入） -->
        <tr><td>[公司 KPI 1]</td><td class="num">[数值]</td><td class="num">[数值]</td><td class="num [pos|neg]">[变化]</td></tr>
        <tr><td>[公司 KPI 2]</td><td class="num">[数值]</td><td class="num">[数值]</td><td class="num [pos|neg]">[变化]</td></tr>
      </tbody>
    </table>
    <div class="source">来源：Kensho、S&P Capital IQ</div>

    <!-- EPS 之外的关键指标 -->
    <h3 class="subsection-title">EPS 之外的关键指标</h3>
    <div class="key-metrics">
      <ul>
        <li><strong>[指标 1]：</strong>[一致预期/管理层预期是什么，为什么重要。请给出具体数字。]</li>
        <li><strong>[指标 2]：</strong>[详情]</li>
        <li><strong>[指标 3]：</strong>[详情]</li>
        <!-- 3-5 项 -->
      </ul>
    </div>

    <!-- 需要关注的主题 -->
    <h3 class="subsection-title">需要关注的主题</h3>
    <div class="themes">
      <ul>
        <li><strong>[主题 1]：</strong>[最多 1-2 句。保持前瞻、具体。]</li>
        <li><strong>[主题 2]：</strong>[详情]</li>
        <li><strong>[主题 3]：</strong>[详情]</li>
        <!-- 3-5 个主题 -->
      </ul>
    </div>

    <!-- 近期新闻与进展 -->
    <h3 class="subsection-title">近期新闻与进展</h3>
    <div class="news-list">
      <ul>
        <li><strong>[日期]：</strong>[标题] — [一句话影响评估]</li>
        <li><strong>[日期]：</strong>[标题] — [影响]</li>
        <li><strong>[日期]：</strong>[标题] — [影响]</li>
        <!-- 过去 60 天内的 3-5 条重要事项 -->
      </ul>
    </div>
    <div class="source">来源：Kensho</div>

  </div>

  <!-- ════════════════════════════════════════════ -->
  <!-- 第 3-5 页：图表                               -->
  <!-- 所有图表和表格按顺序编号                     -->
  <!-- ════════════════════════════════════════════ -->
  <div class="page-break">
    <h2 class="section-title">财务与竞争分析</h2>

    <!-- 图 1：季度收入与摊薄 EPS -->
    <div class="chart-row">
      <div class="chart-container">
        <h4 class="figure-title">图 1：季度收入与摊薄 EPS</h4>
        <canvas id="chart-rev-eps"></canvas>
        <div class="source">来源：S&P Capital IQ</div>
      </div>

      <!-- 图 2：利润率趋势 -->
      <div class="chart-container">
        <h4 class="figure-title">图 2：利润率趋势（毛利率与营业利润率）</h4>
        <canvas id="chart-margins"></canvas>
        <div class="source">来源：S&P Capital IQ</div>
      </div>
    </div>

    <!-- 图 3：收入同比增速 -->
    <div class="chart-row">
      <div class="chart-container chart-full">
        <h4 class="figure-title">图 3：收入同比增速（%）</h4>
        <canvas id="chart-rev-growth" style="max-height: 200px;"></canvas>
        <div class="source">来源：S&P Capital IQ</div>
      </div>
    </div>

    <!-- 图 4：业务分部收入 -->
    <h4 class="figure-title">图 4：业务分部收入</h4>
    <table>
      <thead>
        <tr>
          <th>分部</th>
          <th class="num">最近季度收入（百万美元）</th>
          <th class="num">占总收入比例</th>
          <th class="num">同比变化</th>
        </tr>
      </thead>
      <tbody>
        <!-- 使用分部数据填充。同比变化单元格用 pos/neg class 做颜色标记。 -->
      </tbody>
    </table>
    <div class="source">来源：S&P Capital IQ</div>
  </div>

  <!-- 股票与可比公司图表分页 -->
  <div class="page-break">

    <!-- 图 5：过去 1 年股价及业绩发布日期 -->
    <div class="chart-row">
      <div class="chart-container chart-full">
        <h4 class="figure-title">图 5：过去 1 年股价及业绩发布日期</h4>
        <canvas id="chart-price-annotated" style="max-height: 300px;"></canvas>
        <div class="source">来源：S&P Capital IQ</div>
      </div>
    </div>

    <!-- 图 6：股价表现与可比公司对比（指数化至 100） -->
    <div class="chart-row">
      <div class="chart-container chart-full">
        <h4 class="figure-title">图 6：股价表现与可比公司对比 — 1 年（指数化至 100）</h4>
        <canvas id="chart-comp-perf" style="max-height: 300px;"></canvas>
        <div class="source">来源：S&P Capital IQ</div>
      </div>
    </div>
  </div>

  <div class="page-break">

    <!-- 图 7：LTM P/E 与可比公司对比 -->
    <div class="chart-row">
      <div class="chart-container chart-full">
        <h4 class="figure-title">图 7：LTM P/E 与可比公司对比</h4>
        <canvas id="chart-pe-comp" style="max-height: 280px;"></canvas>
        <div class="source">来源：S&P Capital IQ</div>
      </div>
    </div>

    <!-- 图 8：可比公司对比表 -->
    <h4 class="figure-title">图 8：可比公司对比</h4>
    <table>
      <thead>
        <tr>
          <th>Ticker</th>
          <th>公司</th>
          <th class="num">市值（十亿美元）</th>
          <th class="num">LTM P/E</th>
          <th class="num">NTM P/E</th>
          <th class="num">YTD %</th>
          <th class="num">1-Yr %</th>
        </tr>
      </thead>
      <tbody>
        <!-- 使用 class="highlight-row" 高亮标的公司所在行 -->
      </tbody>
    </table>
    <div class="source">来源：S&P Capital IQ</div>
  </div>

  <!-- ════════════════════════════════════════════ -->
  <!-- 附录：数据来源与计算                          -->
  <!-- ════════════════════════════════════════════ -->
  <div class="page-break appendix" id="appendix">
    <div class="ai-disclaimer">分析由 AI 生成，请核验所有输出</div>
    <h2 class="section-title">附录：数据来源与计算</h2>
    <p style="font-size: 11px; color: #666; margin-bottom: 12px;">
      本报告中的每一项判断都超链接至下方对应条目。点击正文中的高亮文本即可跳转到此处。
    </p>
    <table>
      <thead>
        <tr>
          <th style="width: 40px;">编号</th>
          <th style="width: 170px;">事实</th>
          <th style="width: 75px;">数值</th>
          <th>来源与推导</th>
        </tr>
      </thead>
      <tbody>
        <!-- 分组：季度财务数据 -->
        <tr><td colspan="4" class="appendix-group">季度财务数据</td></tr>
        <tr id="ref-1">
          <td class="ref-id">1</td>
          <td>[Q# FY#### 收入]</td>
          <td class="num">$[XX.X]B</td>
          <td class="source-detail">
            <span class="src-label">S&P Capital IQ</span> — get_financial_line_item_from_identifiers(identifier='[TICKER]', line_item='revenue', period_type='quarterly', period='[Q# FY####]')
          </td>
        </tr>
        <tr id="ref-2">
          <td class="ref-id">2</td>
          <td>[Q# FY#### 摊薄 EPS]</td>
          <td class="num">$[X.XX]</td>
          <td class="source-detail">
            <span class="src-label">S&P Capital IQ</span> — get_financial_line_item_from_identifiers(identifier='[TICKER]', line_item='diluted_eps', period_type='quarterly', period='[Q# FY####]')
          </td>
        </tr>
        <tr id="ref-3">
          <td class="ref-id">3</td>
          <td>[Q# FY#### 毛利]</td>
          <td class="num">$[XX.X]B</td>
          <td class="source-detail">
            <span class="src-label">S&P Capital IQ</span> — get_financial_line_item_from_identifiers(identifier='[TICKER]', line_item='gross_profit', period_type='quarterly', period='[Q# FY####]')
          </td>
        </tr>
        <tr id="ref-4">
          <td class="ref-id">4</td>
          <td>[Q# FY#### 毛利率]</td>
          <td class="num">[XX.X%]</td>
          <td class="source-detail">
            <span class="formula"><a href="#ref-3" class="data-ref">毛利 $XX.XB</a> / <a href="#ref-1" class="data-ref">收入 $XX.XB</a> = XX.X%</span><br>
            <span class="src-label">S&P Capital IQ</span>（计算值）
          </td>
        </tr>
        <tr id="ref-5">
          <td class="ref-id">5</td>
          <td>[Q# FY#### 收入同比增速]</td>
          <td class="num">[+/-X.X%]</td>
          <td class="source-detail">
            <span class="formula">(<a href="#ref-1" class="data-ref">[Q# FY## 收入 $XX.XB]</a> - <a href="#ref-N" class="data-ref">[Q# FY## 收入 $XX.XB]</a>) / <a href="#ref-N" class="data-ref">[Q# FY## 收入 $XX.XB]</a> = X.X%</span><br>
            <span class="src-label">S&P Capital IQ</span>（计算值）
          </td>
        </tr>
        <!-- 继续列出所有财务数据点…… -->

        <!-- 分组：估值 -->
        <tr><td colspan="4" class="appendix-group">估值</td></tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>当前股价 — [TICKER]</td>
          <td class="num">$[XXX.XX]</td>
          <td class="source-detail">
            <span class="src-label">S&P Capital IQ</span> — get_prices_from_identifiers(identifier='[TICKER]', periodicity='day')
          </td>
        </tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>市值 — [TICKER]</td>
          <td class="num">$[XXX.X]B</td>
          <td class="source-detail">
            <span class="src-label">S&P Capital IQ</span> — get_capitalization_from_identifiers(identifier='[TICKER]', capitalization='market_cap')
          </td>
        </tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>LTM P/E — [TICKER]</td>
          <td class="num">[XX.X]x</td>
          <td class="source-detail">
            <span class="formula"><a href="#ref-20" class="data-ref">股价 $XXX.XX</a> / (<a href="#ref-8" class="data-ref">Q1 EPS $X.XX</a> + <a href="#ref-9" class="data-ref">Q2 EPS $X.XX</a> + <a href="#ref-10" class="data-ref">Q3 EPS $X.XX</a> + <a href="#ref-11" class="data-ref">Q4 EPS $X.XX</a>) = XX.Xx</span><br>
            <span class="src-label">S&P Capital IQ</span>（计算值）
          </td>
        </tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>NTM P/E — [TICKER]</td>
          <td class="num">[XX.X]x</td>
          <td class="source-detail">
            <span class="formula"><a href="#ref-20" class="data-ref">股价 $XXX.XX</a> / (<a href="#ref-N" class="data-ref">Q4'25E $X.XX</a> + <a href="#ref-N" class="data-ref">Q1'26E $X.XX</a> + <a href="#ref-N" class="data-ref">Q2'26E $X.XX</a> + <a href="#ref-N" class="data-ref">Q3'26E $X.XX</a>) = XX.Xx</span><br>
            <span class="src-label">S&P Capital IQ</span> — get_consensus_estimates_from_identifiers(identifier='[TICKER]', period_type='quarterly', num_periods_forward=4)。NTM EPS = 未来 4 个季度一致预期平均 EPS 之和。
          </td>
        </tr>

        <!-- 分组：业绩会文字稿论据 -->
        <tr><td colspan="4" class="appendix-group">业绩会文字稿论据</td></tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>[事实，例如：“管理层指引同店销售增长 3-4%”]</td>
          <td class="num">不适用</td>
          <td class="source-detail">
            <span class="excerpt">“我们预计 Q4 同店销售增长 3-4%，主要受食品杂货和健康护理业务持续强劲带动。”</span><br>
            <span class="src-label">来源：</span> <span class="transcript-ref">[Q# FY#### 业绩会文字稿]</span> (key_dev_id: [ID]) — [发言人姓名]，[职务]
          </td>
        </tr>

        <!-- 分组：预测与一致预期 -->
        <tr><td colspan="4" class="appendix-group">预测与一致预期</td></tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>一致预期 EPS — [Q# FY####]</td>
          <td class="num">$[X.XX]</td>
          <td class="source-detail">
            <span class="excerpt">“一致预期 EPS 为 $X.XX，过去 90 天从 $X.XX 上修。”</span><br>
            <a href="https://[source-url-from-kensho-search]" target="_blank" class="src-url">[来源标题 / 发布机构名称]</a><br>
            <span class="src-label">查询：</span> search("[TICKER] 业绩预测 一致预期 EPS 收入 下一季度")
          </td>
        </tr>

        <!-- 分组：新闻与分析师评论 -->
        <tr><td colspan="4" class="appendix-group">新闻与分析师评论</td></tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>[例如：“巴克莱将评级上调至增持”]</td>
          <td class="num">不适用</td>
          <td class="source-detail">
            <span class="excerpt">“巴克莱将 WMT 评级上调至增持，目标价 210 美元，理由是电商增长动能加速。”</span><br>
            <a href="https://[source-url-from-kensho-search]" target="_blank" class="src-url">[来源标题 / 发布机构，日期]</a><br>
            <span class="src-label">查询：</span> search("[TICKER] 分析师评级 目标价 上调 下调")
          </td>
        </tr>

        <!-- 分组：股价表现 -->
        <tr><td colspan="4" class="appendix-group">股价表现</td></tr>
        <tr id="ref-N">
          <td class="ref-id">[N]</td>
          <td>年初至今回报 — [TICKER]</td>
          <td class="num">[+/-X.X%]</td>
          <td class="source-detail">
            <span class="formula">(<a href="#ref-N" class="data-ref">当前 $XXX.XX</a> - <a href="#ref-N" class="data-ref">12 月 31 日收盘价 $XXX.XX</a>) / <a href="#ref-N" class="data-ref">12 月 31 日收盘价 $XXX.XX</a> = X.X%</span><br>
            <span class="src-label">S&P Capital IQ</span>（基于日度价格计算）
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ════════════════════════════════════════════ -->
  <!-- 页脚                                         -->
  <!-- ════════════════════════════════════════════ -->
  <div class="page-footer">
    <div class="footer-disclaimer">分析由 AI 生成，请核验所有输出</div>
    <div class="footer-meta">数据：S&P Capital IQ、Kensho | [年 月 日]</div>
  </div>

</div>

<!-- ════════════════════════════════════════════════ -->
<!-- CHART.JS 脚本                                    -->
<!-- ════════════════════════════════════════════════ -->
<script>
// ── 注册注释插件 ──
// 通过 CDN 加载的 annotation 插件必须显式注册。
// script 标签加载后，该插件会作为全局对象可用。
if (window['chartjs-plugin-annotation']) {
  Chart.register(window['chartjs-plugin-annotation']);
}

// ── Chart 默认值 ──
Chart.defaults.font.family = "'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', Arial, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = '#555';
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.plugins.legend.labels.boxWidth = 12;

// ── 配色方案 ──
const COLORS = {
  navy:     '#1a1a4e',
  blue:     '#3366cc',
  teal:     '#0d9488',
  orange:   '#e67e22',
  red:      '#c0392b',
  green:    '#27ae60',
  purple:   '#8e44ad',
  gray:     '#7f8c8d',
  lightBlue:'#85c1e9',
  gold:     '#f0b429',
};
const COMP_COLORS = [
  COLORS.navy, COLORS.blue, COLORS.teal,
  COLORS.orange, COLORS.red, COLORS.green,
  COLORS.purple, COLORS.gold
];

// ── 辅助函数：收入与 EPS 组合图 ──
function createRevEpsChart(canvasId, labels, revenueData, epsData, revLabel) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: revLabel || '收入 ($B)',
          data: revenueData,
          backgroundColor: COLORS.navy + 'cc',
          borderColor: COLORS.navy,
          borderWidth: 1,
          yAxisID: 'y',
          order: 2
        },
        {
          label: '摊薄 EPS',
          data: epsData,
          type: 'line',
          borderColor: COLORS.orange,
          backgroundColor: COLORS.orange,
          borderWidth: 2.5,
          pointRadius: 4,
          pointBackgroundColor: COLORS.orange,
          tension: 0.3,
          yAxisID: 'y1',
          order: 1
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: {
          position: 'left',
          title: { display: true, text: revLabel || '收入 ($B)', font: { size: 11 } },
          grid: { color: '#eee' }
        },
        y1: {
          position: 'right',
          title: { display: true, text: 'EPS ($)', font: { size: 11 } },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}

// ── 辅助函数：利润率趋势图 ──
function createMarginChart(canvasId, labels, grossMargins, opMargins) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '毛利率 %',
          data: grossMargins,
          borderColor: COLORS.blue,
          backgroundColor: COLORS.blue + '20',
          borderWidth: 2.5,
          pointRadius: 4,
          fill: false,
          tension: 0.3
        },
        {
          label: '营业利润率 %',
          data: opMargins,
          borderColor: COLORS.teal,
          backgroundColor: COLORS.teal + '20',
          borderWidth: 2.5,
          pointRadius: 4,
          fill: false,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          title: { display: true, text: '利润率（%）', font: { size: 11 } },
          grid: { color: '#eee' },
          ticks: { callback: v => v.toFixed(1) + '%' }
        }
      }
    }
  });
}

// ── 辅助函数：收入增速柱状图 ──
function createRevGrowthChart(canvasId, labels, growthData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '收入同比增速 %',
        data: growthData,
        backgroundColor: growthData.map(v => v >= 0 ? COLORS.green + 'cc' : COLORS.red + 'cc'),
        borderColor: growthData.map(v => v >= 0 ? COLORS.green : COLORS.red),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          title: { display: true, text: '增速（%）', font: { size: 11 } },
          grid: { color: '#eee' },
          ticks: { callback: v => v.toFixed(1) + '%' }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
}

// ── 辅助函数：带业绩日期标注的股价图 ──
function createAnnotatedPriceChart(canvasId, labels, prices, earningsDates, ticker) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const annotations = {};
  earningsDates.forEach((ed, i) => {
    let xValue = ed.date;
    const isNeg = ed.move.startsWith('-');
    annotations['earnings' + i] = {
      type: 'line',
      xMin: xValue,
      xMax: xValue,
      borderColor: isNeg ? '#c0392b' : '#0d7a3e',
      borderWidth: 2,
      borderDash: [6, 4],
      label: {
        display: true,
        content: ed.label + ' (' + ed.move + ')',
        position: i % 2 === 0 ? 'start' : 'end',
        backgroundColor: isNeg ? '#c0392b' : '#0d7a3e',
        color: '#fff',
        font: { size: 10, weight: 'bold' },
        padding: { top: 3, bottom: 3, left: 6, right: 6 },
        borderRadius: 3
      }
    };
  });
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: ticker + ' 收盘价',
        data: prices,
        borderColor: COLORS.navy,
        backgroundColor: COLORS.navy + '15',
        borderWidth: 1.5,
        pointRadius: 0,
        pointHitRadius: 4,
        fill: true,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: { type: 'category', ticks: { maxTicksLimit: 12, font: { size: 10 } }, grid: { display: false } },
        y: { title: { display: true, text: '股价（美元）', font: { size: 11 } }, grid: { color: '#eee' } }
      },
      plugins: {
        annotation: { annotations: annotations },
        tooltip: { callbacks: { label: ctx => ticker + ': $' + ctx.raw.toFixed(2) } }
      }
    }
  });
}

// ── 辅助函数：可比公司指数化表现图 ──
// datasets: [{ label: 'TICKER', data: [price1, price2, ...], color: '#xxx', isSubject: true/false }, ...]
function createCompPerfChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const chartDatasets = datasets.map((ds, i) => {
    const base = ds.data[0] || 1;
    return {
      label: ds.label,
      data: ds.data.map(v => (v / base) * 100),
      borderColor: ds.color || COMP_COLORS[i % COMP_COLORS.length],
      backgroundColor: 'transparent',
      borderWidth: ds.isSubject ? 3 : 1.5,
      borderDash: ds.isSubject ? [] : [4, 2],
      pointRadius: 0,
      tension: 0.2
    };
  });
  new Chart(ctx, {
    type: 'line',
    data: { labels: labels, datasets: chartDatasets },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: { title: { display: true, text: '指数化（起点=100）', font: { size: 11 } }, grid: { color: '#eee' } },
        x: { ticks: { maxTicksLimit: 12 } }
      },
      plugins: {
        tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + ctx.raw.toFixed(1) } }
      }
    }
  });
}

// ── 辅助函数：LTM P/E 横向柱状图 ──
// companies: [{ label: 'TICKER', pe: 25.3, isSubject: true/false }, ...]
function createPEChart(canvasId, companies) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  companies.sort((a, b) => b.pe - a.pe);
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: companies.map(c => c.label),
      datasets: [{
        label: 'LTM P/E',
        data: companies.map(c => c.pe),
        backgroundColor: companies.map(c => c.isSubject ? COLORS.navy : COLORS.lightBlue),
        borderColor: companies.map(c => c.isSubject ? COLORS.navy : COLORS.blue),
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      scales: {
        x: {
          title: { display: true, text: 'LTM P/E', font: { size: 11 } },
          grid: { color: '#eee' }
        },
        y: {
          ticks: { font: { size: 12, weight: 'bold' } }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: { label: ctx => 'P/E：' + ctx.raw.toFixed(1) + 'x' }
        }
      }
    }
  });
}

// ═══════════════════════════════════════════════
// 上方已定义辅助函数，请勿重写。
// 只使用这些函数创建图表。
// 不要编写自定义内联 Chart.js 代码。
// ═══════════════════════════════════════════════

</script>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- 图表数据：每个图表单独使用一个 script + try-catch          -->
<!-- 一个图表的语法错误不得影响其他图表。                      -->
<!-- 强制要求：使用上方辅助函数，不要写自定义代码。             -->
<!-- ═══════════════════════════════════════════════════════════ -->

<!-- 图 1：收入与 EPS -->
<script>
try {
  createRevEpsChart('chart-rev-eps',
    ['Q1 FY24','Q2 FY24','Q3 FY24','Q4 FY24','Q1 FY25','Q2 FY25','Q3 FY25','Q4 FY25'],
    [152.3, 161.6, 160.8, 173.4, 161.5, 169.3, 165.8, 178.0],  // 收入，单位：十亿美元
    [1.47, 1.84, 1.53, 1.80, 1.56, 1.92, 1.60, 1.90],          // 摊薄 EPS
    '收入 ($B)'
  );
} catch(e) { console.error('图 1 错误：', e); }
</script>

<!-- 图 2：利润率趋势 -->
<script>
try {
  createMarginChart('chart-margins',
    ['Q1 FY24','Q2 FY24','Q3 FY24','Q4 FY24','Q1 FY25','Q2 FY25','Q3 FY25','Q4 FY25'],
    [24.0, 24.4, 24.2, 23.8, 24.5, 24.8, 24.6, 24.1],  // 毛利率 %
    [4.2, 5.1, 4.5, 4.8, 4.6, 5.3, 4.7, 5.0]            // 营业利润率 %
  );
} catch(e) { console.error('图 2 错误：', e); }
</script>

<!-- 图 3：收入同比增速 — 仅包含可计算同比的季度（最近 4 个） -->
<script>
try {
  createRevGrowthChart('chart-rev-growth',
    ['Q1 FY25','Q2 FY25','Q3 FY25','Q4 FY25'],  // 仅 4 个标签，即有同比数据的季度
    [6.0, 4.8, 3.1, 2.7]                         // 这 4 个季度的收入同比增速 %
  );
} catch(e) { console.error('图 3 错误：', e); }
</script>

<!-- 图 5：带标注的股价走势 -->
<script>
try {
  createAnnotatedPriceChart('chart-price-annotated',
    ['2025-02-18','2025-02-19'],  // ……过去 1 年日度日期标签
    [170.5, 171.2],               // ……日度收盘价
    [
      { date: '2025-05-15', label: 'Q1 FY26', move: '+3.2%' },
      { date: '2025-08-15', label: 'Q2 FY26', move: '-1.8%' }
    ],
    'WMT'
  );
} catch(e) { console.error('图 5 错误：', e); }
</script>

<!-- 图 6：可比公司指数化表现 -->
<script>
try {
  createCompPerfChart('chart-comp-perf',
    ['2025-02-18','2025-03-18'],  // ……日期标签
    [
      { label: 'WMT', data: [170.5, 172.3], isSubject: true },
      { label: 'COST', data: [580.2, 595.1], isSubject: false },
      { label: 'TGT', data: [142.0, 138.5], isSubject: false }
    ]
  );
} catch(e) { console.error('图 6 错误：', e); }
</script>

<!-- 图 7：LTM P/E 对比 -->
<script>
try {
  createPEChart('chart-pe-comp', [
    { label: 'COST', pe: 52.3, isSubject: false },
    { label: 'WMT', pe: 28.1, isSubject: true },
    { label: 'TGT', pe: 15.6, isSubject: false },
    { label: 'BJ', pe: 22.4, isSubject: false }
  ]);
} catch(e) { console.error('图 7 错误：', e); }
</script>

</body>
</html>
```

## Chart.js 实现说明

### 图 1：收入与 EPS 图
- **类型**：柱状图 + 折线图组合
- **柱状图**：季度收入，使用左侧 y 轴
- **折线图**：摊薄 EPS，使用右侧 y 轴
- **标签**：季度标识（例如 `"Q1 FY24"`）
- 使用 8 个季度的数据

### 图 2：利润率趋势图
- **类型**：双折线图
- **折线**：毛利率和营业利润率
- **Y 轴**：百分比，保留 1 位小数

### 图 3：收入增速图
- **类型**：带条件配色的柱状图
- **绿色柱**：正增长季度
- **红色柱**：负增长季度
- **重要**：只包含可以计算同比的季度，即 `financials.csv` 中同时存在当前季度和去年同期季度的数据。使用 8 个季度原始数据时，通常只能得到 4 根柱，而不是 8 根。不要传入没有同比数据的季度标签。
- 不需要图例，图形含义应自明

### 图 4：业务分部收入
- 使用 HTML 表格，不使用图表
- 列：分部 | 最近季度收入（百万美元） | 占总收入比例 | 同比变化
- 同比变化单元格使用 `pos` / `neg` class 做颜色标记

### 图 5：带业绩日期标注的股价图
- **类型**：折线图，使用 annotation 插件添加竖线
- **数据**：过去 1 年日度收盘价
- **标注**：每个业绩发布日期放置一条竖向虚线
- **标签**：季度名称 + 业绩发布后 1 个交易日股价变动
- **颜色**：正向反应用绿色，负向反应用红色
- **1 日变动计算**：比较业绩发布日期收盘价与下一交易日收盘价
- **关键**：创建图表前必须注册 annotation 插件：`Chart.register(window['chartjs-plugin-annotation'])`。模板脚本块中已包含该逻辑。

### 图 6：可比公司指数化表现图
- **类型**：多折线图，统一重设起点为 100
- **标的公司**：较粗实线（`borderWidth: 3`）
- **可比公司**：较细虚线（`borderWidth: 1.5`、`borderDash`）
- 这种视觉层级可以让标的公司一眼可辨

### 图 7：LTM P/E 对比图
- **类型**：横向柱状图
- **标的公司**：使用深蓝色高亮（#1a1a4e）
- **可比公司**：使用浅蓝色（#85c1e9）
- **排序**：按 P/E 降序排列
- 一眼展示公司相对同业是溢价还是折价交易

### 图 8：可比公司对比表
- 使用 HTML 表格，并用 `highlight-row` 高亮标的公司
- 列：Ticker | 公司 | 市值（十亿美元） | LTM P/E | NTM P/E | YTD % | 1 年 %
- 回报率使用 `pos` / `neg` class 做颜色标记

## 格式约定

### 数字
- 收入：十亿美元口径保留 1 位小数（例如 `"$152.3B"`），百万美元口径不保留小数（例如 `"$4,521M"`）
- EPS：保留 2 位小数（例如 `"$1.47"`）
- 利润率：保留 1 位小数并带 `%`（例如 `"24.5%"`）
- 增速：保留 1 位小数并带正负号（例如 `"+5.2%"`、`"-3.1%"`）
- 市值：十亿美元口径保留 1 位小数（例如 `"$562.1B"`）
- 股价：保留 2 位小数（例如 `"$172.35"`）
- P/E 倍数：保留 1 位小数并带 `x` 后缀（例如 `"25.3x"`）

### 颜色标记
- 正值：`class="pos"`，绿色（#0d7a3e）
- 负值：`class="neg"`，红色（#c0392b）
- 中性/持平：`class="neutral"`，灰色（#555）
- 标的公司行：`class="highlight-row"`，浅蓝色背景

### 图表标签
- 所有图表按顺序编号：`图 1：`、`图 2：` 等
- 图 1-8 位于第 3-5 页，第 2 页的一致预期表不编号
- 每个图表和表格下方都必须标注来源：`来源：S&P Capital IQ`

### 超链接论据
- 报告正文中的每个事实性判断，无论是数字还是定性表述，都必须包在 `<a href="#ref-N" class="data-ref">论据文本</a>` 中
- `ref-N` ID 必须匹配附录表中的一行
- 适用范围包括叙述文字、要点列表、表格单元格、blockquote，以及任何出现事实的地方
- 图表坐标轴标签和 tooltip 不需要超链接，只有报告正文需要
- 撰写报告时按顺序分配引用 ID（`ref-1`、`ref-2` 等）
- 多处引用同一底层事实时，应共用同一个 ref ID
- 对定性论据，包住关键短语即可：`<a href="#ref-25" class="data-ref">管理层提示关税逆风</a>`

### 附录
- **必须以此开头**：`<div class="ai-disclaimer">分析由 AI 生成，请核验所有输出</div>`
- 附录是报告最后一节，位于所有图表之后
- **4 列**：编号 | 事实 | 数值 | 来源与推导
- 报告中引用的每个唯一论据各占一行，包括数字论据和非数字论据
- **报告正文中的每个数字都必须是可点击的 `<a href="#ref-N">` 链接，并跳转到对应附录行。没有例外。**
- 按类别分组：季度财务数据、估值、业绩会文字稿论据、预测与一致预期、新闻与分析师评论、股价表现
- 使用小标题行（`appendix-group` class）分隔分组
- **“来源与推导”列必须为每一行提供具体、详细的来源说明：**
  - 原始 S&P 数据（收入、EPS、价格、市值等）：`<span class="src-label">S&P Capital IQ</span>` 后接带参数的具体 MCP 函数调用，例如 `get_financial_line_item_from_identifiers(identifier='WMT', line_item='revenue', period_type='quarterly', period='Q3 FY2026')`。**不得只写 “S&P Capital IQ” 而没有细节。**
  - 计算值（利润率、增速、P/E、回报率）：写出完整公式，并用 `<a class="data-ref">` 超链接到每个组成项所在行（使用 `formula` CSS class）。**公式中的每个数字都必须可点击，并链接到自己的附录行。**
  - 业绩会文字稿论据：使用斜体逐字摘录句子（`excerpt` CSS class）+ 带 `transcript-ref` class 的文字稿名称 + `key_dev_id`
  - Kensho 结果：关键发现（`excerpt` class）+ **可点击来源 URL**，格式为 `<a href="[URL]" target="_blank" class="src-url">[来源标题]</a>` + 使用过的搜索查询。**每一条 Kensho 来源论据都必须链接到原始来源。**
- 来源标签使用 `src-label` CSS class（加粗深蓝）
- 外部来源 URL 使用 `src-url` CSS class（蓝色、下划线、可点击）

### 风格规则
- **报告任何位置都不得使用表情符号**。标题、表格、图表标签和正文都不得出现表情符号。这是一份专业研究文档。
- 字体：全文使用中文优先字体栈（正文、标题、表格、图表），例如 Microsoft YaHei / PingFang SC / Noto Sans CJK SC，并保留 Arial 作为备用字体。
- 管理层引述：作为 `<blockquote>` 元素嵌入核心观点叙述中，不要单独设立标题。
- 文字保持精炼。正文目标总长度为打印后 4-5 页，附录另计。
