> Reference 链路：执行本文件前，先读取插件根目录 `../../../DATA_QUERY_ORDER_CN.md`，并读取插件根目录 `../../../CN_OUTPUT_FORMATTING.md`、`../../../CN_MARKDOWN_OUTPUT_CONTRACT.md`、`../../../CN_DOCX_OUTPUT_CONTRACT.md`、`../../../CN_XLSX_OUTPUT_CONTRACT.md`、`../../../CN_CHART_OUTPUT_CONTRACT.md`；本文件只描述业务 workflow 或参考口径，不承载新增中文格式正文。

# 任务 2：财务建模 - 详细工作流

本文档提供执行 initiating-coverage skill 任务 2（财务建模）的分步说明。

## 任务概览

**目的**：提取历史财务数据，并构建包含预测和情景的完整 Excel 财务模型。

**前置条件**：⚠️ 开始前验证
- **必需**：可访问公司财务数据
  - 上市公司：SEC EDGAR 最新 10-K 和近期 10-Q
  - 私营公司：财务报表，或来自可用来源的估算
  - 或：用户提供的已提取历史财务数据
- **可选**：公司研究（任务 1）提供业务背景

**输出**：Excel 财务模型（.xlsx），包含 6 个核心标签页：
1. 收入模型
2. 利润表
3. 现金流量表
4. 资产负债表
5. 情景分析
6. DCF 输入

---

## 输入验证

**开始前检查：**

**路径 A：直接提取财务数据（最常见）**
- [ ] 是否可访问 10-K 披露文件（上市公司）？
- [ ] 或是否可访问财务报表（私营公司）？
- [ ] 是否准备好创建 Excel 文件用于历史数据提取？

**路径 B：用户已提供预提取财务数据**
- [ ] 是否已提供历史财务文件？（.xlsx 或其他格式）
- [ ] 是否包含 3–5 年利润表、现金流量表和资产负债表？
- [ ] 数据是否干净且可直接使用？

**可选背景：**
- [ ] 公司研究（任务 1）是否已完成，用于理解业务？

**如验证失败**：停止，并先取得财务报表（10-K 或等价文件）访问权限。

---

## 模型结构与格式

### 颜色编码（行业标准）
- **蓝色文字**：硬编码输入（用户可改）
- **黑色文字**：公式和计算
- **绿色文字**：指向其他 sheet 的链接
- **红色文字**：错误或提示（应解决）

### 格式标准
- 专业边框和底纹
- 清晰章节标题
- 分组行，支持折叠
- 关键输入/输出使用 named ranges
- 公式中不要硬编码数字（12 个月等常数除外）
- 明确单位（$ thousands、$ millions 等）

### 公式最佳实践
- 所有数字都应从假设流出
- 改变一个假设 → 整个模型会更新
- 不要出现循环引用
- 关键单元格使用 named ranges
- 公式保持简单且可审计
- 复杂计算添加注释

---

## 分步建模工作流

### 步骤 1：提取历史财务数据

**如果历史财务数据已经提取，跳到步骤 2。**

**对上市公司：**

1. **下载 10-K 披露文件**
   - 访问 SEC EDGAR（https://www.sec.gov/edgar/searchedgar/companysearch.html）
   - 搜索公司名称或股票代码
   - 下载最新 10-K（年度报告）
   - 进入第 8 项：财务报表及补充数据

2. **创建历史财务 Excel 文件**
   - 文件名：`[公司]_历史财务_[日期].xlsx`
   - 该文件将成为模型基础

3. **提取利润表（3–5 年）**
   - 创建 Sheet 1：“历史利润表”
   - 提取 3–5 年全部科目：
     - 收入（总额及按分部拆分，如披露）
     - 收入成本 / COGS
     - 毛利
     - 经营费用（R&D、销售与营销、G&A 拆分）
     - EBITDA（如未披露则计算：EBIT + D&A）
     - EBIT / 经营利润
     - 利息费用/收入
     - 其他收入/费用
     - 税前利润
     - Income tax 和 tax rate
     - 净利润
     - EPS（basic 和 diluted）
     - Shares outstanding（basic 和 diluted）

4. **提取现金流量表（3–5 年）**
   - 创建 Sheet 2：“历史现金流量表”
   - 提取全部科目：
     - 经营活动（从净利润开始）
     - 折旧与摊销
     - 股权激励费用
     - 营运资本变化（应收账款、存货、应付账款）
     - 经营活动现金流
     - 投资活动（CapEx、收购）
     - 融资活动（债务发行/偿还、股权、分红）
     - 现金净变动
     - 期初和期末现金

5. **提取资产负债表（3–5 年）**
   - 创建 Sheet 3：“历史资产负债表”
   - 提取全部科目：
     - 流动资产（现金、应收账款、存货、其他）
     - 非流动资产（PP&E、无形资产、商誉）
     - 总资产
     - 流动负债（应付账款、应计费用、流动债务）
     - 非流动负债（长期债务、递延税项）
     - 总负债
     - 股东权益（普通股、留存收益）
     - 总负债 + 权益

6. **计算历史指标**
   - 创建 Sheet 4：“历史指标”
   - 根据三张表计算：
     - 收入增速 %（YoY）
     - 毛利率 %
     - EBITDA 利润率 %
     - 经营利润率 %
     - 净利率 %
     - 自由现金流（CFO - CapEx）
     - FCF 利润率 %
     - ROIC（近似：NOPAT / Invested Capital）
     - 债务/权益比率
     - 流动比率（流动资产 / 流动负债）

7. **记录来源和注释**
   - 创建第 5 个标签页：“附注”
   - 记录：
     - 10-K 提交日期和财年结束日
     - 任何一次性项目或调整
     - Non-GAAP 与 GAAP 差异
     - 分部拆分（如按产品/地域披露收入）
     - 数据质量说明和限制

**对私营公司：**

1. **收集可得数据**
   - 财务报表（如可得）
   - 包含收入数字的新闻稿
   - 融资公告
   - 行业估算或可比公司数据

2. **创建简化历史文件**
   - 估算收入（如可得）
   - 估算利润率（必要时来自可比公司）
   - 关键比率和指标
   - 记录所有假设和来源

**验证：**
- [ ] 三张财务报表均已提取（3–5 年）
- [ ] 报表之间数字可勾稽（net income 可对应）
- [ ] 关键指标计算正确
- [ ] Excel 文件已保存且可打开
- [ ] 已记录数据来源（10-K 日期、页码）

**预测模型基础已完成。继续步骤 2。**
- 资本开支
- 营运资本项目
- 债务和利息费用
- 股数（basic 和 diluted）

3. **整理历史数据以便录入**
   - 准备 3–5 年实际数据
   - 将直接录入利润表、现金流量表和资产负债表标签页
   - 历史年份作为列，预测年份紧随其后

4. **计算历史趋势**
   - 收入 CAGR
   - 利润率演进
   - OpEx 杠杆
   - 营运资本模式
   - CapEx 占收入比例
   - 这些趋势将支持预测假设

**注意**：假设将直接作为蓝色文字输入记录在各标签页中，不单独设置假设标签页。

### 步骤 2：建模收入

**关键：这是模型最重要、最详细的部分。**

#### A. 按产品/类别拆分收入（20–30 行）

创建详细表格：
```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
产品类别 A
  子产品 A1             XX      XX      XX      XX      XX      XX      XX      XX      XX
  子产品 A2             XX      XX      XX      XX      XX      XX      XX      XX      XX
  子产品 A3             XX      XX      XX      XX      XX      XX      XX      XX      XX
  类别 A 合计           XX      XX      XX      XX      XX      XX      XX      XX      XX
  占总收入 %            X%      X%      X%      X%      X%      X%      X%      X%      X%
  YoY 增长率 %          -       X%      X%      X%      X%      X%      X%      X%      X%

产品类别 B
  [类似结构]

[继续列出所有产品类别]

服务收入                XX      XX      XX      XX      XX      XX      XX      XX      XX
其他收入                XX      XX      XX      XX      XX      XX      XX      XX      XX

总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
总收入增长率 %          -       X%      X%      X%      X%      X%      X%      X%      X%
```

**关键要求：**
- 展示每个类别的绝对收入（$M）
- 计算每个类别占总收入的比例
- 展示每个类别 YoY 增长率 %
- 必须包含细颗粒度子类别（不能只有 3–5 个顶层类别）
- 展示结构变化随时间变化
- 所有预测都要链接到假设输入

#### B. 按地域拆分收入（15–20 行）

创建详细表格：
```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
北美
  美国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  加拿大                XX      XX      XX      XX      XX      XX      XX      XX      XX
  墨西哥                XX      XX      XX      XX      XX      XX      XX      XX      XX
  北美合计              XX      XX      XX      XX      XX      XX      XX      XX      XX
  占总额 %              X%      X%      X%      X%      X%      X%      X%      X%      X%
  YoY 增长率 %          -       X%      X%      X%      X%      X%      X%      X%      X%

欧洲
  英国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  德国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  法国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  欧洲其他地区          XX      XX      XX      XX      XX      XX      XX      XX      XX
  欧洲合计              XX      XX      XX      XX      XX      XX      XX      XX      XX
  占总额 %              X%      X%      X%      X%      X%      X%      X%      X%      X%
  YoY 增长率 %          -       X%      X%      X%      X%      X%      X%      X%      X%

亚太
  [类似结构]

世界其他地区
  [类似结构]

总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
```

**验证：**
- 按产品拆分收入合计 = 按地域拆分收入合计 = 总收入
- 所有百分比合计为 100%
- 增长率计算正确

#### C. 按渠道拆分收入（如适用）

```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
直销                    XX      XX      XX      XX      XX      XX      XX      XX      XX
电商/线上               XX      XX      XX      XX      XX      XX      XX      XX      XX
批发/合作伙伴           XX      XX      XX      XX      XX      XX      XX      XX      XX
零售门店
  公司自营门店          XX      XX      XX      XX      XX      XX      XX      XX      XX
  门店数量              XX      XX      XX      XX      XX      XX      XX      XX      XX
  单店销售额            XX      XX      XX      XX      XX      XX      XX      XX      XX
其他渠道                XX      XX      XX      XX      XX      XX      XX      XX      XX

总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
```

### 步骤 3：建模经营费用

#### A. 收入成本
1. **拆分 COGS 构成**
   - 产品成本（材料、制造）
   - 运输与物流
   - 服务交付成本
   - 其他直接成本

2. **链接到收入**
   - 将 COGS 计算为收入的百分比
   - 按年度建模毛利率
   - 链接到假设输入

#### B. R&D 费用
```
研发                    2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
R&D 人数                XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D 人均薪酬            XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D 人员成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D 其他成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D 合计                XX      XX      XX      XX      XX      XX      XX      XX      XX
占收入 %                X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### C. 销售与营销费用
```
销售与营销              2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
S&M 人数                XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M 人均薪酬            XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M 人员成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
营销支出                XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M 其他成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M 合计                XX      XX      XX      XX      XX      XX      XX      XX      XX
占收入 %                X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### D. 一般及行政费用
```
G&A                     2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
G&A 人数                XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A 人均薪酬            XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A 人员成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A 其他成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A 合计                XX      XX      XX      XX      XX      XX      XX      XX      XX
占收入 %                X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### E. 折旧与摊销
- 链接到 CapEx 明细表
- 应用假设中的折旧率
- 计算年度 D&A

### 步骤 4：构建利润表

**创建包含 40–50 个科目的完整 P&L：**

```
利润表                  2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

收入
[链接到收入模型标签页]
总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  YoY 增长率 %          -       X%      X%      X%      X%      X%      X%      X%      X%

收入成本
[链接到 COGS 明细]
总 COGS                 XX      XX      XX      XX      XX      XX      XX      XX      XX

毛利                    XX      XX      XX      XX      XX      XX      XX      XX      XX
  毛利率 %              X%      X%      X%      X%      X%      X%      X%      X%      X%

经营费用
R&D 合计                XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入 %              X%      X%      X%      X%      X%      X%      X%      X%      X%
S&M 合计                XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入 %              X%      X%      X%      X%      X%      X%      X%      X%      X%
G&A 合计                XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入 %              X%      X%      X%      X%      X%      X%      X%      X%      X%
折旧与摊销              XX      XX      XX      XX      XX      XX      XX      XX      XX

经营费用合计            XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入 %              X%      X%      X%      X%      X%      X%      X%      X%      X%

EBITDA                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  EBITDA 利润率 %       X%      X%      X%      X%      X%      X%      X%      X%      X%

EBIT                    XX      XX      XX      XX      XX      XX      XX      XX      XX
  EBIT 利润率 %         X%      X%      X%      X%      X%      X%      X%      X%      X%

利息费用                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
利息收入                XX      XX      XX      XX      XX      XX      XX      XX      XX
其他收入/(费用)         XX      XX      XX      XX      XX      XX      XX      XX      XX

税前利润                XX      XX      XX      XX      XX      XX      XX      XX      XX

所得税                  (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  税率 %                X%      X%      X%      X%      X%      X%      X%      X%      X%

净利润                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  净利率 %              X%      X%      X%      X%      X%      X%      X%      X%      X%

流通股数
基本股数 (M)            XX      XX      XX      XX      XX      XX      XX      XX      XX
稀释后股数 (M)          XX      XX      XX      XX      XX      XX      XX      XX      XX

每股收益
基本 EPS                $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX
稀释后 EPS              $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX
```

### 步骤 5：构建现金流量表

```
现金流量表              2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

经营活动
净利润                  XX      XX      XX      XX      XX      XX      XX      XX      XX
调整项：
  折旧与摊销            XX      XX      XX      XX      XX      XX      XX      XX      XX
  股权激励费用          XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他非现金项目        XX      XX      XX      XX      XX      XX      XX      XX      XX

营运资本变动：
  应收账款              (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  存货                  (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  应付账款              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他营运资本          (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)

经营活动现金流          XX      XX      XX      XX      XX      XX      XX      XX      XX

投资活动
资本开支                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
收购                    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
其他投资活动            XX      XX      XX      XX      XX      XX      XX      XX      XX

投资活动现金流          (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)

自由现金流              XX      XX      XX      XX      XX      XX      XX      XX      XX
  FCF 利润率 %          X%      X%      X%      X%      X%      X%      X%      X%      X%

融资活动
债务发行                XX      XX      XX      XX      XX      XX      XX      XX      XX
债务偿还                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
股权发行                XX      XX      XX      XX      XX      XX      XX      XX      XX
已付股利                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
其他融资活动            XX      XX      XX      XX      XX      XX      XX      XX      XX

融资活动现金流          XX      XX      XX      XX      XX      XX      XX      XX      XX

现金净变动              XX      XX      XX      XX      XX      XX      XX      XX      XX

期初现金                XX      XX      XX      XX      XX      XX      XX      XX      XX
期末现金                XX      XX      XX      XX      XX      XX      XX      XX      XX
```

### 步骤 6：构建资产负债表

创建包含 35–45 个科目的完整资产负债表：

```
资产负债表              2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

资产
流动资产：
  现金及等价物          XX      XX      XX      XX      XX      XX      XX      XX      XX
  应收账款              XX      XX      XX      XX      XX      XX      XX      XX      XX
  存货                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  预付费用              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他流动资产          XX      XX      XX      XX      XX      XX      XX      XX      XX
流动资产合计            XX      XX      XX      XX      XX      XX      XX      XX      XX

非流动资产：
  PP&E 原值             XX      XX      XX      XX      XX      XX      XX      XX      XX
  累计折旧              (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  PP&E 净额             XX      XX      XX      XX      XX      XX      XX      XX      XX
  无形资产              XX      XX      XX      XX      XX      XX      XX      XX      XX
  商誉                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他非流动资产        XX      XX      XX      XX      XX      XX      XX      XX      XX
非流动资产合计          XX      XX      XX      XX      XX      XX      XX      XX      XX

总资产                  XX      XX      XX      XX      XX      XX      XX      XX      XX

负债
流动负债：
  应付账款              XX      XX      XX      XX      XX      XX      XX      XX      XX
  应计费用              XX      XX      XX      XX      XX      XX      XX      XX      XX
  递延收入              XX      XX      XX      XX      XX      XX      XX      XX      XX
  一年内到期债务        XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他流动负债          XX      XX      XX      XX      XX      XX      XX      XX      XX
流动负债合计            XX      XX      XX      XX      XX      XX      XX      XX      XX

非流动负债：
  长期债务              XX      XX      XX      XX      XX      XX      XX      XX      XX
  递延所得税            XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他非流动负债        XX      XX      XX      XX      XX      XX      XX      XX      XX
非流动负债合计          XX      XX      XX      XX      XX      XX      XX      XX      XX

总负债                  XX      XX      XX      XX      XX      XX      XX      XX      XX

权益
  普通股                XX      XX      XX      XX      XX      XX      XX      XX      XX
  资本公积              XX      XX      XX      XX      XX      XX      XX      XX      XX
  留存收益              XX      XX      XX      XX      XX      XX      XX      XX      XX
  库存股                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  其他权益              XX      XX      XX      XX      XX      XX      XX      XX      XX
总权益                  XX      XX      XX      XX      XX      XX      XX      XX      XX

总负债 + 权益           XX      XX      XX      XX      XX      XX      XX      XX      XX

平衡检查                OK      OK      OK      OK      OK      OK      OK      OK      OK
```

**平衡检查公式：**
- 每年总资产必须等于总负债与股东权益之和
- 任何不平衡都用红色标记

### 步骤 7：构建 DCF 输入标签页

为估值（任务 3）准备输入：

```
DCF 输入                2025E   2026E   2027E   2028E   2029E

EBIT                    XX      XX      XX      XX      XX
税率                    X%      X%      X%      X%      X%
NOPAT                   XX      XX      XX      XX      XX

加：D&A                 XX      XX      XX      XX      XX
减：CapEx               (XX)    (XX)    (XX)    (XX)    (XX)
减：NWC 变动            (XX)    (XX)    (XX)    (XX)    (XX)

无杠杆 FCF              XX      XX      XX      XX      XX

终值年度指标：
  2029E 收入            $X,XXX
  2029E EBITDA          $XXX
  2029E EBIT            $XXX
  2029E 无杠杆 FCF      $XXX
```

### 步骤 8：构建情景标签页

使用不同假设创建三种情景：

#### 情景假设表
```
假设                            乐观        基准        悲观
收入 CAGR (2025-2029)           XX%         XX%         XX%
2029E 毛利率                    XX%         XX%         XX%
2029E EBITDA 利润率             XX%         XX%         XX%
CapEx 占收入 %                  X%          X%          X%
[添加其他关键假设]
```

#### 情景输出表
```
指标                            乐观        基准        悲观
2029E 收入 ($M)                 $X,XXX      $X,XXX      $X,XXX
2029E EBITDA ($M)               $XXX        $XXX        $XXX
2029E EBITDA 利润率             XX%         XX%         XX%
2029E 净利润 ($M)               $XXX        $XXX        $XXX
2029E EPS                       $X.XX       $X.XX       $X.XX
2029E FCF ($M)                  $XXX        $XXX        $XXX
2029E FCF 利润率                XX%         XX%         XX%

2025-2029 年累计 FCF ($M)       $XXX        $XXX        $XXX
```

**记录情景理由：**
- Bull case：[描述乐观但可实现的假设]
- Base case：[描述最可能情景]
- Bear case：[描述下行风险和触发因素]

### 步骤 9：质量检查

**验证模型完整性：**
1. [ ] 测试所有公式（抽样检查计算）
2. [ ] 改变假设 → 验证模型正确更新
3. [ ] 测试情景切换
4. [ ] 验证颜色编码（蓝/黑/绿）
5. [ ] 检查所有年份资产负债表平衡
6. [ ] 验证无循环引用（Excel 会提示）
7. [ ] 检查预测中是否有硬编码数字
8. [ ] 验证所有跨标签页链接有效
9. [ ] 测试各标签页收入合计是否勾稽
10. [ ] 审阅格式和展示效果

---

## 质量标准

### 模型完整性
- 所有公式在各标签页间正确链接
- 预测中没有硬编码数字（假设输入除外）
- 无循环引用
- 所有年份资产负债表平衡
- 情景切换正常工作

### 完整性
- 包含全部 6 个核心标签页：收入模型、利润表、现金流量表、资产负债表、情景、DCF 输入
- 利润表包含 40–50 个科目
- 收入模型中产品拆分 20–30 行
- 收入模型中地域拆分 15–20 行
- 完整现金流量表和资产负债表，包含全部科目
- 乐观/基准/悲观情景完整

### 专业格式
- 颜色编码一致（蓝/黑/绿）
- 标题和标签清晰
- 边框和底纹正确
- 关键单元格使用命名区域
- 分组行支持折叠
- 单位清晰标注（千美元 vs. 百万美元）

### 文档记录
- 假设记录了理由（蓝色文字单元格 + 批注）
- 数据来源记录在单元格批注或标签页内说明区域
- 复杂计算通过批注解释
- 描述方法论

---

## 文件命名规范

将财务模型保存为：
`[Company]_Financial_Model_[Date].xlsx`

示例：`Tesla_Financial_Model_2024-10-27.xlsx`

---

## 成功标准

成功的财务模型应当：
1. 包含全部 6 个核心标签页（收入模型、利润表、现金流量表、资产负债表、情景、DCF 输入）
2. 完全动态（改变假设 → 模型更新）
3. 预测中没有硬编码数字
4. 包含详细收入拆分（按产品 20–30 行、按地域 15–20 行）
5. 利润表包含 40–50 个科目
6. 包含 Bull/Base/Bear 情景
7. 使用专业格式和颜色编码
8. 正确勾稽（资产负债表、现金流）
9. 可审计且易于理解
10. 通过正确 FCF 计算支持估值分析

---

## 常见模型类型 - 特别注意事项

### 高增长科技 / SaaS
- 关注 ARR 增长和净留存
- 按产品线和地域建模
- R&D 和 S&M 投入较重
- 盈利路径时间线
- 单位经济（LTV/CAC）

### 电商 / 零售
- 按产品类别和渠道拆分收入
- 门店数和同店增长（如适用）
- 存货周转和营运资本
- 履约成本
- 客户获取

### 制造 / 工业
- 产能利用率
- 原材料成本和定价
- 毛利桥（销量/价格/结构/成本）
- CapEx 密集型模型
- 营运资本周期

---

## 下一步

完成任务 2 后，财务模型将用于：
- **任务 3（估值）**：DCF 输入、预测财务数据
- **任务 4（图表）**：收入趋势、利润率图表、情景对比数据
- **任务 5（报告组装）**：报告表格和分析所需财务数据
