---
name: skill-creator
description: 创建有效 skill 的指南。当用户希望创建新 skill（或更新现有 skill），以专业知识、工作流或工具集成扩展 Codex 能力时使用。
license: 完整条款见 LICENSE.txt
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
- 插件根目录 `../../DATA_QUERY_ORDER_CN.md`（当任务需要外部数据查询、行情更新、财报抓取、行业/公司/宏观/监管材料检索时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、数据缺口和人工审阅边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 需要查询或刷新外部数据时，必须先读取 `../../DATA_QUERY_ORDER_CN.md`，先生成“数据源发现记录”，列出可用/不可用 MCP、connector、授权源和用户文件；Gate 通过前不得网页搜索、官网抓取、SEC/交易所抓取或生成正式交付物。若本 skill 有更严格数据源限制，以更严格规则为准。
- 正式 Markdown、聊天摘要和最终交付说明必须遵守插件根目录 `../../CN_MARKDOWN_OUTPUT_CONTRACT.md`，并包含来源、口径限制、数据缺口和人工审阅边界。


# Skill Creator（技能创建器）

本 skill 提供创建有效 skill 的指南。

## 关于 Skills

Skills 是模块化、自包含的包，通过提供专业知识、工作流和工具来扩展 Codex 的能力。可以把它们理解为特定领域或任务的“入门指南”：它们把 Codex 从通用 agent 转化为具备过程性知识的专业 agent，而这些过程性知识不是任何模型都能完全内置的。

### Skills 提供什么

1. 专业工作流 - 面向特定领域的多步骤流程
2. 工具集成 - 使用特定文件格式或 API 的说明
3. 领域专业知识 - 公司特定知识、schema、业务逻辑
4. 打包资源 - 面向复杂和重复任务的脚本、参考文件和资产

## 核心原则

### 简洁是关键

上下文窗口是公共资源。Skills 会与 Codex 需要的其他全部内容共享上下文窗口：system prompt、对话历史、其他 Skills 的元数据，以及用户的实际请求。

**默认假设：Codex 已经很聪明。** 只添加 Codex 尚不具备的上下文。逐条挑战每段信息：“Codex 真的需要这个解释吗？”以及“这段话是否值得消耗这些 token？”

优先使用简洁示例，而不是冗长解释。

### 设置合适的自由度

将具体程度与任务的脆弱性和可变性匹配：

**高自由度（文字说明）**：当多种方法都有效、决策依赖上下文，或需要启发式判断时使用。

**中自由度（伪代码或带参数脚本）**：当存在偏好模式、允许一定变化，或配置会影响行为时使用。

**低自由度（具体脚本、少量参数）**：当操作脆弱、容易出错、一致性关键，或必须遵循特定顺序时使用。

可以把 Codex 想象成在探索路径：有悬崖的窄桥需要明确护栏（低自由度），开阔草地则允许多条路线（高自由度）。

### Skill 的构成

每个 skill 都包含必需的 `SKILL.md` 文件，以及可选的打包资源：

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name:（必需）
│   │   └── description:（必需）
│   └── Markdown 说明（必需）
└── 打包资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 按需加载进上下文的文档
    └── assets/           - 输出中使用的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

每个 `SKILL.md` 包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。Codex 只读取这些字段来判断何时使用 skill，因此必须清楚、全面地描述 skill 是什么，以及何时应该使用。
- **正文**（Markdown）：使用该 skill 的说明和指导。只有在 skill 触发后才会加载（如果触发）。

#### 打包资源（可选）

##### Scripts（`scripts/`）

面向需要确定性可靠性或会被反复重写任务的可执行代码（Python/Bash 等）。

- **何时包含**：当同一段代码被反复重写，或需要确定性可靠性时
- **示例**：用于 PDF 旋转任务的 `scripts/rotate_pdf.py`
- **收益**：节省 token、结果确定，可以不读入上下文直接执行
- **注意**：Codex 仍可能需要读取脚本，以便 patch 或做环境特定调整

##### 参考资料（`references/`）

按需加载进上下文的文档和参考材料，用于指导 Codex 的流程与思考。

- **何时包含**：当 Codex 工作时应参考某些文档
- **示例**：财务 schema 的 `references/finance.md`、公司 NDA 模板的 `references/mnda.md`、公司政策的 `references/policies.md`、API 规格的 `references/api_docs.md`
- **使用场景**：数据库 schema、API 文档、领域知识、公司政策、详细工作流指南
- **收益**：保持 `SKILL.md` 精简，仅在 Codex 判断需要时加载
- **最佳实践**：如果文件很大（>10k 词），在 `SKILL.md` 中加入 grep 搜索模式
- **避免重复**：信息应该只存在于 `SKILL.md` 或 references 文件之一，不要两处重复。详细信息优先放进 references，除非它确实是 skill 的核心；这样能保持 `SKILL.md` 精简，同时让信息可发现，不占满上下文窗口。`SKILL.md` 中只保留必要的过程说明和工作流指导；详细参考材料、schema 和示例放入 references。

##### Assets（`assets/`）

不会读入上下文、但会在 Codex 产出的最终结果中使用的文件。

- **何时包含**：当 skill 需要最终输出会用到的文件时
- **示例**：品牌资产 `assets/logo.png`、PowerPoint 模板 `assets/slides.pptx`、HTML/React 样板 `assets/frontend-template/`、字体 `assets/font.ttf`
- **使用场景**：模板、图片、图标、样板代码、字体、会被复制或修改的样例文档
- **收益**：将输出资源与文档分离，让 Codex 可以使用文件而不把它们加载进上下文

#### Skill 中不应包含什么

skill 应只包含直接支持其功能的必要文件。不要创建多余文档或辅助文件，包括：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等等

skill 应只包含 AI agent 完成当前任务所需的信息。不应包含创建过程背景、安装和测试流程、面向用户的文档等辅助上下文。额外文档只会增加杂乱和困惑。

### 渐进披露设计原则

Skills 使用三级加载系统来高效管理上下文：

1. **元数据（name + description）** - 始终在上下文中（约 100 词）
2. **`SKILL.md` 正文** - skill 触发时加载（<5k 词）
3. **打包资源** - Codex 按需使用（不受限，因为脚本可执行而无需读入上下文窗口）

#### 渐进披露模式

将 `SKILL.md` 正文保持在必要范围内，并控制在 500 行以内，以减少上下文膨胀。接近限制时，将内容拆分为单独文件。拆分到其他文件时，必须从 `SKILL.md` 引用这些文件，并清楚说明何时读取，确保 skill 使用者知道它们存在以及何时使用。

**关键原则：** 当一个 skill 支持多种变体、框架或选项时，在 `SKILL.md` 中只保留核心工作流和选择指导。将变体特定细节（模式、示例、配置）放入单独参考文件。

**模式 1：带参考文件的高层指南**

```markdown
# PDF 处理

## 快速开始

用 pdfplumber 提取文本：
[code example]

## 高级功能

- **表单填写**：完整指南见 [FORMS.md](FORMS.md)
- **API 参考**：全部方法见 [REFERENCE.md](REFERENCE.md)
- **示例**：常见模式见 [EXAMPLES.md](EXAMPLES.md)
```

Codex 只在需要时加载 `FORMS.md`、`REFERENCE.md` 或 `EXAMPLES.md`。

**模式 2：按领域组织**

对包含多个领域的 Skills，按领域组织内容，避免加载无关上下文：

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

当用户询问销售指标时，Codex 只读取 `sales.md`。

类似地，对于支持多个框架或变体的 skills，按变体组织：

```
cloud-deploy/
├── SKILL.md（工作流 + 提供方选择）
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

当用户选择 AWS 时，Codex 只读取 `aws.md`。

**模式 3：条件细节**

先展示基础内容，再链接到高级内容：

```markdown
# DOCX 处理

## 创建文档

新建文档时使用 docx-js。详见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

简单编辑可以直接修改 XML。

**修订模式**：见 [REDLINING.md](REDLINING.md)
**OOXML 细节**：见 [OOXML.md](OOXML.md)
```

只有当用户需要这些功能时，Codex 才读取 `REDLINING.md` 或 `OOXML.md`。

**重要指南：**

- **避免深层嵌套引用** - references 距离 `SKILL.md` 保持一层。所有参考文件都应直接从 `SKILL.md` 链接。
- **组织较长参考文件** - 对超过 100 行的文件，在顶部加入目录，便于 Codex 预览时了解完整范围。

## Skill 创建流程

创建 skill 包含以下步骤：

1. 用具体示例理解 skill
2. 规划可复用 skill 内容（scripts、references、assets）
3. 初始化 skill（运行 `init_skill.py`）
4. 编辑 skill（实现资源并编写 `SKILL.md`）
5. 打包 skill（运行 `package_skill.py`）
6. 基于真实使用迭代

按顺序执行这些步骤；只有在有明确理由不适用时才跳过。

### 步骤 1：用具体示例理解 Skill

只有当 skill 的使用模式已经非常清楚时才跳过这一步。即使处理现有 skill，这一步仍然有价值。

要创建有效 skill，必须清楚理解该 skill 将如何被使用。这个理解可来自用户提供的直接示例，也可来自生成后再经用户反馈验证的示例。

例如，构建 `image-editor` skill 时，相关问题包括：

- “`image-editor` skill 应支持哪些功能？编辑、旋转，还是其他？”
- “能否给一些这个 skill 会如何使用的示例？”
- “我能想象用户会说 ‘Remove the red-eye from this image’ 或 ‘Rotate this image’。你还设想过其他用法吗？”
- “用户说什么时应该触发这个 skill？”

为避免压迫用户，不要在一条消息里问太多问题。先问最重要的问题，并按需要追问，以提升效果。

当你清楚知道该 skill 应支持什么功能时，结束这一步。

### 步骤 2：规划可复用 Skill 内容

将具体示例转化为有效 skill 时，对每个示例进行分析：

1. 思考如果从零执行该示例，应如何完成
2. 识别重复执行这些工作流时哪些 scripts、references 和 assets 会有帮助

示例：构建 `pdf-editor` skill，处理“帮我旋转这个 PDF”之类请求，分析结果是：

1. 旋转 PDF 每次都需要重写相同代码
2. 在 skill 中保存 `scripts/rotate_pdf.py` 脚本会很有帮助

示例：设计 `frontend-webapp-builder` skill，处理“帮我做一个 todo app”或“帮我做一个记录步数的 dashboard”之类请求，分析结果是：

1. 编写前端 webapp 每次都需要相同 HTML/React 样板
2. 将包含 HTML/React 项目样板文件的 `assets/hello-world/` 模板放入 skill 会很有帮助

示例：构建 `big-query` skill，处理“今天有多少用户登录？”之类请求，分析结果是：

1. 查询 BigQuery 每次都需要重新发现表 schema 和关系
2. 在 skill 中保存记录表 schema 的 `references/schema.md` 文件会很有帮助

为确定 skill 内容，分析每个具体示例，并列出需要包含的可复用资源：scripts、references 和 assets。

### 步骤 3：初始化 Skill

到这一步，就该真正创建 skill。

只有在待开发 skill 已经存在、只需要迭代或打包时，才跳过这一步。这种情况下继续下一步。

从零创建新 skill 时，始终运行 `init_skill.py` 脚本。该脚本会方便地生成新的 skill 模板目录，并自动包含 skill 所需的一切，使创建流程更高效、更可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

该脚本会：

- 在指定路径创建 skill 目录
- 生成带有正确 frontmatter 和 TODO 占位符的 `SKILL.md` 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 `SKILL.md` 和示例文件。

### 步骤 4：编辑 Skill

编辑（新生成或既有）skill 时，记住这个 skill 是给另一个 Codex 实例使用的。包含对 Codex 有帮助且非显而易见的信息。思考哪些过程性知识、领域细节或可复用资产能帮助另一个 Codex 实例更有效完成这些任务。

#### 学习经过验证的设计模式

根据 skill 需要，参考以下有用指南：

- **多步骤流程**：见 `references/workflows.md`，用于顺序工作流和条件逻辑
- **特定输出格式或质量标准**：见 `references/output-patterns.md`，用于模板和示例模式

这些文件包含有效 skill 设计的成熟最佳实践。

#### 从可复用 Skill 内容开始

开始实现时，先处理上面识别出的可复用资源：`scripts/`、`references/` 和 `assets/` 文件。注意，这一步可能需要用户输入。例如，实现 `brand-guidelines` skill 时，用户可能需要提供品牌资产或模板以存入 `assets/`，或提供文档以存入 `references/`。

新增脚本必须实际运行测试，确保无 bug 且输出符合预期。如果有许多类似脚本，只需测试代表性样本，以在完成时间和信心之间取得平衡。

skill 不需要的示例文件和目录应删除。初始化脚本会在 `scripts/`、`references/` 和 `assets/` 中创建示例文件用于展示结构，但多数 skills 并不需要全部示例。

#### 更新 SKILL.md

**写作指南：** 始终使用祈使/不定式表达。

##### Frontmatter

编写包含 `name` 和 `description` 的 YAML frontmatter：

- `name`：skill 名称
- `description`：skill 的主要触发机制，帮助 Codex 理解何时使用该 skill。
  - 同时包含 skill 做什么，以及在哪些具体触发/上下文中使用。
  - 将所有“何时使用”信息写在这里，而不是正文中。正文只有在触发后才加载，因此正文中的“何时使用此 Skill”章节对 Codex 选择 skill 没有帮助。
  - `docx` skill 的示例 description：“全面的文档创建、编辑和分析能力，支持修订、批注、格式保留和文本提取。当 Codex 需要处理专业文档（.docx 文件）时使用，包括：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理修订，(4) 添加批注，或任何其他文档任务。”

不要在 YAML frontmatter 中包含任何其他字段。

##### Body

编写使用该 skill 及其打包资源的说明。

### 步骤 5：打包 Skill

skill 开发完成后，必须打包为可分发的 `.skill` 文件并交给用户。打包流程会先自动验证 skill，确保它满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

可选输出目录：

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本会：

1. **自动验证** skill，检查：

   - YAML frontmatter 格式和必需字段
   - Skill 命名规范和目录结构
   - Description 完整性和质量
   - 文件组织和资源引用

2. **验证通过后打包** skill，创建以 skill 命名的 `.skill` 文件（例如 `my-skill.skill`），包含全部文件并保持正确目录结构，便于分发。`.skill` 文件本质上是扩展名为 `.skill` 的 zip 文件。

如果验证失败，脚本会报告错误并退出，不会创建包。修复所有验证错误后，再次运行打包命令。

### 步骤 6：迭代

测试 skill 后，用户可能会要求改进。这通常发生在刚刚使用 skill 后，此时对 skill 表现有新鲜上下文。

**迭代工作流：**

1. 在真实任务中使用 skill
2. 发现卡点或低效之处
3. 识别 `SKILL.md` 或打包资源应如何更新
4. 实施变更并再次测试
