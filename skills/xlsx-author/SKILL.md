---
name: xlsx-author
description: 在磁盘生成 .xlsx 文件（无界面），而不是驱动实时 Excel 工作簿；用于没有打开 Office 应用的托管代理会话。
---

## 中文版执行契约

- 默认使用中国大陆金融语境：A股优先，港股和美股兼容；如用户指定市场、币种、会计准则或模板，以用户输入为准。
- 数据来源必须遵守根目录 `DATA_SOURCES_CN.md`：官方披露、用户文件、已授权 MCP/数据库优先；免费源只作辅助；监管、会计、KYC、基金文件和月结判断无依据时写“需确认”。
- 所有产物必须遵守根目录 `CN_OUTPUT_FORMATTING.md`：中文字体栈、中文日期、币种/单位、图表标题、表格表头、来源脚注、风险提示和免责声明都要按中文机构材料处理。
- 用户模板和品牌规范优先，但不得突破中文可读性、来源脚注、币种/单位/日期/口径说明这些底线。
- 保留 DCF、LBO、WACC、EV/EBITDA、IRR、MOIC、NAV、KYC、AML、MCP、CLI 等专业缩写和代码标识。


# xlsx-author（XLSX 作者）

当处于**无界面**运行环境，且需要交付一个 Excel 工作簿作为**文件产物**，而不是通过 `mcp__office__excel_*` 编辑实时工作簿时，使用本 skill。

## 输出契约

- 写入 `./out/<name>.xlsx`。如果 `./out/` 不存在，则创建该目录。
- 在最终消息中返回相对路径，便于编排层收集产物。

## 构建工作簿

编写一个简短 Python 脚本并用 Bash 运行。使用 `openpyxl`：

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active; ws.title = "Inputs"
ws["B2"] = "收入"; ws["C2"] = 1_250_000_000
ws["C2"].font = Font(color="0000FF")           # blue = hardcoded input
calc = wb.create_sheet("DCF")
calc["C5"] = "=Inputs!C2*(1+Inputs!C3)"        # black = formula
wb.save("./out/model.xlsx")
```

## 约定（对齐 `audit-xls`）

- **蓝色 / 黑色 / 绿色。** 蓝色 = 硬编码输入，黑色 = 公式，绿色 = 指向其他工作表/文件的链接。
- **计算单元格不允许硬编码。** 每个计算单元格都必须是公式；所有输入都放在 Inputs 工作表。
- **命名区域。** 对材料或备忘录引用的任何数值设置命名区域。
- **勾稽检查。** 包含 Checks 工作表，检查资产负债表平衡、现金流与现金勾稽等，并显示 TRUE/FALSE。
- **每个文件一个模型。** 除非用户明确要求，不要追加到已有工作簿。

## 不适用场景

如果 `mcp__office__excel_*` 工具可用，优先使用这些工具；它们会驱动用户的实时工作簿并保留审阅节点。本 skill 是无界面运行时的文件生成 fallback。
