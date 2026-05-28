---
name: ppt-template-creator
description: 根据用户提供的 PowerPoint 模板创建自包含 PPT 模板 SKILL（不是演示文稿）。仅当用户希望把自己的模板变成可复用 skill 时使用。若用户要创建实际演示文稿，请改用 pptx skill。
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
- 插件根目录 `../../CN_PPTX_OUTPUT_CONTRACT.md`（当输出 PPTX/PowerPoint 文件时）

本 skill 的输出必须按既有交付物承诺执行：
- 聊天摘要或即时分析不能替代本 skill 已承诺的文件主交付物。
- 纯文本/聊天输出必须包含来源、口径限制、待确认项和人工复核边界，不强制落盘为文件。
- 若用户要求或本 skill 明确承诺生成 Markdown 文件，最终回复前必须确认 `.md` 文件已生成、Markdown 文件路径存在、结构可读，并确保最终回复包含 Markdown 文件路径。
- 若本 skill 的既有输出包含 PPTX/PowerPoint 文件，最终回复前必须确认 PPTX 文件已生成、PPTX 文件路径存在、可打开或结构校验通过，并确保最终回复包含 PPTX 文件路径。


# PPT 模板 Skill 创建器

**此 skill 创建的是 SKILL，不是演示文稿。** 当用户希望把 PowerPoint 模板变成可复用 skill，并在之后生成演示文稿时使用。如果用户只是要创建一份演示文稿，请改用 `pptx` skill。

生成的 skill 包含：
- `assets/template.pptx` - 模板文件
- `SKILL.md` - 完整说明，无需引用本 meta skill

**通用 skill 构建最佳实践**请参考 `skill-creator` skill。本 skill 只聚焦 PPT 特定模式。

## 工作流

1. **用户提供模板**（.pptx 或 .potx）
2. **分析模板** - 提取版式、占位符和页面尺寸
3. **初始化 skill** - 使用 `skill-creator` skill 建立 skill 结构
4. **添加模板** - 将 .pptx 复制到 `assets/template.pptx`
5. **编写 SKILL.md** - 按下方模板写入 PPT 特定细节
6. **创建示例** - 生成样例演示文稿进行验证
7. **打包** - 使用 `skill-creator` skill 打包为 .skill 文件

## 步骤 2：分析模板

**关键：提取精确占位符位置**。这会决定内容区域边界。

```python
from pptx import Presentation

prs = Presentation(template_path)
print(f"Dimensions: {prs.slide_width/914400:.2f}\" x {prs.slide_height/914400:.2f}\"")
print(f"Layouts: {len(prs.slide_layouts)}")

for idx, layout in enumerate(prs.slide_layouts):
    print(f"\n[{idx}] {layout.name}:")
    for ph in layout.placeholders:
        try:
            ph_idx = ph.placeholder_format.idx
            ph_type = ph.placeholder_format.type
            # 重要：提取以英寸计的精确位置
            left = ph.left / 914400
            top = ph.top / 914400
            width = ph.width / 914400
            height = ph.height / 914400
            print(f"    idx={ph_idx}, type={ph_type}")
            print(f"        x={left:.2f}\", y={top:.2f}\", w={width:.2f}\", h={height:.2f}\"")
        except:
            pass
```

**需要记录的关键测量值：**
- **标题位置**：标题占位符在哪里？
- **副标题/描述**：副标题行在哪里？
- **页脚占位符**：页脚/来源出现在哪里？
- **内容区域**：副标题和页脚之间的空间就是内容区域。

### 找到真实内容起点

**关键：** 内容区域不一定紧跟副标题占位符之后开始。很多模板会在副标题和内容区域之间保留视觉边框、线条或空白。

**最佳做法：** 查看 Layout 2 或类似的“内容”版式，寻找 OBJECT 占位符。该占位符的 `y` 位置通常说明内容应从哪里真正开始。

```python
# 查找 OBJECT 占位符，确定真实内容起点
for idx, layout in enumerate(prs.slide_layouts):
    for ph in layout.placeholders:
        try:
            if ph.placeholder_format.type == 7:  # OBJECT type
                top = ph.top / 914400
                print(f"Layout [{idx}] {layout.name}: OBJECT starts at y={top:.2f}\"")
                # 这个 y 值就是内容应开始的位置
        except:
            pass
```

**示例：** 某模板可能是：
- 副标题结束于 y=1.38"
- 但 OBJECT 占位符从 y=1.90" 开始
- 中间空隙（0.52"）留给边框/线条，**不要把内容放在那里**

使用 OBJECT 占位符的 `y` 位置作为内容起点，而不是副标题结束位置。

## 步骤 5：编写 SKILL.md

生成的 skill 应采用以下结构：
```
[company]-ppt-template/
├── SKILL.md
└── assets/
    └── template.pptx
```

### 生成的 SKILL.md 模板

生成的 SKILL.md 必须是**自包含**的，所有说明都嵌入其中。使用此模板，并用分析结果填入括号值：

````markdown
---
name: [company]-ppt-template
description: 用于创建演示文稿的 [Company] PowerPoint 模板。创建 [Company] 品牌投行材料、董事会材料或客户演示时使用。
---

# [Company] PPT 模板

模板：`assets/template.pptx`（[WIDTH]" x [HEIGHT]"，[N] 个版式）

## 创建演示文稿

```python
from pptx import Presentation

prs = Presentation("path/to/skill/assets/template.pptx")

# 先删除所有已有幻灯片
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[0]

# 从版式添加幻灯片
slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_IDX])
```

## 关键版式

| Index | Name | 用途 |
|-------|------|------|
| [0] | [Layout Name] | [封面/标题页] |
| [N] | [Layout Name] | [带要点的内容页] |
| [N] | [Layout Name] | [双栏版式] |

## 占位符映射

**关键：为每个占位符写清精确位置（x、y 坐标）。**

### Layout [N]：[Name]
| idx | Type | Position | 用途 |
|-----|------|----------|------|
| [idx] | TITLE (1) | y=[Y]" | 幻灯片标题 |
| [idx] | BODY (2) | y=[Y]" | 副标题/描述 |
| [idx] | BODY (2) | y=[Y]" | 页脚 |
| [idx] | BODY (2) | y=[Y]" | 来源/备注 |

### 内容区域边界

**记录自定义形状/表格/图表的安全内容区域：**

```
内容区域（Layout [N]）：
- 左边距：[X]"（内容从这里开始）
- 顶部：[Y]"（位于副标题占位符下方）
- 宽度：[W]"
- 高度：[H]"（在页脚前结束）

四象限版式：
- 左列：x=[X]"，宽度=[W]"
- 右列：x=[X]"，宽度=[W]"
- 上行：y=[Y]"，高度=[H]"
- 下行：y=[Y]"，高度=[H]"
```

**为什么重要：** 自定义内容（文本框、表格、图表）必须留在这些边界内，避免与标题、页脚、来源行等模板占位符重叠。

## 填充内容

**不要手工添加项目符号字符**。幻灯片母版会处理格式。

```python
# 填充标题
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        if shape.placeholder_format.type == 1:  # TITLE
            shape.text = "幻灯片标题"

# 按层级填充内容（level 0 = 小标题，level 1 = 要点）
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == [CONTENT_IDX]:
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()

            content = [
                ("章节小标题", 0),
                ("第一条要点", 1),
                ("第二条要点", 1),
            ]

            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```

## 示例：封面页

```python
slide = prs.slides.add_slide(prs.slide_layouts[[COVER_IDX]])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == [TITLE_IDX]:
            shape.text = "公司名称"
        elif idx == [SUBTITLE_IDX]:
            shape.text = "演示标题 | 日期"
```

## 示例：内容页

```python
slide = prs.slides.add_slide(prs.slide_layouts[[CONTENT_IDX]])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        ph_type = shape.placeholder_format.type
        idx = shape.placeholder_format.idx
        if ph_type == 1:
            shape.text = "执行摘要"
        elif idx == [BODY_IDX]:
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()
            content = [
                ("关键发现", 0),
                ("收入同比增长 40% 至 $50M", 1),
                ("拓展至 3 个新市场", 1),
                ("建议", 0),
                ("推进该战略举措", 1),
            ]
            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```
````

## 步骤 6：创建示例输出

生成一份样例演示文稿，验证 skill 可用。将其与 skill 放在一起，便于参考。

## 生成 Skills 的 PPT 专属规则

1. **模板放入 assets/** - 始终打包 .pptx 文件
2. **SKILL.md 自包含** - 所有说明都嵌入文档，不依赖外部引用
3. **不要手工添加项目符号** - 使用 `paragraph.level` 表示层级
4. **先删除幻灯片** - 添加新幻灯片前始终清空现有幻灯片
5. **按 idx 记录占位符** - placeholder idx 值与模板绑定
