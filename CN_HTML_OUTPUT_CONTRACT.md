# 中文 HTML 交付契约

本文件是 `financial-services-cn` 的中文 HTML 交付契约。任何 skill 生成 `.html`、网页报告、可打开的本地 HTML 或可部署的静态页面时，都必须遵守本契约。

## 1. 字体

- HTML 唯一指定字体为 `Source Han Serif CN`。
- 必须使用在线 CDN `@font-face` 定义 Regular 和 Bold 两种字重；不得在仓库内嵌入字体文件。
- CSS 必须包含以下字体声明：

```css
@font-face {
  font-family: "Source Han Serif CN";
  font-style: normal;
  font-weight: 400;
  src: url("https://cdn.jsdelivr.net/gh/adobe-fonts/source-han-serif@release/SubsetOTF/CN/SourceHanSerifCN-Regular.otf") format("opentype");
}

@font-face {
  font-family: "Source Han Serif CN";
  font-style: normal;
  font-weight: 700;
  src: url("https://cdn.jsdelivr.net/gh/adobe-fonts/source-han-serif@release/SubsetOTF/CN/SourceHanSerifCN-Bold.otf") format("opentype");
}
```

- `body`、表格、图表、来源、脚注和免责声明的 `font-family` 必须写为 `"Source Han Serif CN"`。

## 2. 排版参数

- 正文默认 15px Regular，line-height 1.55。
- H1 默认 24px Bold，line-height 1.25，段前 24px，段后 10px。
- H2 默认 20px Bold，line-height 1.30，段前 18px，段后 8px。
- H3 默认 17px Bold，line-height 1.35，段前 14px，段后 6px。
- 表头默认 13px Bold，line-height 1.35，padding 6px 8px。
- 表体默认 13px Regular，line-height 1.35，padding 6px 8px。
- 来源、注释和免责声明默认 12px Regular，line-height 1.35，颜色 `#666666`。
- 图表内部来源默认 7pt Regular，颜色 `#666666`。

## 3. 内容和来源

- HTML 必须使用中文标题、表头、图例、来源和免责声明。
- 链接必须使用有意义显示文本，避免裸 URL。
- 图表必须在图表内部写明来源和数据日期；多来源清单放入“数据来源与口径说明”。
- 正式表格缺失值使用 `—`。

## 4. 验收

- HTML 文件存在且可在浏览器打开。
- 字体 CSS 使用上述两个 CDN URL。
- 页面没有明显文字重叠、表格溢出或图表遮挡。
- 最终回复包含 HTML 文件路径；如生成 PDF 或截图，也必须包含对应路径。
