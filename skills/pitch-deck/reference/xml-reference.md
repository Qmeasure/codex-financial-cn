# PowerPoint XML 参考

本文件包含用于程序化编辑 PowerPoint 的 XML 模式。直接处理 OOXML 格式时使用这些模式。

**注：** 示例中的颜色值（例如 `E67E22`、`D35400`）只是占位符。请替换为模板的品牌色。

---

## 何时使用本参考

**以下场景使用 `python-pptx`：**
- 创建新表格（自动处理单元格结构和关系）
- 添加文本框
- 插入图片
- 创建大多数形状
- 任何 `python-pptx` 已提供 API 的操作

**仅在以下场景直接编辑 XML：**
- 修改 `python-pptx` 未暴露的既有元素属性
- 通过 `python-pptx` 创建表格后微调单元格格式
- 调整 `python-pptx` API 不支持的特定形状属性

**以下场景绝不要直接编辑 XML：**
- 从零创建表格（关系管理容易出错，可能损坏文件）
- 初始创建形状（存在形状 ID 冲突风险）
- 任何可以通过 `python-pptx` 完成的操作

本文件中的 XML 模式仅用于**参考和定向修改**，不是用于批量构造完整元素。

---

## XML 编辑风险

如果处理不谨慎，直接编辑 XML 可能损坏 PowerPoint 文件：
- PowerPoint XML 存在相互依赖（关系文件、内容类型）
- 无效 XML 或缺失关系可能损坏整个文件
- 每页幻灯片内的形状 ID 必须唯一

**始终在备份副本上操作**，不要直接编辑原始文件。

---

## 目录
- [表格实现](#表格实现)
- [箭头形状](#箭头形状)
- [文本框](#文本框)
- [带填充的形状](#带填充的形状)
- [图片插入](#图片插入)
- [连接线](#连接线)
- [单位换算](#单位换算)

---

## 表格实现

### 关键：确认表格是真正的表格对象

创建任何表格后，都必须确认它是真正的表格对象，而不是用分隔符拼出来的文本。

**程序化验证（python-pptx）：**
```python
for shape in slide.shapes:
    if shape.has_table:
        print(f"✓ Found table: {len(shape.table.rows)} rows, {len(shape.table.columns)} columns")
```

**视觉验证（导出图片）：**
- 无论内容长度如何变化，各列都完美对齐
- 单元格边框一致
- 选中表格时会整体选中所有单元格

**失败迹象：说明你创建的是文本，不是表格：**
- 数值之间可见 `|` 字符
- 内容长度变化时列无法对齐
- 使用制表符（`\t`）控制间距
- 多个文本框排列得像表格

基于文本的“表格”无法被接收方正常编辑；字体变化时会错位，也会显得不专业。投行材料中不允许使用管道符或制表符分隔的伪表格。

---

### 基础表格结构

```xml
<a:tbl>
  <a:tblPr firstRow="1" bandRow="1">
    <a:tableStyleId>{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}</a:tableStyleId>
  </a:tblPr>
  <a:tblGrid>
    <a:gridCol w="2000000"/>  <!-- 来源列 - 宽度单位为 EMU -->
    <a:gridCol w="1200000"/>  <!-- 2024 规模列 -->
    <a:gridCol w="1200000"/>  <!-- CAGR 列 -->
    <a:gridCol w="1200000"/>  <!-- 2030 预测列 -->
  </a:tblGrid>
  <!-- 后续为行定义 -->
</a:tbl>
```

### 包含单元格的表格行

```xml
<a:tr h="370840">  <!-- 行高，单位为 EMU -->
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="l"/>  <!-- 文本列左对齐 -->
        <a:r>
          <a:rPr lang="zh-CN" sz="1000" b="0"/>
          <a:t>Grand View Research</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr/>
  </a:tc>
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="ctr"/>  <!-- 数值列居中 -->
        <a:r>
          <a:rPr lang="zh-CN" sz="1000"/>
          <a:t>22.1</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr/>
  </a:tc>
  <!-- 其他单元格... -->
</a:tr>
```

### 表头行样式

```xml
<a:tr h="370840">
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="l"/>
        <a:r>
          <a:rPr lang="zh-CN" sz="1000" b="1">  <!-- 表头加粗 -->
            <a:solidFill>
              <a:srgbClr val="FFFFFF"/>  <!-- 白色文字 -->
            </a:solidFill>
          </a:rPr>
          <a:t>来源</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr>
      <a:solidFill>
        <a:srgbClr val="E67E22"/>  <!-- 橙色背景 -->
      </a:solidFill>
    </a:tcPr>
  </a:tc>
  <!-- 其他表头单元格... -->
</a:tr>
```

---

## 箭头形状

### 右箭头

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="10" name="Arrow Right"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="3000000" y="2500000"/>  <!-- 位置，单位为 EMU -->
      <a:ext cx="500000" cy="300000"/>   <!-- 尺寸，单位为 EMU -->
    </a:xfrm>
    <a:prstGeom prst="rightArrow">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>  <!-- 箭头填充色 -->
    </a:solidFill>
    <a:ln>
      <a:noFill/>  <!-- 无轮廓 -->
    </a:ln>
  </p:spPr>
</p:sp>
```

### 下箭头

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="11" name="Arrow Down"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="2500000" y="3000000"/>
      <a:ext cx="300000" cy="500000"/>
    </a:xfrm>
    <a:prstGeom prst="downArrow">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
  </p:spPr>
</p:sp>
```

### Chevron 形状

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="12" name="Chevron"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="3000000" y="2500000"/>
      <a:ext cx="400000" cy="600000"/>
    </a:xfrm>
    <a:prstGeom prst="chevron">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
  </p:spPr>
</p:sp>
```

---

## 文本框

### 基础文本框

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="5" name="TextBox 4"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="1500000"/>
      <a:ext cx="4000000" cy="500000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:noFill/>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" rtlCol="0">
      <a:spAutoFit/>
    </a:bodyPr>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:rPr lang="zh-CN" sz="1400" dirty="0"/>
        <a:t>在此填写文本内容</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### 带项目符号的文本框

```xml
<p:txBody>
  <a:bodyPr wrap="square">
    <a:spAutoFit/>
  </a:bodyPr>
  <a:lstStyle/>
  <a:p>
    <a:pPr marL="342900" indent="-342900">
      <a:buFont typeface="Wingdings" panose="05000000000000000000" pitchFamily="2" charset="2"/>
      <a:buChar char="&#252;"/>  <!-- 勾选符号 -->
    </a:pPr>
    <a:r>
      <a:rPr lang="zh-CN" sz="1400" dirty="0"/>
      <a:t>第一个要点</a:t>
    </a:r>
  </a:p>
  <a:p>
    <a:pPr marL="342900" indent="-342900">
      <a:buFont typeface="Wingdings" panose="05000000000000000000" pitchFamily="2" charset="2"/>
      <a:buChar char="&#252;"/>
    </a:pPr>
    <a:r>
      <a:rPr lang="zh-CN" sz="1400" dirty="0"/>
      <a:t>第二个要点</a:t>
    </a:r>
  </a:p>
</p:txBody>
```

### 白色文本（用于深色背景）

```xml
<a:r>
  <a:rPr lang="zh-CN" sz="1000" b="1" i="1" dirty="0">
    <a:solidFill>
      <a:srgbClr val="FFFFFF"/>  <!-- 白色文本 -->
    </a:solidFill>
  </a:rPr>
  <a:t>深色背景上的白色文字</a:t>
</a:r>
```

---

## 带填充的形状

### 实心填充矩形

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="20" name="Rectangle 19"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="2500000"/>
      <a:ext cx="1000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>  <!-- 橙色填充 -->
    </a:solidFill>
    <a:ln w="12700">  <!-- 边框宽度 -->
      <a:solidFill>
        <a:srgbClr val="D35400"/>  <!-- 深色边框 -->
      </a:solidFill>
    </a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr rtlCol="0" anchor="ctr"/>  <!-- 文本垂直居中 -->
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>  <!-- 水平居中 -->
      <a:r>
        <a:rPr lang="zh-CN" sz="1600" b="1">
          <a:solidFill>
            <a:srgbClr val="FFFFFF"/>
          </a:solidFill>
        </a:rPr>
        <a:t>标签文本</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 图片插入

### 将图片添加到幻灯片

```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="99" name="Company Logo"/>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rIdLogo"/>  <!-- 关系 ID 引用 -->
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="10800000" y="200000"/>  <!-- 右上角位置 -->
      <a:ext cx="800000" cy="600000"/>   <!-- Logo 尺寸 -->
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

### 添加图片关系

在 `ppt/slides/_rels/slideN.xml.rels` 中：

```xml
<Relationship Id="rIdLogo" 
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" 
  Target="../media/logo.png"/>
```

---

## 连接线

### 直线连接符

```xml
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="15" name="Straight Connector 14"/>
    <p:cNvCxnSpPr>
      <a:cxnSpLocks/>
    </p:cNvCxnSpPr>
    <p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="2500000"/>
      <a:ext cx="5000000" cy="0"/>  <!-- 水平线 -->
    </a:xfrm>
    <a:prstGeom prst="line">
      <a:avLst/>
    </a:prstGeom>
    <a:ln w="12700">
      <a:solidFill>
        <a:srgbClr val="E67E22"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

### 虚线

```xml
<p:spPr>
  <a:xfrm>
    <a:off x="500000" y="4500000"/>
    <a:ext cx="5000000" cy="0"/>
  </a:xfrm>
  <a:prstGeom prst="line">
    <a:avLst/>
  </a:prstGeom>
  <a:ln w="12700">
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
    <a:prstDash val="dash"/>  <!-- 虚线样式 -->
  </a:ln>
</p:spPr>
```

---

## 单位换算

| 单位 | 每单位 EMU 数 |
|------|---------------|
| 1 英寸 | 914400 |
| 1 厘米 | 360000 |
| 1 磅 | 12700 |
| 1 像素（96 DPI） | 9525 |

### 常见幻灯片尺寸（16:9）

- 宽度：12192000 EMU（13.333 英寸）
- 高度：6858000 EMU（7.5 英寸）

### 常见元素位置

| 元素 | X 位置 | Y 位置 |
|------|--------|--------|
| Logo（右上角） | 10800000 | 200000 |
| 标题 | 342583 | 286603 |
| 副标题 | 402591 | 1767390 |
| 页脚 | 342583 | 6435334 |
