# OpenBB 金融数据 MCP 接入 Codex：从零搭建完整教程

本文从零开始，完成一条完整链路：

1. 建好 Python 环境，安装 **OpenBB**（开源金融数据平台）及常用公开数据源：美股/全球（yfinance）、美国与欧美宏观（FRED、ECB 等）和一批免 API key 的公开数据源；
2. 把这套 OpenBB 封装成 **MCP（Model Context Protocol）Server**；
3. 接入 **OpenAI Codex CLI**，让 Codex 直接调用金融数据。

MCP 传输方式采用 **stdio**：Codex 自己拉起进程，无需单独开终端、无需端口、无需 HTTPS，是最稳定的接法。

> 命令默认 macOS / Linux；Windows 把路径与 shell 命令做对应替换即可。

---

## 第一部分 · 安装 OpenBB 与常用数据源

### 1. 准备工具：uv、Python 3.12、Node.js、Codex CLI

**安装 uv**（Python 包与环境管理器，比 pip 快很多）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**安装 Python 3.12**：

```bash
uv python install 3.12
```

本教程推荐 Python 3.12，用于兼容 OpenBB 平台库和常用 provider 扩展。

**安装 Node.js 18 或更高**（Codex CLI 依赖 Node 运行）。已装可跳过，检查版本：

```bash
node --version    # 需 >= 18
```

**安装 Codex CLI**：

```bash
npm install -g @openai/codex
codex --version
```

> npm 上无 scope 的 `codex` 是另一个无关的老项目，**包名必须带 scope：`@openai/codex`**。

### 2. 创建虚拟环境

```bash
mkdir ~/openbb && cd ~/openbb
uv venv --python 3.12
source .venv/bin/activate
```

激活后命令行前会出现 `(.venv)` 字样。**后续所有 `uv pip` / `openbb` 操作都在这个激活状态下进行。**

> **中国大陆网络**：若安装缓慢或超时，在下面所有 `uv pip install` 后加上 `--index-url https://mirrors.aliyun.com/pypi/simple` 走阿里云镜像。

### 3. 安装 OpenBB 核心

```bash
uv pip install openbb
```

> 安装的是 `openbb`（Python 平台库），不是 `openbb-cli`。MCP Server 封装的正是这个平台库，必须装它。

核心会附带一组标准数据源，本教程基础路径用得到的有：

| 数据源 | 覆盖 | key |
|---|---|---|
| FRED | 美联储经济数据库 | 需免费 key（第 6 步配置） |
| Federal Reserve | 美联储 | 无 |
| SEC | 美国证监会 EDGAR 财报 | 无 |

### 4. 安装其余数据源（美股/全球、宏观及免 key 源）

一条命令装齐。所有列出的源**均无需 API key**（FRED 的 key 在第 6 步单独配）：

```bash
uv pip install \
  openbb-yfinance \
  openbb-ecb \
  openbb-imf \
  openbb-oecd \
  openbb-cboe \
  openbb-deribit \
  openbb-finviz \
  openbb-finra \
  openbb-tmx \
  openbb-famafrench \
  openbb-econdb \
  openbb-seeking-alpha
```

各源覆盖：

| 扩展 | 覆盖 | key |
|---|---|---|
| `openbb-yfinance` | 美股 / 全球股票 / ETF / 外汇（雅虎财经） | 免 |
| `openbb-ecb` | 欧洲央行 | 免 |
| `openbb-imf` | 国际货币基金组织 | 免 |
| `openbb-oecd` | 经合组织 | 免 |
| `openbb-cboe` | 美股期权 / 行情（Cboe） | 免 |
| `openbb-deribit` | 加密货币期权 | 免 |
| `openbb-finviz` | 选股 / 筛选 | 免 |
| `openbb-finra` | FINRA 监管数据 | 免 |
| `openbb-tmx` | 加拿大 TMX | 免 |
| `openbb-famafrench` | Ken French 因子库 | 免 |
| `openbb-econdb` | 宏观经济数据库 | 免 |
| `openbb-seeking-alpha` | 财经新闻 / 分析 | 免 |

### 5. 重建资源（让新数据源生效）

**这是一条不可省略的步骤。** OpenBB 的接口从已安装的扩展动态生成，每次增删数据源后都必须重建一次，否则在 Python 接口和 MCP 里看不到这些新源：

```bash
python -c "import openbb; openbb.build()"
```

### 6. 配置 FRED 的免费 key

FRED 是本教程验证宏观数据时需要的免费 key。key 写在 OpenBB 的本地配置文件 `~/.openbb_platform/user_settings.json` 中。

1. 打开 `https://fred.stlouisfed.org/docs/api/api_key.html`，注册并获取 API key；
2. 编辑 `~/.openbb_platform/user_settings.json`（文件不存在则新建），写入：

```json
{
  "credentials": {
    "fred_api_key": "粘贴你的key"
  }
}
```

> 这一个文件就是 OpenBB 读取 provider 凭据的地方。MCP Server 也会自动读它，后面无需在别处重复配置 FRED key。改完凭据无需重新 `openbb.build()`，但需要重启当前 Python / OpenBB MCP / Codex 会话，让进程重新读取配置。

### 7. 验证数据层

```bash
python - << 'PYEOF'
from openbb import obb

# 查看已安装的全部 provider（应能看到 yfinance / fred / ecb / cboe 等）
print(obb.coverage.providers)

# 美股 / 全球 -> yfinance
print(obb.equity.price.historical("AAPL", provider="yfinance").to_dataframe().tail())

# 美国宏观 -> fred
print(obb.economy.fred_series("GDP", provider="fred").to_dataframe().tail())
PYEOF
```

三项（provider 列表 + 两组取数）都正常返回，数据层即就绪。

---

## 第二部分 · 封装为 MCP 并接入 Codex

### 8. 安装 MCP Server（装在同一个 venv 里）

**关键点：MCP Server 必须装进上面这个带 yfinance 等扩展的 venv。** 若用 `uvx --from openbb-mcp-server` 那种临时环境，它只有核心 openbb，已安装的数据源扩展不会出现。

确认仍在激活状态（命令行有 `(.venv)`），然后：

```bash
uv pip install openbb-mcp-server
openbb-mcp --help
```

能打印出参数列表（`--transport`、`--host`、`--port` 等）即安装成功。

### 9. 取得 openbb-mcp 的绝对路径

Codex 拉起进程时**不会激活你的 venv**，因此配置里必须填**绝对路径**，不能填裸命令 `openbb-mcp`。

venv 激活状态下执行：

```bash
which openbb-mcp
```

输出形如：

```text
/Users/你的用户名/openbb/.venv/bin/openbb-mcp
```

**复制这一整行**，下一步要用。

### 10. 配置 Codex（`~/.codex/config.toml`）

Codex 的 MCP 配置全部写在 `~/.codex/config.toml`（CLI 与 VS Code 扩展共用此文件，TOML 语法错一处两边一起失效）。

文件不存在则先建：

```bash
mkdir -p ~/.codex
touch ~/.codex/config.toml
```

把下面这段追加进去，**将 `command` 替换为第 9 步复制的绝对路径**：

```toml
[mcp_servers.openbb]
command = "/Users/你的用户名/openbb/.venv/bin/openbb-mcp"
args = ["--transport", "stdio"]
startup_timeout_sec = 60
tool_timeout_sec = 120
```

逐字段说明：

| 字段 | 作用 |
|---|---|
| `command` | venv 中 openbb-mcp 的**绝对路径** |
| `args` | 使用 stdio 传输（Codex 经标准输入输出通信） |
| `startup_timeout_sec = 60` | **必填**。Codex 默认 MCP 启动超时仅 **10 秒**，OpenBB 加载多个数据源时可能超过，不调高会直接报 `timed out after 10 seconds` |
| `tool_timeout_sec = 120` | 单次工具调用超时，默认 60 秒；部分行情/财报查询较慢，给到 120 更稳 |

FRED key 不必写在这里，MCP Server 会自动读取第 6 步配置的 `user_settings.json`。如果刚刚修改过 key，重启 Codex 会话或 MCP server。

> **CLI 等价写法**（仅用于快速添加，超时参数仍需回到 toml 手动补）：
> ```bash
> codex mcp add openbb -- /Users/你的用户名/openbb/.venv/bin/openbb-mcp --transport stdio
> ```

### 11. 验证连接

启动一个 Codex 会话：

```bash
cd ~/openbb        # 或任意你要工作的项目目录
codex
```

在 Codex 中输入：

```text
/mcp
```

看到 `openbb` 服务器、状态为已连接、并列出工具数量，即接入成功。

也可直接询问确认能力：

```text
你能用 openbb 工具做什么？列出所有可用的数据类别。
```

### 12. 实际使用

OpenBB MCP 默认开启**工具发现机制**：启动时只暴露少量发现类工具（`available_categories`、`activate_tools` 等），Codex 会根据问题自动激活对应的数据工具再去取数。提问时点明数据源，命中更准。

**美股 / 全球（yfinance）：**

```text
用 openbb 取苹果（AAPL）近一年的价格与基本面，provider 用 yfinance。
```

**美国宏观（FRED）：**

```text
用 openbb 从 FRED 拉取美国 GDP 与 CPI 最近 10 年数据并做对比。
```

---

## 故障排查

**1. 报 `MCP client for openbb timed out after 10 seconds`**

没加或未生效 `startup_timeout_sec`。确认该行位于 `[mcp_servers.openbb]` 块之下，并把值提高到 `90` 或 `120`，重启 Codex。

**2. Codex 找不到命令 / 启动失败**

`command` 填成了裸命令 `openbb-mcp` 而非绝对路径。回到第 9 步用 `which openbb-mcp` 取绝对路径填入。先在终端单独运行那个绝对路径确认能启动。终端跑不起来，Codex 里必然跑不起来。

**3. 安装时依赖冲突 / openbb 被降级**

把核心与全部扩展合并成一条 `uv pip install` 命令重装，让解析器一次性求解版本。

**4. yfinance 等数据源的工具不出现**

装完扩展后没重建资源。回到 venv 重跑第 5 步：

```bash
cd ~/openbb && source .venv/bin/activate
python -c "import openbb; openbb.build()"
```

然后重启 Codex（stdio 模式下会重新拉起 server 并加载新源）。

**5. Codex 连上了却说“取不到数据”**

工具发现机制下需先激活工具。把提示写明确，如“**使用 openbb 工具**查询……”，或让它先列出类别再激活。

**6. TOML 语法错误导致 CLI 与 VS Code 同时失效**

检查：字符串均加双引号、数组用方括号 `["a", "b"]`、`env` 块须正确嵌套在 `[mcp_servers.openbb.env]` 下。拿不准用 TOML 校验器过一遍。

**7. 每次启动 Codex 都要等几秒**

stdio 模式每开一个会话都会重新拉起进程并 import OpenBB，属固有开销。嫌慢可改用常驻 HTTP 方式（见附录）。

---

## 附录：HTTP（streamable-http）常驻方式

适合不愿每次启动都等待 OpenBB 加载的场景：服务器常开常热，Codex 秒连，代价是需单独保持一个进程运行。

**第一步：从激活的 venv 启动服务器**（必须从 venv 运行，才会带上已安装的数据源扩展）

```bash
cd ~/openbb && source .venv/bin/activate
openbb-mcp --port 8001
```

控制台打印：

```text
Starting MCP server 'OpenBB MCP' with transport 'streamable-http' on http://127.0.0.1:8001/mcp
```

**第二步：Codex 配置改为 url 形式**

```toml
[mcp_servers.openbb]
url = "http://127.0.0.1:8001/mcp/"
startup_timeout_sec = 60
tool_timeout_sec = 120
```

结尾的斜杠 `/mcp/` 不能省。

**若连不上**：本地 `localhost` 的 http 一般可用（Codex 仅对**远程**服务器强制 HTTPS）；如仍连不上，在 `config.toml` 顶部启用 Rust MCP 客户端：

```toml
[features]
rmcp_client = true
```

---

## 一页速查（从零到通）

```bash
# ── 数据层 ──
curl -LsSf https://astral.sh/uv/install.sh | sh      # 装 uv
uv python install 3.12                                # 装 Python 3.12
node --version                                        # 确认 Node >= 18（Codex 需要）
npm install -g @openai/codex                          # 装 Codex CLI

mkdir ~/openbb && cd ~/openbb
uv venv --python 3.12 && source .venv/bin/activate    # 建并激活环境

uv pip install openbb                                 # 核心（含 FRED/SEC/Federal Reserve 等）
uv pip install openbb-yfinance openbb-ecb openbb-imf openbb-oecd \
  openbb-cboe openbb-deribit openbb-finviz openbb-finra openbb-tmx \
  openbb-famafrench openbb-econdb openbb-seeking-alpha
python -c "import openbb; openbb.build()"             # 重建资源（必做）
# 然后在 ~/.openbb_platform/user_settings.json 写入 fred_api_key

# ── MCP 层 ──
uv pip install openbb-mcp-server                      # 装 MCP（同一 venv）
which openbb-mcp                                      # 取绝对路径

# 写入 ~/.codex/config.toml：
#   [mcp_servers.openbb]
#   command = "<上面的绝对路径>"
#   args = ["--transport", "stdio"]
#   startup_timeout_sec = 60
#   tool_timeout_sec = 120

codex                                                 # 进会话后输入 /mcp 验证
```
