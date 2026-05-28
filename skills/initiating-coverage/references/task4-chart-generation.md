# 任务 4：图表生成 - 详细工作流

本文档提供执行 initiating-coverage skill 任务 4（图表生成）的分步说明。

## 任务概览

**目的**：为报告生成 25–35 张专业财务图表。

**前置条件**：⚠️ 开始前验证
- **必需**：任务 1 的公司研究
  - 公司历史、里程碑（用于时间线图）
  - 管理团队、组织结构（用于组织结构图）
  - 产品组合（用于产品图）
  - 客户分层（用于客户图）
  - 竞争格局（用于竞争定位图）
  - TAM 分析（用于市场规模图）
- **必需**：任务 2 的财务模型
  - 按产品/地域拆分收入数据
  - Margin 趋势
  - 情景对比数据
- **必需**：任务 3 的估值分析
  - DCF 敏感性表
  - 可比公司数据
  - 估值区间
- **必需**：外部市场数据
  - 历史股价数据（Yahoo Finance、Bloomberg）
  - 历史估值倍数（图表 34 可选）

**⚠️ 关键：任务 1、2、3 未全部完成时，不要开始本任务**

本任务需要前三个任务的输出。缺少任何一项都会导致图表不完整。

**如果任务 1、2 或 3 任一未完成**：立即停止，并告知用户需要先完成哪些任务。具体要求是：
- 任务 1：公司研究文档（用于 9 张图）
- 任务 2：包含全部 6 个标签页的财务模型（用于 8 张图）
- 任务 3：已添加到模型的估值标签页（用于 6 张图）
- 外部数据访问（用于 2 张图）

不要尝试创建占位图表，也不要因缺少数据而跳过图表。

**输出**：25–35 个专业图表文件（PNG/JPG，300 DPI）

---

## 输入验证

**开始前检查全部前置条件：**

### 任务 1 验证（公司研究）
- [ ] 任务 1 是否已完成？（公司研究文档存在）
- [ ] 是否已记录公司历史和里程碑？（用于图表 05、06）
- [ ] 是否描述管理团队和组织结构？（用于图表 07）
- [ ] 产品组合是否详细？（用于图表 08）
- [ ] 是否分析客户分层？（用于图表 09）
- [ ] 是否绘制竞争格局？（用于图表 16、17、18）
- [ ] TAM 测算是否完成？（用于图表 15）

### 任务 2 验证（财务模型）
- [ ] 任务 2 是否已完成？（Excel 财务模型存在）
- [ ] 是否有按产品拆分收入？（用于图表 03 ⭐）
- [ ] 是否有按地域拆分收入？（用于图表 04 ⭐）
- [ ] 历史 + 预测财务数据是否完整？（用于图表 02、10、11、12）
- [ ] 情景分析（Bull/Base/Bear）是否完整？（用于图表 14）
- [ ] 是否有经营指标？（用于图表 13）

### 任务 3 验证（估值）
- [ ] 任务 3 是否已完成？（估值标签页已添加到模型）
- [ ] 是否存在 DCF 敏感性矩阵？（用于图表 28 ⭐）
- [ ] 是否有 DCF 计算明细？（用于图表 29）
- [ ] 是否已收集可比公司数据？（用于图表 30、31）
- [ ] 估值区间是否已计算？（用于图表 32 ⭐）

### 外部数据验证
- [ ] 是否可访问历史股价数据？（Yahoo Finance、Bloomberg，用于图表 01）
- [ ] 是否可访问历史估值数据？（可选，用于图表 34）

**如任何验证失败**：
- 缺少任务 1？→ 先完成任务 1（公司研究）
- 缺少任务 2？→ 先完成任务 2（财务建模）
- 缺少任务 3？→ 先完成任务 3（估值分析）
- 缺少外部数据？→ 从 Yahoo Finance、Bloomberg 或类似来源收集

---

## 图表要求：25 张必需 + 10 张可选

**重要**：任务 5（报告组装）会把**所有已创建图表**嵌入报告。报告需要高视觉密度（每 200–300 词 1 张图），因此要创建覆盖全面的图表包。

### 4 张强制图表（不可协商）⭐

以下 4 张是关键可视化，必须存在：

1. **chart_03**：按产品/分部拆分收入 - 堆叠面积图 ⭐
2. **chart_04**：按地域拆分收入 - 堆叠柱状图 ⭐
3. **chart_28**：DCF 敏感性分析 - 双因素热力图 ⭐
4. **chart_32**：估值 Football Field - 横向条形图 ⭐

### 25 张必需图表（完整集合）

创建以下全部 25 张图。每张图都在任务 5 中有具体用途：

**投资摘要章节（1 张）：**
- chart_01：股价表现（12–24 个月）

**财务表现章节（6 张）：**
- chart_02：收入增长轨迹
- chart_03：按产品拆分收入 - 堆叠面积图 ⭐ 强制
- chart_04：按地域拆分收入 - 堆叠柱状图 ⭐ 强制
- chart_10：毛利率变化
- chart_11：EBITDA 利润率演进
- chart_12：自由现金流趋势

**Company 101 章节（7 张）：**
- chart_05：公司概览/时间线
- chart_06：关键里程碑时间线
- chart_07：组织结构
- chart_08：产品组合概览
- chart_09：客户分层
- chart_15：市场规模演进（TAM）
- chart_16：竞争定位矩阵

**竞争与市场章节（2 张）：**
- chart_17：市场份额拆分
- chart_18：竞争基准对比

**情景分析章节（2 张）：**
- chart_13：经营指标仪表盘
- chart_14：情景对比（乐观/基准/悲观）

**估值章节（7 张）：**
- chart_28：DCF 敏感性热力图 ⭐ 强制
- chart_29：DCF 估值瀑布图
- chart_30：交易可比公司散点图
- chart_31：同业倍数对比
- chart_32：估值 Football Field ⭐ 强制
- chart_33：目标价情景
- chart_34：历史估值倍数

**总计：25 张必需图表**

### 10 张可选图表（用于达到 30–35 张）

如需更高视觉密度和更完整叙事，添加以下图表（总数达到 26–35 张）：

- chart_19：客户获取趋势
- chart_20：单位经济演进
- chart_21：产品路线图时间线
- chart_22：地域扩张地图
- chart_23：R&D 投资趋势
- chart_24：销售与市场效率
- chart_25：营运资本趋势
- chart_26：债务到期计划
- chart_27：所有权结构
- chart_35：分析师目标价分布

**总范围：25–35 张图表（25 必需 + 0–10 可选）**

---

## 必需图表的数据来源映射

理解每张图的数据来自哪里：

### 来自任务 1（公司研究）— 9 张
- chart_05：公司概览 → 任务 1：公司概览章节
- chart_06：关键里程碑 → 任务 1：公司历史章节
- chart_07：组织结构 → 任务 1：管理团队章节
- chart_08：产品组合 → 任务 1：产品与服务章节
- chart_09：客户分层 → 任务 1：客户与 Go-to-Market 章节
- chart_15：市场规模演进 → 任务 1：市场机会（TAM）章节
- chart_16：竞争定位 → 任务 1：竞争格局章节
- chart_17：市场份额 → 任务 1：竞争格局章节
- chart_18：竞争基准对比 → 任务 1：竞争格局章节

### 来自任务 2（财务模型）— 8 张
- chart_02：收入增长 → 利润表标签页（收入行）
- chart_03：按产品拆分收入 ⭐ → 收入模型标签页（按产品拆分）
- chart_04：按地域拆分收入 ⭐ → 收入模型标签页（按地域拆分）
- chart_10：毛利率 → 利润表标签页（毛利 / 收入）
- chart_11：EBITDA 利润率 → 利润表标签页（EBITDA / 收入）
- chart_12：自由现金流 → 现金流量表标签页（CFO - CapEx）
- chart_13：经营指标 → 多个标签页（利润表、现金流量表）
- chart_14：情景对比 → 情景标签页（乐观/基准/悲观）

### 来自任务 3（估值）— 6 张
- chart_28：DCF 敏感性 ⭐ → 敏感性分析标签页
- chart_29：DCF 瀑布图 → DCF 标签页（企业价值组成部分）
- chart_30：交易可比公司散点图 → 可比公司标签页
- chart_31：同业倍数 → 可比公司标签页
- chart_32：估值 Football Field ⭐ → 估值摘要标签页
- chart_33：目标价情景 → 估值摘要标签页（或从情景计算）

### 来自外部来源 — 2 张
- chart_01：股价表现 → Yahoo Finance、Bloomberg、Alpha Vantage
- chart_34：历史估值倍数 → Yahoo Finance、Bloomberg（历史 P/E、EV/EBITDA）

**重要**：要创建全部 25 张必需图表，必须完成任务 1、2、3，并能访问外部数据。

---

## 分步图表生成工作流

### 步骤 1：设置环境

**安装所需库：**
```bash
pip install matplotlib seaborn pandas numpy plotly
```

**创建 Python 脚本头部：**
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# 设置全局样式
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 全局设置
DPI = 300
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 6
TITLE_FONT_SIZE = 14
AXIS_FONT_SIZE = 12
LABEL_FONT_SIZE = 10
```

### 步骤 2：从模型和估值中提取数据

#### A. 提取收入数据
```python
# 按产品拆分收入（来自任务 2 模型）
years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029]

# 从 Excel 提取，或从模型手动定义
product_a = [100, 120, 145, 175, 210, 252, 302, 363, 435, 522]
product_b = [80, 95, 115, 138, 165, 198, 238, 285, 342, 411]
product_c = [50, 62, 78, 98, 122, 153, 191, 239, 299, 374]
product_d = [30, 38, 48, 61, 77, 97, 122, 153, 191, 239]

# 按地域拆分收入
north_america = [150, 180, 220, 265, 320, 384, 461, 553, 664, 797]
europe = [80, 95, 115, 140, 170, 204, 245, 294, 353, 423]
asia_pacific = [40, 50, 63, 80, 101, 127, 159, 199, 249, 311]
rest_of_world = [20, 25, 32, 40, 51, 64, 80, 100, 125, 156]
```

#### B. 提取 Margin 数据
```python
# Margin 演进
gross_margin = [58.0, 59.2, 60.5, 61.8, 63.0, 64.5, 66.0, 67.0, 67.5, 68.0]
ebitda_margin = [12.0, 15.5, 18.8, 22.0, 25.0, 28.0, 30.5, 32.0, 33.0, 34.0]
fcf_margin = [8.0, 11.0, 14.5, 18.0, 21.0, 24.0, 26.5, 28.0, 29.0, 30.0]
```

#### C. 提取 DCF 敏感性数据
```python
# DCF 敏感性（来自任务 3 估值）
wacc_values = [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
terminal_growth = [1.5, 2.0, 2.5, 3.0, 3.5]

# 每股价格矩阵（行 = WACC，列 = terminal growth）
dcf_sensitivity = np.array([
    [66, 71, 76, 82, 89],
    [58, 62, 67, 72, 78],
    [52, 55, 59, 63, 68],
    [47, 50, 53, 56, 60],
    [42, 45, 48, 51, 54],
    [39, 41, 44, 46, 49]
])
```

#### D. 提取估值区间
```python
# 估值 Football Field（来自任务 3）
valuation_methods = ['DCF 分析', '交易可比公司\n(NTM)', '先例\n交易']
valuation_low = [48, 45, 52]
valuation_high = [62, 57, 66]
current_price = 50
target_price = 55
```

### 步骤 3：创建强制图表

#### 图表 1：按产品拆分收入 - 堆叠面积图 ⭐ 强制

```python
def create_revenue_by_product_chart():
    """创建按产品拆分收入的堆叠面积图"""

    fig, ax = plt.subplots(figsize=(10, 6))

    # 创建堆叠面积图
    ax.stackplot(years, product_a, product_b, product_c, product_d,
                 labels=['产品 A', '产品 B', '产品 C', '产品 D'],
                 colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 alpha=0.8)

    # 格式
    ax.set_xlabel('年份', fontsize=12, fontweight='bold')
    ax.set_ylabel('收入 ($M)', fontsize=12, fontweight='bold')
    ax.set_title('图 3 - 按产品/分部拆分收入（2020-2029E）',
                 fontsize=14, fontweight='bold', pad=20)

    # 图例
    ax.legend(loc='upper left', frameon=False, fontsize=10)

    # 网格
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 添加竖线区分历史和预测
    ax.axvline(x=2024, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(2024.2, ax.get_ylim()[1]*0.95, '预测 →',
            fontsize=9, color='gray', ha='left')

    # 来源行
    fig.text(0.12, 0.02, '来源：公司数据，[机构]估算',
             fontsize=9, style='italic', color='gray')

    # 保存
    plt.tight_layout()
    plt.savefig('chart_03_revenue_by_product_stacked_area.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_03_revenue_by_product_stacked_area.png")

create_revenue_by_product_chart()
```

#### 图表 2：按地域拆分收入 - 堆叠柱状图 ⭐ 强制

```python
def create_revenue_by_geography_chart():
    """创建按地域拆分收入的堆叠柱状图"""

    years_labels = ['2020', '2021', '2022', '2023', '2024',
                    '2025E', '2026E', '2027E', '2028E', '2029E']

    fig, ax = plt.subplots(figsize=(10, 6))

    # 创建堆叠柱状图
    width = 0.6
    x = np.arange(len(years_labels))

    p1 = ax.bar(x, north_america, width, label='北美', color='#1f77b4')
    p2 = ax.bar(x, europe, width, bottom=north_america,
                label='欧洲', color='#ff7f0e')
    p3 = ax.bar(x, asia_pacific, width,
                bottom=np.array(north_america) + np.array(europe),
                label='亚太', color='#2ca02c')
    p4 = ax.bar(x, rest_of_world, width,
                bottom=np.array(north_america) + np.array(europe) + np.array(asia_pacific),
                label='世界其他地区', color='#d62728')

    # 格式
    ax.set_xlabel('年份', fontsize=12, fontweight='bold')
    ax.set_ylabel('收入 ($M)', fontsize=12, fontweight='bold')
    ax.set_title('图 4 - 按地域拆分收入（2020-2029E）',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years_labels, rotation=45, ha='right')

    # 图例
    ax.legend(loc='upper left', frameon=False, fontsize=10)

    # 网格
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 来源行
    fig.text(0.12, 0.02, '来源：公司数据，[机构]估算',
             fontsize=9, style='italic', color='gray')

    # 保存
    plt.tight_layout()
    plt.savefig('chart_04_revenue_by_geography_stacked_bar.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_04_revenue_by_geography_stacked_bar.png")

create_revenue_by_geography_chart()
```

#### 图表 3：DCF 敏感性 - 热力图 ⭐ 强制

```python
def create_dcf_sensitivity_heatmap():
    """创建 DCF 敏感性分析热力图"""

    # 创建 DataFrame
    df = pd.DataFrame(dcf_sensitivity,
                      index=[f'{w}%' for w in wacc_values],
                      columns=[f'{g}%' for g in terminal_growth])

    fig, ax = plt.subplots(figsize=(8, 6))

    # 创建热力图
    sns.heatmap(df, annot=True, fmt='d', cmap='RdYlGn',
                cbar_kws={'label': '每股价格 ($)'},
                linewidths=0.5, linecolor='white',
                ax=ax, vmin=35, vmax=95)

    # 格式
    ax.set_xlabel('终值增长率', fontsize=12, fontweight='bold')
    ax.set_ylabel('WACC', fontsize=12, fontweight='bold')
    ax.set_title('图 28 - DCF 敏感性分析（$/股）',
                 fontsize=14, fontweight='bold', pad=20)

    # 旋转 y 轴标签
    plt.yticks(rotation=0)

    # 来源行
    fig.text(0.12, 0.02, '来源：[机构]估算',
             fontsize=9, style='italic', color='gray')

    # 保存
    plt.tight_layout()
    plt.savefig('chart_28_dcf_sensitivity_heatmap.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_28_dcf_sensitivity_heatmap.png")

create_dcf_sensitivity_heatmap()
```

#### 图表 4：估值 Football Field ⭐ 强制

```python
def create_valuation_football_field():
    """创建估值 Football Field 图"""

    fig, ax = plt.subplots(figsize=(10, 5))

    # 创建横向条形
    y_positions = np.arange(len(valuation_methods))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, (method, low, high, color) in enumerate(
            zip(valuation_methods, valuation_low, valuation_high, colors)):
        ax.barh(i, high - low, left=low, height=0.6,
                color=color, alpha=0.7, label=method)

        # 在两端添加数值标签
        ax.text(low - 1, i, f'${low}', va='center', ha='right', fontsize=10)
        ax.text(high + 1, i, f'${high}', va='center', ha='left', fontsize=10)

    # 添加当前价格线
    ax.axvline(x=current_price, color='red', linestyle='--', linewidth=2,
               label=f'当前价格：${current_price}', alpha=0.7)

    # 添加目标价线
    ax.axvline(x=target_price, color='black', linestyle='-', linewidth=2,
               label=f'目标价：${target_price}')

    # 格式
    ax.set_yticks(y_positions)
    ax.set_yticklabels(valuation_methods, fontsize=11)
    ax.set_xlabel('每股价格 ($)', fontsize=12, fontweight='bold')
    ax.set_title('图 32 - 估值 Football Field',
                 fontsize=14, fontweight='bold', pad=20)

    # 设置 x 轴范围
    ax.set_xlim(40, 70)

    # 移除边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # 网格
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # 图例
    ax.legend(loc='upper right', frameon=False, fontsize=9)

    # 来源行
    fig.text(0.12, 0.02, '来源：[机构] 预测',
             fontsize=9, style='italic', color='gray')

    # 保存
    plt.tight_layout()
    plt.savefig('chart_32_valuation_football_field.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ 已创建：chart_32_valuation_football_field.png")

create_valuation_football_field()
```

### 步骤 4：创建其余必需图表（Charts 1–34）

**完成 25 张必需图表**，即创建必需清单中的所有剩余图表。每张图在任务 5 中都有具体用途。

#### 投资摘要（1 张）
```python
# chart_01：股价表现（12-24 个月）
# - 折线图，展示股价相对市场指数随时间变化
# - 用于最终报告第 1 页
```

#### 财务表现（除 chart_03 和 chart_04 外另 5 张）
```python
# chart_02: 收入增长轨迹
# chart_10: 毛利率演变
# chart_11: EBITDA 利润率变化
# chart_12: 自由现金流趋势
# chart_14: 情景对比（乐观/基准/悲观）
```

#### Company 101 章节（7 张）
```python
# chart_05: 公司概览/时间线
# chart_06: 关键里程碑时间线
# chart_07: 组织架构
# chart_08: 产品组合概览
# chart_09: 客户分层
# chart_15: 市场规模演变（TAM）
# chart_16: 竞争定位矩阵
```

#### 竞争与市场（2 张）
```python
# chart_17: 市场份额拆分
# chart_18: 竞争基准比较
```

#### 情景分析（1 张）
```python
# chart_13: 经营指标仪表盘
```

#### Valuation 章节（除 chart_28 和 chart_32 外另 6 张）
```python
# chart_29: DCF 估值瀑布图
# chart_30: 交易可比公司散点图
# chart_31: 同业倍数对比
# chart_33: 目标价情景
# chart_34: 历史估值倍数
```

**所有图表使用一致格式：**
- 300 DPI 分辨率
- 专业配色
- 清晰标签、图例和标题
- 图号（例如“图 5 - 公司时间线”）
- 底部来源引用

### 步骤 4B：创建可选图表（用于总数 26–35 张）

**可选**：从下列清单中再增加 1–10 张图表，以提高视觉密度：

```python
# chart_19: 客户获取趋势
# chart_20: 单位经济模型演变
# chart_21: 产品路线图时间线
# chart_22: 地域扩张地图
# chart_23: R&D 投入趋势
# chart_24: 销售与营销效率
# chart_25: 营运资本趋势
# chart_26: 债务到期明细表
# chart_27: 所有权结构
# chart_35: 分析师目标价分布
```

这些可选图表能补充视觉叙事，并帮助任务 5 达到“每 200–300 词 1 张图”的密度目标。

### 步骤 5：创建图表索引

创建一个记录所有图表的文本文件：

```python
def create_chart_index():
    """创建所有图表的索引"""

    # 25 张必需图表
    required_charts = [
        "chart_01_stock_price_performance.png - 股价表现（12-24M）",
        "chart_02_revenue_growth_trajectory.png - 收入增长轨迹",
        "chart_03_revenue_by_product_stacked_area.png - 按产品拆分收入 [强制]",
        "chart_04_revenue_by_geography_stacked_bar.png - 按地域拆分收入 [强制]",
        "chart_05_company_overview.png - 公司概览/时间线",
        "chart_06_key_milestones_timeline.png - 关键里程碑时间线",
        "chart_07_organizational_structure.png - 组织结构",
        "chart_08_product_portfolio.png - 产品组合概览",
        "chart_09_customer_segmentation.png - 客户分层",
        "chart_10_gross_margin_evolution.png - 毛利率变化",
        "chart_11_ebitda_margin_progression.png - EBITDA 利润率演进",
        "chart_12_free_cash_flow_trend.png - 自由现金流趋势",
        "chart_13_operating_metrics_dashboard.png - 经营指标仪表盘",
        "chart_14_scenario_comparison.png - 情景对比（乐观/基准/悲观）",
        "chart_15_market_size_evolution.png - 市场规模演进（TAM）",
        "chart_16_competitive_positioning.png - 竞争定位矩阵",
        "chart_17_market_share.png - 市场份额拆分",
        "chart_18_competitive_benchmarking.png - 竞争基准对比",
        "chart_28_dcf_sensitivity_heatmap.png - DCF 敏感性热力图 [强制]",
        "chart_29_dcf_waterfall.png - DCF 估值瀑布图",
        "chart_30_trading_comps_scatter.png - 交易可比公司散点图",
        "chart_31_peer_multiples_comparison.png - 同业倍数对比",
        "chart_32_valuation_football_field.png - 估值 Football Field [强制]",
        "chart_33_price_target_scenarios.png - 目标价情景",
        "chart_34_historical_valuation_multiples.png - 历史估值倍数",
    ]

    # 10 张可选图表（用于 26–35 张范围）
    optional_charts = [
        "chart_19_customer_acquisition_trends.png - 客户获取趋势 [可选]",
        "chart_20_unit_economics_evolution.png - 单位经济演进 [可选]",
        "chart_21_product_roadmap_timeline.png - 产品路线图时间线 [可选]",
        "chart_22_geographic_expansion_map.png - 地域扩张地图 [可选]",
        "chart_23_rd_investment_trends.png - R&D 投资趋势 [可选]",
        "chart_24_sales_marketing_efficiency.png - 销售与市场效率 [可选]",
        "chart_25_working_capital_trends.png - 营运资本趋势 [可选]",
        "chart_26_debt_maturity_schedule.png - 债务到期计划 [可选]",
        "chart_27_ownership_structure.png - 所有权结构 [可选]",
        "chart_35_analyst_price_targets.png - 分析师目标价分布 [可选]",
    ]

    with open('chart_index.txt', 'w') as f:
        f.write("[COMPANY] 股票研究报告图表索引\n")
        f.write("=" * 60 + "\n\n")

        f.write("4 张强制图表（必须存在）：\n")
        f.write("- chart_03: 按产品拆分收入（堆叠面积图）⭐\n")
        f.write("- chart_04: 按地域拆分收入（堆叠柱状图）⭐\n")
        f.write("- chart_28: DCF 敏感性（热力图）⭐\n")
        f.write("- chart_32: 估值 Football Field ⭐\n\n")

        f.write("25 张必需图表：\n")
        for chart in required_charts:
            f.write(f"  {chart}\n")

        f.write("\n10 张可选图表（用于总数 26–35 张）：\n")
        for chart in optional_charts:
            f.write(f"  {chart}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("说明：任务 5 会将所有已创建图表（25–35 张）嵌入报告，\n")
        f.write("以达到视觉密度要求（每 200–300 词 1 张图）。\n")

    print("✓ Created: chart_index.txt")

create_chart_index()
```

### 步骤 6：质量检查

**运行验证检查：**

```python
import os

def verify_charts():
    """验证所有图表是否成功创建"""

    mandatory_charts = [
        'chart_03_revenue_by_product_stacked_area.png',
        'chart_04_revenue_by_geography_stacked_bar.png',
        'chart_28_dcf_sensitivity_heatmap.png',
        'chart_32_valuation_football_field.png'
    ]

    print("\n" + "="*60)
    print("图表生成验证")
    print("="*60)

    # 检查强制图表
    print("\n1. 强制图表：")
    all_mandatory_present = True
    for chart in mandatory_charts:
        if os.path.exists(chart):
            size = os.path.getsize(chart) / 1024  # KB
            print(f"   ✓ {chart} ({size:.1f} KB)")
        else:
            print(f"   ✗ 缺失：{chart}")
            all_mandatory_present = False

    # 统计图表总数
    chart_files = [f for f in os.listdir('.') if f.startswith('chart_') and f.endswith('.png')]
    print(f"\n2. 图表总数：{len(chart_files)}")
    print(f"   目标：25–35 张图表")
    print(f"   状态：{'✓ PASS' if 25 <= len(chart_files) <= 35 else '⚠ WARNING'}")

    # 检查文件大小（300 DPI 通常应 > 50KB）
    print("\n3. 文件大小检查：")
    small_files = []
    for chart in chart_files[:5]:  # 抽样前 5 个
        size = os.path.getsize(chart) / 1024
        if size < 50:
            small_files.append(chart)
        print(f"   {chart}: {size:.1f} KB")

    if small_files:
        print(f"   ⚠ WARNING: {len(small_files)} files may be low resolution")
    else:
        print(f"   ✓ 抽样文件大小充足")

    # 最终结论
    print("\n" + "="*60)
    if all_mandatory_present and 25 <= len(chart_files) <= 35:
        print("✓ 验证通过 - 可进入任务 5")
    else:
        print("✗ 验证失败 - 请审阅缺失图表")
    print("="*60 + "\n")

verify_charts()
```

---

## 质量标准

### 视觉质量
- [ ] 高分辨率（最低 300 DPI）
- [ ] 专业配色（全部图表保持一致）
- [ ] 文字清晰可读（不得小于 9pt）
- [ ] 宽高比正确（无变形）
- [ ] 无像素化或瑕疵

### 数据准确性
- [ ] 数据与来源一致（财务模型和估值）
- [ ] 单位和标签正确（百万美元、百分比等）
- [ ] 尺度和范围合适
- [ ] 不同图表时间区间一致
- [ ] 计算已验证

### 格式质量
- [ ] 所有图表样式一致
- [ ] 图号正确（连续编号）
- [ ] 标题和图注清晰
- [ ] 每张图都有来源引用
- [ ] 外观专业

### 完整性
- [ ] 已创建全部 4 张强制图表
- [ ] 图表总数 25–35 张
- [ ] 文件命名正确（chart_01、chart_02 等）
- [ ] 已创建 chart index
- [ ] 可嵌入 Word

---

## 图表类型参考

### 何时使用各类图表

**折线图**：时间序列趋势（收入、利润率、股价）

**堆叠面积图**：按产品拆分收入 ⭐、市场规模构成

**堆叠柱状图**：按地域拆分收入 ⭐、季度拆分

**热力图**：DCF 敏感性 ⭐、相关矩阵

**横向条形图**：估值 Football Field ⭐、同业排名

**瀑布图**：收入桥、利润率分析、DCF 构建

**散点/气泡图**：growth vs. valuation、竞争定位

**2×2 矩阵**：竞争定位、产品组合

---

## 文件命名规范

**始终使用以下格式：**
```
chart_[NUMBER]_[DESCRIPTION].png

示例:
chart_01_stock_price_performance.png
chart_03_revenue_by_product_stacked_area.png
chart_28_dcf_sensitivity_heatmap.png
```

**按图表在报告中的位置连续编号**，不是按创建顺序编号。

---

## 常见图表生成问题

### 问题 1：分辨率低
**问题**：图表看起来像素化
**解决方案**：确保 `plt.savefig()` 中设置 `dpi=300`

### 问题 2：文字被截断
**问题**：标签或标题在边缘被截断
**解决方案**：在 `plt.savefig()` 中使用 `bbox_inches='tight'`

### 问题 3：颜色不专业
**问题**：颜色看起来不专业
**解决方案**：使用 Tableau10 等成熟配色，或定义自有企业色

### 问题 4：标签重叠
**问题**：坐标轴标签重叠
**解决方案**：旋转标签（例如 `rotation=45`）或减小字号

### 问题 5：空白太多
**问题**：图表周围留白过多
**解决方案**：保存前使用 `plt.tight_layout()`

---

## 成功标准

成功的图表包应当：
1. **包含全部 4 张强制图表**（已验证）⭐
   - chart_03：按产品拆分收入
   - chart_04：按地域拆分收入
   - chart_28：DCF 敏感性
   - chart_32：估值 Football Field
2. **至少创建 25 张必需图表**（已验证）
3. **可选：增加 1–10 张图表**，使总数达到 26–35 张
4. 所有图表风格一致且专业
5. 高分辨率（300 DPI），适合打印
6. 每张图都有清晰标签、图例和标题
7. 包含正确图号和来源引用
8. 可立即嵌入 Word
9. 覆盖全部关键财务指标和分析
10. 形成与书面分析互补的视觉故事
11. 准确且可追溯至来源数据（模型/估值）
12. 所有图表已与 chart index 一并打包为 zip 文件

**记住**：任务 5 会把全部已创建图表（25–35 张）嵌入报告，以满足视觉密度要求。

---

## 输出文件

完成任务 4 后，交付物包括：

**25 个必需图表文件（最低）：**
1. chart_01_stock_price_performance.png
2. chart_02_revenue_growth_trajectory.png
3. chart_03_revenue_by_product_stacked_area.png ⭐ 强制
4. chart_04_revenue_by_geography_stacked_bar.png ⭐ 强制
5. chart_05_company_overview.png
6. chart_06_key_milestones_timeline.png
7. chart_07_organizational_structure.png
8. chart_08_product_portfolio.png
9. chart_09_customer_segmentation.png
10. chart_10_gross_margin_evolution.png
11. chart_11_ebitda_margin_progression.png
12. chart_12_free_cash_flow_trend.png
13. chart_13_operating_metrics_dashboard.png
14. chart_14_scenario_comparison.png
15. chart_15_market_size_evolution.png
16. chart_16_competitive_positioning.png
17. chart_17_market_share.png
18. chart_18_competitive_benchmarking.png
19–27. *如创建可选图表，则保留给可选图表*
28. chart_28_dcf_sensitivity_heatmap.png ⭐ 强制
29. chart_29_dcf_waterfall.png
30. chart_30_trading_comps_scatter.png
31. chart_31_peer_multiples_comparison.png
32. chart_32_valuation_football_field.png ⭐ 强制
33. chart_33_price_target_scenarios.png
34. chart_34_historical_valuation_multiples.png
35. *如创建可选图表，则保留给可选图表*

**10 个可选图表文件（用于总数 26–35）：**
- chart_19 至 chart_27、chart_35（如创建）

**Chart Index**（1 个文本文件）：
- `chart_index.txt`（列出全部图表、说明和类别）

**所有图表文件必须：**
- 300 DPI 分辨率（印刷质量）
- 6–10 英寸宽（标准 Word 嵌入尺寸）
- 白色背景（专业外观）
- PNG 格式（无损质量）
- 可立即嵌入 Word

**最终步骤：打包全部图表**

创建包含所有图表文件和 chart index 的 zip 文件：

```
[Company]_Charts_[Date].zip
├── chart_01_stock_price_performance.png
├── chart_02_revenue_growth_trajectory.png
├── chart_03_revenue_by_product_stacked_area.png ⭐
├── chart_04_revenue_by_geography_stacked_bar.png ⭐
├── chart_05_company_overview.png
├── ... (all 25-35 chart files)
├── chart_28_dcf_sensitivity_heatmap.png ⭐
├── chart_32_valuation_football_field.png ⭐
├── chart_34_historical_valuation_multiples.png
└── chart_index.txt
```

**示例**：`Tesla_Charts_2024-10-28.zip`

**为什么重要**：任务 5 会把全部已创建图表（25–35 张）嵌入报告。报告需要视觉密度（每 200–300 词 1 张图），因此所有图表都有用途：要么服务特定分析章节，要么服务视觉叙事和页面密度。
- 验证全部 25–35 张图表都存在
- 为任务 5（报告组装）提取图表

---

## 下一步

完成任务 4 后，zip 文件将用于：
- **任务 5（报告组装）**：解压图表，并在最终 DOCX 报告全文适当位置嵌入全部图表

4 张强制图表对报告中的估值和财务分析章节至关重要。
