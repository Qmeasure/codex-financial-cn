# Financial Services CN 仓库规则

本仓库是单一 Codex 插件的中文版金融服务技能集合。仓库根目录本身就是插件源；所有 skill、README、脚本注释和用户可见输出必须使用中文金融语境。

## 数据规则

- 默认 A 股优先，港股和美股兼容。
- 所有工作流必须遵守 `DATA_SOURCES_CN.md`。
- 付费源只能作为用户确认后的增强源，不得默认启用。
- 非权益工作流涉及监管、会计、KYC、基金文件和月结判断时，必须引用官方材料、用户政策或用户文件；没有依据时写“需确认”。

## 中文产物规则

- 所有 DOCX、PPTX、XLSX、Markdown、表格、图表、脚注和最终摘要必须遵守 `CN_OUTPUT_FORMATTING.md`。
- 中文正文、表格、图表、脚注和来源说明不得沿用英文默认字体或英文版式。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。

## Codex 插件规则

- 根目录固定包含 `.codex-plugin/plugin.json`、`.mcp.json` 和 `skills/`。
- `plugin.json` 的 `name` 固定为 `financial-services-cn`，`skills` 固定指向 `./skills/`，`mcpServers` 固定指向 `./.mcp.json`。
- `skills/` 采用全扁平结构，每个 skill 目录必须包含 `SKILL.md`。
- 不允许重新引入旧多插件包装层、旧平台命令入口、代理包、托管代理模板或其他旧架构入口。
- `plugin.json` 只能声明真实存在的能力；没有 `.app.json` 时不得声明 `apps`。
- 默认 MCP 配置必须使用 Codex 兼容的 `.mcp.json` 形态；不得硬编码 token。
- A 股/港股相关 MCP 配置可以保留为默认入口，但无法确认本地服务、依赖或授权时，技能必须写“需确认”。

## 修改规则

- source skills 直接位于根级 `skills/`。
- 不修改技能目录名、schema key、环境变量或既有 URL。
- 不使用 LiteLLM 或外部翻译 API 做本仓库中文化。
- 改完必须运行结构检查、中文化门禁、中文产物样例检查和 Codex manifest 校验。
