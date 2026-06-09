# Financial Services CN Agent 规约

本仓库是中文金融服务技能集合，根目录就是 `financial-services-cn` 插件源。它不是多插件包装层，也不是旧平台入口集合。任何 Agent 在这里工作时，都必须围绕“中文金融产物、A 股优先、来源可追溯、结构可校验、最小改动”执行。

## 1. 仓库身份

- 插件名称固定为 `financial-services-cn`。
- 根级结构固定包含 `.codex-plugin/plugin.json`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`OPTIONAL_MCP_SERVERS.json`、`skills/`、`README.md`、`DATA_SOURCES_CN.md`、`DATA_QUERY_ORDER_CN.md` 和 `CN_OUTPUT_FORMATTING.md`；根目录不得放置 `.mcp.json`，避免 Codex 或 Claude Code 自动加载可选数据源。
- `skills/` 是唯一的 source skills 目录，采用全扁平结构；每个技能目录必须包含 `SKILL.md`。
- 仓库内不得重新引入旧多插件包装层、旧平台入口、代理包、托管代理模板或其他旧架构残留；`.claude-plugin/` 只用于 Claude Code 插件 manifest 和 marketplace catalog。
- `.codex-plugin/plugin.json` 只能声明真实存在的能力；没有 `.app.json` 时不得声明 `apps`。

## 2. 默认金融语境

- 未指定市场时，默认按中国大陆机构金融工作流和 A 股语境处理。
- 港股、美股、ADR、H 股、红筹、双重主要上市和跨市场比较必须显式标注交易所、币种、会计准则、数据日期、汇率来源和口径差异。
- A 股默认人民币，单位优先“万元/亿元”；港股默认港元；美股默认美元。除非用户明确要求，不默认强制折算成人民币。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI、API 等专业缩写和代码标识，但面向用户的解释必须使用中文金融语境。

## 3. 数据来源规则

- 所有技能、README、脚本注释、样例和用户可见输出必须遵守 `DATA_SOURCES_CN.md` 和 `DATA_QUERY_ORDER_CN.md`。
- 来源优先级为：用户文件或政策、官方披露、已授权 MCP 或机构数据库、用户确认可用的中国市场工具、免费公开网页辅助线索。
- 付费源、机构源和本地 MCP 只能作为用户确认后的增强源，不得默认启用，不得假设本机已安装、已登录或已有授权。
- 监管、会计、KYC、AML、税务、基金文件、LP 报告、月结、总账入账、签批和客户适当性判断，必须引用官方材料、用户政策或用户文件；缺少依据时不得作出正式判断。
- 免费网页和搜索结果不得作为估值、KYC、会计、监管、基金运营或月结判断的唯一依据。
- 不得在代码、文档、日志或最终摘要中输出任何 token、key、账号密钥或客户敏感信息。

## 4. 中文产物规则

- 所有 DOCX、PPTX、XLSX、Markdown、表格、图表、脚注、文件名建议和最终摘要必须遵守 `CN_OUTPUT_FORMATTING.md`。
- 中文正文、标题、表头、图例、脚注、来源说明和免责声明不得沿用英文默认标题或英文版式。
- 用户模板、公司品牌规范和既有版式优先，但不能省略中文可读性、来源脚注、币种、单位、日期、口径和数据缺口。
- 财务模型必须区分输入区、计算区、来源/假设区和检查区；派生值不得硬编码。
- PPT 每页只表达一个核心结论；图表必须标注数据日期、来源和估算/预测/未经审计等限制。
- 最终摘要必须说明产物内容、数据来源、口径限制、数据缺口和免责声明，不得只返回英文路径或英文状态。
- 本仓库中文化不得使用 LiteLLM 或外部翻译 API。

## 5. Formatting 一致性铁律

- Formatting 规则是全链路合同，不是某个 skill 的局部提示。根级合同、README 说明、校验脚本、样例产物和安装 cache 必须保持一致。
- 修改 DOCX、XLSX、PPTX、Markdown、HTML、图表或 ZIP 的任何格式规则前，必须先用 `rg` 扫描相关旧口径、禁词、根级合同、业务 reference、README、脚本和样例，确认真实影响范围。
- 只要某条格式规则属于通用产物类型，就必须同步更新根级对应合同和门禁脚本；不得只修改 `earnings-analysis`、单个 skill、单个根合同或单个样例。
- 只有当规则确实只适用于某一个 skill 时，才允许局部修改；最终说明必须写清楚为什么不需要同步到其他 formatting 文件。
- 看到 DOCX、PPTX、XLSX、HTML、Markdown 或图表输出问题时，先追根因到 skill 指令、业务 reference、根级合同、样例产物和门禁脚本；不要只修生成出的某个报告或只改一个示例。
- 新增或调整 formatting 内容时，不把大段格式正文追加进旧 workflow/reference 文件；业务 reference 只保留短引用，格式正文只放在根级 `CN_*_OUTPUT_CONTRACT.md`。
- 每次 formatting 修改都必须同步考虑 `scripts/check_cn_localization.py` 和 `scripts/check_cn_artifact_samples.py`，让门禁能防止旧口径回退。
- 修改完成后，必须重新安装插件并复扫 Codex plugin cache，确认安装快照里的根合同、业务 reference 和门禁规则与源仓库一致。

## 6. 共享合同与交付标准

- 共享合同只能放在根目录，包括 `DATA_SOURCES_CN.md`、`DATA_QUERY_ORDER_CN.md`、`CN_OUTPUT_FORMATTING.md` 和所有 `CN_*_OUTPUT_CONTRACT.md`；不得在 `skills/*/references/` 或 `skills/*/reference/` 下重复放置 `data-query-order.md` 或 `cn-*formatting.md`。
- `skills/*/references/`、`skills/*/reference/` 和 `skills/*/assets/` 只能承载某个 skill 独有的业务 workflow、schema、样例、计算口径或专用限制；共享数据查询顺序和格式正文必须通过短引用指向根级合同。
- 每个 `SKILL.md` 必须引用插件根目录 `../../DATA_SOURCES_CN.md`、`../../DATA_QUERY_ORDER_CN.md`、`../../CN_OUTPUT_FORMATTING.md` 和 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`；承诺 DOCX、XLSX、PPTX、HTML 或独立图表/ZIP 时，必须额外引用对应根级产物合同。
- 业务 reference 或 asset 引用根级合同时，必须使用相对自身位置可解析的路径，例如 `../../../DATA_QUERY_ORDER_CN.md`；不得从 `SKILL.md` 的层级复制错误路径。
- 正式交付物不能用聊天摘要替代。凡 skill 承诺生成 DOCX、XLSX、PPTX、HTML、Markdown 文件、图表图片或 ZIP，最终交付前必须确认文件已生成、路径存在、格式合同已读取、数据源发现记录已完成或说明不适用。
- 修改共享合同、skill 引用或交付标准后，必须同步更新 README、校验脚本和安装 cache；完成验收必须证明源仓库和安装快照中所有根级合同引用都能解析，且不存在重复本地合同。
- 最终说明必须列出运行过的校验命令、结果、无法通过的具体阻塞原因和剩余风险；不得把“运行无报错”等同于“交付标准正确”。

## 7. 插件与 MCP 边界

- `.codex-plugin/plugin.json` 的 `name` 必须固定为 `financial-services-cn`。
- `plugin.json` 的 `skills` 必须固定指向 `./skills/`。
- `plugin.json` 默认不得声明 `mcpServers`；否则 Codex 安装后会主动初始化所有 MCP，导致未登录、未授权或本地服务未启动时弹出启动告警。
- `.claude-plugin/plugin.json` 的 `name` 必须固定为 `financial-services-cn`，`skills` 必须固定指向 `./skills/`，不得声明 MCP、hooks、agents 或 commands。
- `.claude-plugin/marketplace.json` 的 `name` 必须固定为 `financial-services-cn`，且其中 `financial-services-cn` 插件的 `source` 必须固定为 `./`，表示 Claude Code 从同一仓库根目录安装本插件。
- Codex manifest、Claude Code manifest 和 Claude Code marketplace 的 `name`、`version`、`repository`、`homepage`、`license` 和 `skills` 口径必须保持一致；修改版本或仓库元数据时必须同步三处。
- `OPTIONAL_MCP_SERVERS.json` 必须保持 Codex MCP 配置形态，不得硬编码 token；它是可选模板清单，不要求保留所有潜在 MCP，也不代表安装插件时会启用或安装 MCP。
- A 股、港股或机构数据相关 MCP 配置只能作为可选模板保留；无法确认本地服务、依赖、账号或授权时，技能只能记录为未覆盖数据项。
- 不修改已有技能目录名、schema key、环境变量名、MCP server 名称或既有 URL，除非用户明确要求并说明迁移方案。

## 8. 修改工作流

- 先侦察现有结构，再修改文件。不要凭记忆判断插件结构、技能数量、校验脚本或数据规则。
- 修改前先确认影响范围：根文档、manifest、MCP、某个 skill、脚本、样例产物或跨文件规则。
- 优先最小改动。不要顺手重构无关技能、移动目录、改命名、改格式或批量替换无关文本。
- 如果用户给出明确模板、接口、参数、命令或既有 adapter，必须 1:1 沿用，不自创替代实现。
- 新增或改写技能时，必须包含“中文版执行契约”，并引用 `DATA_SOURCES_CN.md`、`DATA_QUERY_ORDER_CN.md` 和 `CN_OUTPUT_FORMATTING.md`。
- 修改根级规则时，同步检查 `README.md`、`DATA_SOURCES_CN.md`、`DATA_QUERY_ORDER_CN.md`、`CN_OUTPUT_FORMATTING.md`、`.codex-plugin/plugin.json` 和相关脚本是否产生矛盾。
- 修改插件安装或元数据规则时，同步检查 `.codex-plugin/plugin.json`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`README.md` 和相关脚本是否产生矛盾。
- 修改 formatting 规则时，同步检查对应根级合同、README、样例产物、门禁脚本和安装 cache；不得留下源仓库与安装快照不一致。
- 修改服务代码时必须自动重启受影响服务；本仓库通常是插件和技能集合，若没有运行服务，不要虚构重启步骤。

## 9. 禁止事项

- 不把英文金融技能直接照搬为中文文件名或英文交付模板。
- 不默认启用付费源、机构源或本地 MCP。
- 不输出投资、法律、税务、会计、监管、交易、签批、入账或客户准入建议；只能辅助起草并要求专业人员审阅。
- 不删除兼容路径、不破坏 manifest、不改变技能目录结构、不引入旧架构残留。
- 不用前端式或营销式文案包装金融结论；材料必须克制、可审计、能追溯。
- 不把“运行无报错”当作“设计正确”；完成前必须有校验证据。
- 不在 skill 目录下新增重复共享合同；`data-query-order.md`、`cn-docx-formatting.md`、`cn-xlsx-formatting.md`、`cn-pptx-formatting.md`、`cn-markdown-formatting.md`、`cn-html-formatting.md` 和 `cn-chart-formatting.md` 一律禁止回流。

## 10. 完成前校验

改完必须至少运行以下校验：

```bash
python3 scripts/check.py
python3 scripts/check_cn_localization.py
python3 scripts/check_cn_artifact_samples.py
python3 /Users/lesterbot/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
claude plugin validate .
```

如果某个校验因本机依赖、外部服务或授权缺失无法执行，必须在最终说明中写清楚具体命令、失败原因和剩余风险。

## 11. 一句话原则

本仓库的每一次修改，都必须让 `financial-services-cn` 更稳定地作为中文金融服务 Codex 插件运行：A 股优先、来源清楚、格式中文、边界可信、结构可校验。
