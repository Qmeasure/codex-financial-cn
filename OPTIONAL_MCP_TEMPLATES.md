# 中国市场 MCP 配置

本文件说明本仓库的可选 Codex MCP 配置方式。默认安装 `financial-services-cn` 时只加载技能；根目录不提供 `.mcp.json`，避免 Codex 自动扫描和初始化 MCP。可选入口保存在 [`OPTIONAL_MCP_SERVERS.json`](./OPTIONAL_MCP_SERVERS.json)，只作为用户确认授权、登录和本地服务可用后的配置模板。

## 1. Codex 插件配置形态

Codex 插件的默认 `plugin.json` 不引用 MCP 配置，避免安装后自动初始化付费机构源或本地服务。需要启用数据源时，用户应按自己的授权范围把对应 MCP entry 加入个人 Codex MCP 配置，或在机构 marketplace 中发布单独的数据源插件。

可选 MCP 模板使用以下结构：

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

## 2. 可选机构数据源模板

`OPTIONAL_MCP_SERVERS.json` 保留 Daloopa、Morningstar、S&P Global、FactSet、Moody's、MT Newswires、Aiera、LSEG、PitchBook、Chronograph 和 Egnyte 等可选 MCP 入口。

LSEG 同时保留通用入口 `lseg` 和原 `server-cl` 端点 `lseg-server-cl`。S&P Global 统一使用 `sp-global`，不再保留重复命名。

这些入口只代表插件知道如何连接相应服务；是否可用仍取决于用户本地网络、权限、认证和产品授权。

## 3. A 股/港股相关 MCP

`OPTIONAL_MCP_SERVERS.json` 保留以下国内市场入口模板：

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
5. MCP 不可用、字段缺失、口径不明或授权状态不清时，只记录未覆盖数据项，不得输出固定缺口标签。
