# 中国市场 MCP 配置

本文件说明本仓库的 Codex MCP 配置方式。默认 MCP 入口统一保留在根级 [`.mcp.json`](./.mcp.json) 中，但是否可用取决于用户本地是否已经安装对应 MCP 服务、配置 token 并取得数据授权。

## 1. Codex 插件配置形态

Codex 插件通过根级 `plugin.json` 引用 MCP 配置：

```json
{
  "mcpServers": "./.mcp.json"
}
```

根目录下的 `.mcp.json` 使用以下结构：

```json
{
  "mcpServers": {
    "server-name": {
      "url": "http://127.0.0.1:8001/mcp"
    }
  }
}
```

本地 stdio 服务使用：

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["example-mcp-server"]
    }
  }
}
```

需要 token 的本地服务不得硬编码密钥，只能从环境变量读取：

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["-m", "example_server.main"],
      "env": {
        "EXAMPLE_TOKEN": "${EXAMPLE_TOKEN}"
      }
    }
  }
}
```

## 2. 默认保留的机构数据源

根级 `.mcp.json` 保留 Daloopa、Morningstar、S&P Global、FactSet、Moody's、MT Newswires、Aiera、LSEG、PitchBook、Chronograph 和 Egnyte 等默认 MCP 入口。

LSEG 同时保留通用入口 `lseg` 和原 `server-cl` 端点 `lseg-server-cl`。S&P Global 统一使用 `sp-global`，不再保留重复命名。

这些入口只代表插件知道如何连接相应服务；是否可用仍取决于用户本地网络、权限、认证和产品授权。

## 3. A 股/港股相关 MCP

根级 `.mcp.json` 默认加入以下国内市场入口：

| MCP | 覆盖场景 | Codex 配置 |
|---|---|---|
| `openbb-cn-market` | 多市场股票、宏观、基金和公开金融数据聚合，可覆盖 A 股、港股和美股相关场景 | HTTP：`http://127.0.0.1:8001/mcp` |
| `tushare-pro` | A 股行情、财务指标、公告、指数和部分宏观数据 | stdio：`python -m tushare_mcp_server.main`，需要 `TUSHARE_TOKEN` |
| `akshare-one` | A 股、港股、新闻、财务报表和公开市场数据补充 | stdio：`uvx akshare-one-mcp` |

OpenBB MCP 的官方文档说明，安装 `openbb-mcp-server` 后可使用 `openbb-mcp` 启动本地 HTTP MCP 服务，默认地址为 `http://127.0.0.1:8001`。

Tushare 和 AKShare 相关 MCP 属于开源或第三方封装。使用前必须由用户确认项目来源、安装方式、许可证、数据授权、token、频率限制和字段口径。

## 4. 使用原则

1. 用户先确认数据源授权、安装方式和 token。
2. 技能调用任何 MCP 前，必须确认该 MCP 在当前 Codex 会话中真实可用。
3. 在分析产物中写明 MCP 名称、数据日期、字段口径和限制。
4. 免费数据源只作辅助；监管、会计、KYC、基金文件和月结判断不得只依赖免费源。
5. MCP 不可用、字段缺失、口径不明或授权不确定时，输出必须写“需确认”。
