# Financial Services CN

面向中国大陆投资者和机构金融工作流的中文 Codex 金融服务插件。它参考 `anthropics/financial-services` 的 README 信息架构，并按本仓库实际能力改写：A 股优先，兼容港股和美股，覆盖建模、估值、投行材料、权益研究、私募股权、财富管理、基金运营、KYC、LSEG 和 S&P Global 数据工作流。默认安装只加载技能，不自动初始化付费机构源或本地 MCP。

> [!IMPORTANT]
> 本仓库不构成投资、法律、税务、会计或监管建议。所有技能只用于辅助起草分析材料、模型、备忘录、研究笔记、核对表、报告包和演示材料，输出必须由具备资质的专业人员复核。技能不会作出投资建议、执行交易、绑定风险、入账、批准客户准入或对外分发材料。

## Getting Started（安装或更新到 Codex）

安装命令按操作系统区分：macOS/Linux 使用 bash 或 zsh，Windows 使用 PowerShell。两条命令做同一件事：把插件源码放到用户目录下的 `plugins/financial-services-cn`，写入个人 marketplace，然后执行 `codex plugin add financial-services-cn@personal`。

### macOS / Linux

复制下面整段命令执行，即可安装或更新到 Codex：

```bash
mkdir -p "$HOME/plugins" "$HOME/.agents/plugins" && (git clone --branch main https://github.com/Qmeasure/codex-financial-cn.git "$HOME/plugins/financial-services-cn" 2>/dev/null || (git -C "$HOME/plugins/financial-services-cn" checkout main && git -C "$HOME/plugins/financial-services-cn" pull --ff-only origin main)) && python3 -c 'import json,pathlib;p=pathlib.Path.home()/".agents/plugins/marketplace.json";data=json.loads(p.read_text()) if p.exists() else {"name":"personal","interface":{"displayName":"Personal"},"plugins":[]};entry={"name":"financial-services-cn","source":{"source":"local","path":"./plugins/financial-services-cn"},"policy":{"installation":"AVAILABLE","authentication":"ON_INSTALL"},"category":"Finance"};plugins=data.setdefault("plugins",[]);plugins[:]=[x for x in plugins if not (isinstance(x,dict) and x.get("name")=="financial-services-cn")]+[entry];data.setdefault("name","personal");data.setdefault("interface",{"displayName":"Personal"});p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")' && codex plugin add financial-services-cn@personal
```

### Windows PowerShell

复制下面整段命令到 PowerShell 执行，即可安装或更新到 Codex：

```powershell
$repo='https://github.com/Qmeasure/codex-financial-cn.git'; $plugin=Join-Path $HOME 'plugins\financial-services-cn'; $market=Join-Path $HOME '.agents\plugins\marketplace.json'; New-Item -ItemType Directory -Force -Path (Split-Path $plugin),(Split-Path $market) | Out-Null; if (Test-Path $plugin) { git -C $plugin checkout main; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; git -C $plugin pull --ff-only origin main } else { git clone --branch main $repo $plugin }; py -3 -c "import json,pathlib; p=pathlib.Path.home()/'.agents/plugins/marketplace.json'; data=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'name':'personal','interface':{'displayName':'Personal'},'plugins':[]}; entry={'name':'financial-services-cn','source':{'source':'local','path':'./plugins/financial-services-cn'},'policy':{'installation':'AVAILABLE','authentication':'ON_INSTALL'},'category':'Finance'}; plugins=data.setdefault('plugins',[]); plugins[:]=[x for x in plugins if not (isinstance(x,dict) and x.get('name')=='financial-services-cn')]+[entry]; data.setdefault('name','personal'); data.setdefault('interface',{'displayName':'Personal'}); p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')" ; codex plugin add financial-services-cn@personal
```

Windows 命令默认使用 `py -3`。电脑上只有 `python` 命令时，把上面命令里的 `py -3` 替换为 `python`。

上述安装或更新命令会自动完成：

1. 将本仓库 clone 或更新到 `~/plugins/financial-services-cn`。
2. 新建或合并个人 marketplace entry。
3. 执行 `codex plugin add financial-services-cn@personal`。

已经安装过本插件的用户，后续更新时重新运行对应系统的同一条安装命令即可。命令会先拉取 GitHub 最新代码，再让 Codex 安装当前插件版本快照。安装或更新完成后，开启一个新的 Codex 线程，让 Codex 重新加载插件技能。默认安装不会自动登录或启动任何机构 MCP、本地 MCP 或付费数据源。

`codex plugin add` 会把当前源码复制成安装快照，路径形如 `~/.codex/plugins/cache/personal/financial-services-cn/<version>`。这是 Codex 的正常安装缓存，不是用户需要手工维护的源码目录；源码目录仍是 `~/plugins/financial-services-cn`，更新时继续重新运行上面的安装或更新命令。

本地开发时，在本仓库根目录执行下面这条 macOS/Linux 命令，即可把当前 checkout 安装到 Codex：

```bash
mkdir -p "$HOME/plugins" "$HOME/.agents/plugins" && ln -sfn "$PWD" "$HOME/plugins/financial-services-cn" && python3 -c 'import json,pathlib;p=pathlib.Path.home()/".agents/plugins/marketplace.json";data=json.loads(p.read_text()) if p.exists() else {"name":"personal","interface":{"displayName":"Personal"},"plugins":[]};entry={"name":"financial-services-cn","source":{"source":"local","path":"./plugins/financial-services-cn"},"policy":{"installation":"AVAILABLE","authentication":"ON_INSTALL"},"category":"Finance"};plugins=data.setdefault("plugins",[]);plugins[:]=[x for x in plugins if not (isinstance(x,dict) and x.get("name")=="financial-services-cn")]+[entry];data.setdefault("name","personal");data.setdefault("interface",{"displayName":"Personal"});p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")' && codex plugin add financial-services-cn@personal
```

Windows 本地开发建议直接把 checkout 放在 `$HOME\plugins\financial-services-cn`，然后运行上面的 Windows PowerShell 安装或更新命令。所有命令都是一键命令；不需要用户手写 marketplace JSON。

## What's in the repo（仓库里有什么）

- **一个 Codex 插件**：根级 `.codex-plugin/plugin.json` 声明 `financial-services-cn`。
- **66 个扁平技能**：所有 source skills 直接位于 `skills` 目录，每个技能目录包含 `SKILL.md`。
- **本地 reference 格式合同**：每个 skill 都有 `references/cn-markdown-formatting.md` 和 `references/data-query-order.md`；承诺 DOCX、XLSX、PPTX、HTML 或独立图表/ZIP 文件的 skill 还会带对应类型的本地格式合同。
- **数据源发现 Gate**：所有 skill 的外部数据流程都要求先生成“数据源发现记录”，列明 MCP、connector、已授权源、用户文件和降级理由，Gate 通过前不得网页搜索或生成正式交付物。
- **图表样式 Gate**：DOCX、PPTX、独立图表和旧图表 workflow 都写入柱状图网格线规则；柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线。
- **可选 MCP 模板**：`OPTIONAL_MCP_SERVERS.json` 集中记录机构数据源和中国市场相关入口；根目录不放 `.mcp.json`，避免 Codex 自动加载。
- **中文金融规则文档**：`DATA_SOURCES_CN.md` 规定数据来源优先级，`CN_OUTPUT_FORMATTING.md` 规定中文金融产物格式，`CN_DOCX_OUTPUT_CONTRACT.md`、`CN_XLSX_OUTPUT_CONTRACT.md`、`CN_PPTX_OUTPUT_CONTRACT.md` 和 `CN_MARKDOWN_OUTPUT_CONTRACT.md` 规定文件交付契约。
- **校验脚本**：`scripts` 目录提供结构检查、中文化门禁、中文产物样例检查和版本辅助脚本。

本仓库不内置旧式多插件包装层、独立代理包、旧平台动作目录或托管代理模板。安装、使用和维护都围绕 `financial-services-cn` 进行。

## Agents（工作流入口）

上游 README 的 `Agents` 段用于介绍独立端到端工作流入口。本仓库的对应事实是：不发布独立代理包，不提供托管代理模板，也不需要用户选择多个工作流包。安装 `financial-services-cn` 后，用户可以在 Codex 中用中文自然语言描述任务，也可以用 `$financial-services-cn:<skill-name>` 显式调用某个 skill，例如 `$financial-services-cn:earnings-analysis 分析拼多多最新财报`。Codex 会根据 `skills` 目录中的技能匹配金融建模、投行、权益研究、私募股权、财富管理、基金运营、KYC、LSEG 或 S&P Global 工作流。

如果机构要固定自己的端到端流程，应改写相关技能的中文版执行契约、数据来源规则和产物格式规则，而不是新增旧架构目录。

## Repository Layout（仓库结构）

```text
.codex-plugin/plugin.json      Codex 插件 manifest
OPTIONAL_MCP_SERVERS.json      可选 MCP server 配置模板，默认不自动加载
skills                         66 个中文金融技能
skills/*/references            每个技能的本地格式合同和数据查询顺序合同
scripts                        结构校验、中文化门禁和产物样例校验
DATA_SOURCES_CN.md             中国市场数据来源规则
CN_OUTPUT_FORMATTING.md        中文金融产物格式规则
CN_DOCX_OUTPUT_CONTRACT.md     中文 DOCX/Word 交付契约
CN_XLSX_OUTPUT_CONTRACT.md     中文 XLSX/Excel 交付契约
CN_PPTX_OUTPUT_CONTRACT.md     中文 PPTX/PowerPoint 交付契约
CN_MARKDOWN_OUTPUT_CONTRACT.md 中文 Markdown/聊天正文交付契约
OPTIONAL_MCP_TEMPLATES.md      可选 MCP 接入说明
OPENBB_MCP_CODEX_SETUP.md     OpenBB 金融数据 MCP 本地安装与 Codex 接入教程
ACCEPTANCE_SAMPLES_CN.md       中文产物验收样例
THIRD_PARTY_NOTICES.md         第三方许可说明
```

## 如何使用

安装后，在 Codex 中可以用自然语言描述任务，也可以用 `$financial-services-cn:<skill-name>` 显式调用某个 skill，例如：

- “按 A 股优先口径分析这家公司，并标注港股和美股可比口径。”
- `$financial-services-cn:earnings-analysis 分析拼多多最新财报`
- `$financial-services-cn:pitch-deck 用这些材料填充中文 pitch deck`
- `$financial-services-cn:xlsx-author 生成中文三表模型并标注来源`

所有输出默认遵守：

- A 股优先，港股和美股兼容。
- 官方披露、用户文件和已授权数据源优先。
- 需要外部数据时，先读取本 skill 的 `references/data-query-order.md`，生成“数据源发现记录”，列出可用/不可用 MCP、connector、已授权源、用户文件、覆盖缺口和降级理由；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物。
- 监管、会计、KYC、基金文件、月结和客户适当性判断缺少依据时写“需确认”。
- DOCX、PPTX、XLSX、Markdown、表格、图表、脚注和最终摘要必须使用中文金融语境。
- 正式文件输出前，先读取本 skill 的 `references/cn-*-formatting.md`；聊天摘要不能冒充已经生成的文件交付物。
- DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写保留。

## How It Fits Together（它们如何配合）

| 组成 | 作用 | 位置 |
|---|---|---|
| 插件 manifest | 声明插件名称、版本、展示信息和技能目录；默认不声明 MCP，避免安装后自动握手失败 | `.codex-plugin/plugin.json` |
| 技能 | 写入金融领域方法、执行步骤、产物要求和中文执行契约 | `skills` |
| Skill 调用 | 支持自然语言自动匹配，也支持 `$financial-services-cn:<skill-name>` 显式调用 | `skills/*/SKILL.md` |
| MCP servers | 可选数据源模板；用户确认授权、登录和本地服务可用后再按需配置 | `OPTIONAL_MCP_SERVERS.json` |
| 数据来源规则 | 约束来源优先级、授权判断、缺失依据时的“需确认”表达 | `DATA_SOURCES_CN.md` |
| 中文产物规则 | 约束中文字体、日期、币种、单位、表格、图表、免责声明和摘要 | `CN_OUTPUT_FORMATTING.md` |
| DOCX 交付契约 | 约束中文 Word 的 preset、OOXML 字体、表格几何、真实编号、超链接和 render QA 降级说明 | `CN_DOCX_OUTPUT_CONTRACT.md` |
| XLSX 交付契约 | 约束中文工作簿、公式优先、颜色约定、来源/假设/检查区和结构校验 | `CN_XLSX_OUTPUT_CONTRACT.md` |
| PPTX 交付契约 | 约束中文幻灯片标题、字体、图表、来源脚注、无溢出和视觉 QA | `CN_PPTX_OUTPUT_CONTRACT.md` |
| Markdown 交付契约 | 约束中文标题层级、表格、来源、链接、免责声明和聊天输出边界 | `CN_MARKDOWN_OUTPUT_CONTRACT.md` |
| 本地 reference 格式合同 | 让每个 skill 在安装快照内直接读取自己的 Markdown、DOCX、XLSX、PPTX、HTML 或图表格式规则 | `skills/*/references/cn-*-formatting.md` |
| 本地数据查询顺序 | 约束外部数据任务先生成数据源发现记录；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物 | `skills/*/references/data-query-order.md` |
| 校验脚本 | 防止旧架构残留、英文模板残留、manifest 错误和中文产物样例退化 | `scripts` |

## Reference Formatting 与数据查询链路

Codex 安装插件时会把仓库复制成插件快照。为避免 skill 执行时只看到 `SKILL.md`、却没有继续读取根级格式文件，本仓库把关键格式要求下沉到每个 skill 自己的 `references` 目录：

- 所有 66 个 skill 都包含 `references/cn-markdown-formatting.md`，用于聊天摘要、正式 Markdown、表格、来源、免责声明和最终交付说明。
- 所有 66 个 skill 都包含 `references/data-query-order.md`。只要任务需要外部数据、行情、财报、行业、公司、宏观、监管、KYC、基金、月结或第三方数据库信息，就必须先填写“数据源发现记录”，列出用户文件、当前会话可用 MCP/connector、本地数据库、已授权终端、适用数据源、调用或未调用原因、覆盖缺口和降级路径。
- Gate 未通过时，不得网页搜索，不得抓取公司官网、SEC 或交易所页面，也不得生成正式报告或文件交付物；一致预期、估值倍数、市场份额、行业数据和宏观数据等授权源缺口必须写“需终端复核”。
- 承诺文件交付的 skill 会额外包含本地类型合同：DOCX 15 个、XLSX 18 个、PPTX 11 个、HTML 1 个、独立图表/ZIP 1 个。
- 图表相关合同和旧图表 workflow 都包含同一条硬规则：柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线；除非用户明确要求或图表类型必须依赖网格线，否则不得显示 major/minor gridlines。
- 旧 workflow/reference 文件只保留业务流程和参考口径；它们入口处只指向新的本地格式合同，不把新增格式正文追加进旧文件。
- `pitch-deck` 保留既有 `reference/` 目录，但新增格式合同仍放在 `references/`，旧 reference 文件通过短提示指向新文件。

当前本地格式文件包括：

| 文件 | 用途 |
|---|---|
| `references/cn-markdown-formatting.md` | 中文 Markdown、聊天摘要、表格、来源、免责声明和最终交付说明 |
| `references/data-query-order.md` | 外部数据查询 Gate：先生成数据源发现记录，Gate 通过前不得网页搜索或生成正式交付物 |
| `references/cn-docx-formatting.md` | 中文 Word 页面、字体、OOXML、表格、编号、超链接和 render QA |
| `references/cn-xlsx-formatting.md` | 中文 Excel sheet、公式、颜色、来源、假设、检查区和结构校验 |
| `references/cn-pptx-formatting.md` | 中文 PowerPoint 标题、字体、图表、来源、无溢出和视觉 QA |
| `references/cn-html-formatting.md` | 中文 HTML 字体、响应式表格、链接、免责声明和浏览器打开校验 |
| `references/cn-chart-formatting.md` | 独立图表、图片和 ZIP 的中文标题、坐标轴、图例、来源和分辨率 |

## Vertical Plugins（技能领域）

| 领域 | 能力摘要 |
|---|---|
| 金融分析 | DCF、LBO、三表模型、可比公司、Excel 审计、PPT 质检、数据清洗 |
| 投资银行 | CIM、teaser、买方名单、并购模型、流程函、交易跟踪、数据包和 pitch deck 填充 |
| 权益研究 | 业绩分析、业绩预览、首次覆盖、模型更新、晨会纪要、行业报告、催化剂跟踪 |
| 私募股权 | 项目来源、项目筛选、尽调清单、尽调会议准备、投委会备忘录、组合监控、价值创造计划 |
| 财富管理 | 客户回顾、财务规划、投资建议书、组合再平衡、客户报告、税损收割 |
| 基金运营 | 总账对账、差异追踪、预提明细、滚动表、NAV 勾稽、波动说明 |
| KYC 与运营 | KYC 文件解析、KYC/AML 规则评估、缺失项和升级事项标记 |
| LSEG 数据工作流 | 债券相对价值、期货基差、掉期曲线、外汇套息、期权波动率、固收组合、宏观利率监控 |
| S&P Global 数据工作流 | 公司速览、融资摘要、业绩预览和 Capital IQ 相关材料 |

## MCP Integrations（MCP 集成）

`OPTIONAL_MCP_SERVERS.json` 当前保留以下可选 MCP 入口。根目录不提供 `.mcp.json`，所以 Codex 默认安装不会自动启用这些 MCP；实际使用前需要用户确认本地环境、账号、token、订阅和数据授权。无法确认时，技能必须写“需确认”。

| 名称 | 类型 | 入口 |
|---|---|---|
| `daloopa` | 机构数据源 | `https://mcp.daloopa.com/server/mcp` |
| `morningstar` | 机构数据源 | `https://mcp.morningstar.com/mcp` |
| `sp-global` | S&P Global / Kensho | `https://kfinance.kensho.com/integrations/mcp` |
| `factset` | 机构数据源 | `https://mcp.factset.com/mcp` |
| `moodys` | Moody's 数据源 | `https://api.moodys.com/genai-ready-data/m1/mcp` |
| `mtnewswire` | 新闻数据源 | `https://vast-mcp.blueskyapi.com/mtnewswires` |
| `aiera` | 会议和文字稿数据源 | `https://mcp-pub.aiera.com` |
| `lseg` | LSEG 分析入口 | `https://api.analytics.lseg.com/lfa/mcp` |
| `lseg-server-cl` | LSEG server-cl 入口 | `https://api.analytics.lseg.com/lfa/mcp/server-cl` |
| `pitchbook` | PitchBook 数据源 | `https://premium.mcp.pitchbook.com/mcp` |
| `chronograph` | Chronograph 数据源 | `https://ai.chronograph.pe/mcp` |
| `egnyte` | 文档数据源 | `https://mcp-server.egnyte.com/mcp` |
| `openbb-cn-market` | 本地中国市场工具 | `http://127.0.0.1:8001/mcp` |
| `tushare-pro` | 本地 Tushare Pro 工具 | `python -m tushare_mcp_server.main`，通过 `TUSHARE_TOKEN` 读取 token |
| `akshare-one` | 本地 AKShare 工具 | `uvx akshare-one-mcp` |

机构数据源通常需要订阅或 API key。OpenBB、Tushare 和 AKShare 相关入口只在用户确认本地服务、依赖和授权可用后使用。这样安装插件时不会弹出未登录、未授权或本地服务未启动的 MCP startup warning。

如需从零安装 OpenBB MCP，请参考 [OpenBB MCP Codex 接入教程](./OPENBB_MCP_CODEX_SETUP.md)。该教程说明如何安装 OpenBB、A股/港股和全球公开数据源、`openbb-mcp-server`，并通过 stdio 接入个人 `~/.codex/config.toml`；这仍然是用户主动配置的可选数据源，不会随插件安装自动启用。

## 中国大陆投资者优化

- **A 股优先**：未指定市场时，默认按 A 股公司、人民币、A 股交易日、交易所公告和中国会计语境处理。
- **跨市场可比**：涉及港股、美股或 ADR 时，必须标注交易所、币种、会计准则、数据日期、汇率来源和是否统一口径。
- **中文产物格式**：中文标题、表头、脚注、图例、来源说明和免责声明不得沿用英文默认版式。
- **来源可追溯**：每个关键结论应能追溯到用户文件、官方披露、MCP/数据库名称、公告日期、数据日期或页码。
- **谨慎边界**：缺少官方材料、用户政策或授权数据支持的监管、会计、KYC、税务、基金运营和客户适当性判断，一律写“需确认”。

## Making It Yours（按机构定制）

这些技能是中文金融工作流模板。落地到具体机构时，建议按以下方式调整：

- **替换或启用数据源**：在用户确认授权后，将 `OPTIONAL_MCP_SERVERS.json` 中需要的入口复制到个人 Codex MCP 配置，或按机构环境改写为内部数据库和本地市场数据服务。
- **加入机构语境**：把公司术语、投资标准、KYC 政策、审批流程和材料规范写进相关技能。
- **带入模板**：用用户提供的 PPT、Excel、DOCX 模板约束版式，但保留中文来源脚注、币种、单位和免责声明。
- **调整技能边界**：只扩展真实需要的工作流，不引入与本仓库单插件形态冲突的旧架构入口。
- **保留审计链**：模型、报告和演示材料必须说明数据来源、口径限制和待人工复核事项。

## Skill Reference（技能调用参考）

所有技能都可以由 Codex 按自然语言任务自动匹配；需要强制指定时，在技能名前加 `$financial-services-cn:`，例如 `$financial-services-cn:dcf-model`。

### 金融分析

| 技能 | 用途 |
|---|---|
| `comps-analysis` | 构建可比公司分析、估值倍数和同业基准。 |
| `dcf-model` | 创建 DCF 估值模型、WACC 和敏感性分析。 |
| `lbo-model` | 填充和验证 LBO 模型模板。 |
| `3-statement-model` | 补全利润表、资产负债表和现金流量表模型。 |
| `audit-xls` | 审核 Excel 模型公式、硬编码、勾稽和平衡检查。 |
| `clean-data-xls` | 清理、规范化和去重电子表格数据。 |
| `deck-refresh` | 用新数据刷新演示材料中的数字、图表和表格。 |
| `competitive-analysis` | 构建竞争格局、同业比较和市场定位分析。 |
| `ib-check-deck` | 对投行演示材料做发送前质量检查。 |
| `pptx-author` | 在无界面环境生成 `.pptx` 文件。 |
| `xlsx-author` | 在无界面环境生成 `.xlsx` 文件。 |
| `ppt-template-creator` | 将用户 PowerPoint 模板整理为可复用 PPT 模板技能。 |
| `skill-creator` | 创建或更新本仓库风格的 Codex skill。 |

### 投资银行

| 技能 | 用途 |
|---|---|
| `strip-profile` | 创建投行公司简介页和客户演示公司画像。 |
| `pitch-deck` | 用来源数据填充既有投行 pitch deck 模板。 |
| `datapack-builder` | 从 CIM、披露文件和数据源构建投资分析数据包。 |
| `cim-builder` | 起草卖方 M&A 保密信息备忘录。 |
| `teaser` | 起草匿名一页式 teaser。 |
| `buyer-list` | 建立战略买方和财务买方清单。 |
| `merger-model` | 构建 M&A 增厚/摊薄和 pro forma EPS 分析。 |
| `process-letter` | 起草流程函、投标指引和管理层会议邀请。 |
| `deal-tracker` | 跟踪交易里程碑、截止日期、行动事项和状态。 |

### 权益研究

| 技能 | 用途 |
|---|---|
| `equity-research` | 生成股票研究快照和基本面分析。 |
| `earnings-analysis` | 起草业绩后季度更新报告。 |
| `earnings-preview` | 构建业绩发布前情景、预测和交易关注点。 |
| `earnings-preview-beta` | 为单家公司生成简洁业绩预览报告。 |
| `initiating-coverage` | 创建机构级首次覆盖报告工作流。 |
| `model-update` | 用新业绩、指引或假设更新财务模型。 |
| `morning-note` | 起草晨会纪要、隔夜进展和交易想法。 |
| `sector-overview` | 创建行业和板块格局报告。 |
| `thesis-tracker` | 维护组合持仓和观察名单投资论点。 |
| `catalyst-calendar` | 跟踪覆盖池未来催化剂日历。 |
| `idea-generation` | 运行股票筛选、主题扫描和投资想法生成。 |

### 私募股权

| 技能 | 用途 |
|---|---|
| `deal-sourcing` | 寻找目标公司、检查关系并起草创始人外联。 |
| `deal-screening` | 快速筛选流入项目、CIM 和 teaser。 |
| `dd-checklist` | 生成和跟踪尽职调查清单。 |
| `dd-meeting-prep` | 准备管理层会议、专家访谈和客户访谈问题。 |
| `unit-economics` | 分析 ARR cohort、LTV/CAC、净留存和收入质量。 |
| `returns-analysis` | 构建 IRR/MOIC 回报敏感性分析。 |
| `ic-memo` | 起草投资委员会备忘录。 |
| `portfolio-monitoring` | 跟踪组合公司 KPI、预算差异和契约风险。 |
| `value-creation-plan` | 构建收购后 100 天计划和 EBITDA bridge。 |
| `ai-readiness` | 评估组合公司 AI 机会和落地优先级。 |

### 财富管理

| 技能 | 用途 |
|---|---|
| `client-review` | 准备客户回顾会议材料和谈话要点。 |
| `financial-plan` | 构建退休、教育、遗产和现金流规划。 |
| `portfolio-rebalance` | 分析组合偏离并生成税务敏感的再平衡建议。 |
| `client-report` | 生成面向客户的业绩报告。 |
| `investment-proposal` | 创建潜在客户投资建议书。 |
| `tax-loss-harvesting` | 识别税损收割机会和 wash sale 风险。 |

### 基金运营

| 技能 | 用途 |
|---|---|
| `gl-recon` | 执行总账与子账对账并分类差异。 |
| `break-trace` | 将对账差异追溯到来源交易或入账记录。 |
| `accrual-schedule` | 构建期末预提明细和 JE 草稿。 |
| `roll-forward` | 构建资产负债表科目滚动表。 |
| `variance-commentary` | 为 P&L 和资产负债表差异撰写波动说明。 |
| `nav-tieout` | 将 LP statement 与基金 NAV pack 勾稽。 |

### KYC 与运营

| 技能 | 用途 |
|---|---|
| `kyc-doc-parse` | 解析开户和准入资料包为结构化 KYC 字段。 |
| `kyc-rules` | 应用 KYC/AML 规则表、评级并标记升级事项。 |

### LSEG 和固定收益

| 技能 | 用途 |
|---|---|
| `bond-relative-value` | 分析债券相对价值、信用利差和利率冲击。 |
| `bond-futures-basis` | 分析债券期货基差、CTD 和隐含回购利率。 |
| `fixed-income-portfolio` | 审阅固收组合、现金流、久期和 DV01。 |
| `fx-carry-trade` | 评估外汇套息交易机会和 carry-to-vol 比率。 |
| `swap-curve-strategy` | 分析掉期曲线、利差和曲线交易策略。 |
| `option-vol-analysis` | 分析期权波动率曲面、Greeks 和波动率交易。 |
| `macro-rates-monitor` | 构建宏观经济、收益率曲线和利率监控 dashboard。 |

### S&P Global 和资本市场数据

| 技能 | 用途 |
|---|---|
| `tear-sheet` | 使用 S&P Capital IQ 相关数据生成公司速览。 |
| `funding-digest` | 汇总融资轮次和资本市场活动为简报材料。 |

## 本地开发与校验

修改本仓库后，至少运行：

```bash
python3 scripts/check.py
python3 scripts/check_cn_localization.py
python3 scripts/check_cn_artifact_samples.py
python3 /Users/lesterbot/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

这些检查会覆盖：

- 根级 Codex manifest、可选 MCP 模板和技能目录结构。
- 66 个 skill 的本地 `references/cn-markdown-formatting.md` 和 `references/data-query-order.md`。
- 66 个 skill 的 `SKILL.md` 是否明确数据源发现记录和网页搜索前 Gate。
- DOCX、XLSX、PPTX、HTML、独立图表/ZIP skill 的本地格式合同和最终交付门槛。
- 根级和本地 DOCX/PPTX/图表合同是否包含柱状图网格线规则；PPTX 样例会检查 chart XML 中没有可见 `majorGridlines` / `minorGridlines`。
- 旧 workflow/reference 文件是否只指向本地格式合同，而不是承载新增格式正文。
- 禁止的旧架构目录或文本残留。
- 中文化门禁、中文金融规则引用和英文模板残留。
- XLSX、PPTX、DOCX、Markdown 中文产物样例。
- Codex 插件 manifest schema。

如果 `python3 scripts/check_cn_artifact_samples.py` 因本机缺少 `python-pptx` 或 `openpyxl` 失败，可以在临时 venv 中安装这两个包后重跑该脚本；不要为了跑样例检查而把临时依赖写进仓库。

## Contributing（贡献规则）

- 新增或改写技能时，必须包含“中文版执行契约”，并引用插件根目录 `../../DATA_SOURCES_CN.md`、`../../CN_OUTPUT_FORMATTING.md` 和对应产物合同；生成 DOCX/XLSX/PPTX/Markdown 文件时分别引用 `../../CN_DOCX_OUTPUT_CONTRACT.md`、`../../CN_XLSX_OUTPUT_CONTRACT.md`、`../../CN_PPTX_OUTPUT_CONTRACT.md`、`../../CN_MARKDOWN_OUTPUT_CONTRACT.md`。
- 每个 skill 必须有 `references/cn-markdown-formatting.md` 和 `references/data-query-order.md`；承诺 DOCX、XLSX、PPTX、HTML 或独立图表/ZIP 文件时，必须新增对应 `references/cn-*-formatting.md` 并在 `SKILL.md` 的“生成正式输出前必须读取”中引用。
- 不把新增中文 Formatting 正文追加进旧 workflow/reference 文件；旧文件只能用短提示指向 `references/cn-*-formatting.md` 和 `references/data-query-order.md`。
- 任何需要查询外部数据的流程，必须先生成“数据源发现记录”，列出可用/不可用 MCP、connector、已授权源、用户文件、已调用或未调用原因、覆盖缺口和降级路径；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物。如果某个 skill 有更严格的数据源限制，以更严格规则为准。
- 任何涉及图表生成、图表嵌入或图表 QA 的流程，都必须遵守柱状图样式 Gate：柱状图、堆叠柱状图、分组柱状图默认关闭纵坐标横向网格线；DOCX、PPTX、PNG/JPG 和独立图表交付都要检查。
- 不修改技能目录名、schema key、环境变量名、MCP server 名称或既有 URL，除非同时说明迁移方案。
- 不默认启用付费源、机构源或本地 MCP；需要用户确认授权和可用性。
- 不使用 LiteLLM 或外部翻译 API 做本仓库中文化。
- 不引入旧多插件包装层、独立代理包、旧平台动作目录或托管代理模板。
- 改完必须运行结构检查、中文化门禁、中文产物样例检查和 Codex manifest 校验。

## License（许可证）

仓库根目录遵守 [`LICENSE`](./LICENSE)。部分 S&P Global/Kensho 技能保留原 Apache 2.0 许可文件，详见 [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)。
