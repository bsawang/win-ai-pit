# Claude Code VSCode 扩展兼容性研究报告

> 研究日期: 2026-07-23
> 环境: VSCode + Claude Code 扩展 + 第三方 API 代理 (DeepSeek via `ANTHROPIC_BASE_URL`)

## 一、架构背景

### 两种工作模式

```
模式 A：CLI 模式（终端运行 claude）
  Claude Code CLI → 本地后端进程 → 远程 API
                       ├── 读取 settings.json
                       ├── 启动 mcpServers（stdio 子进程）
                       ├── 执行 hooks（Bash 子进程）
                       └── 维护 MCP 通信
                    ✅ 所有功能正常

模式 B：VSCode 扩展模式（当前使用）
  VSCode 扩展 → WebSocket → 远程 API（无本地后端进程）
                             ├── settings.json 仅读取 env/permissions
                             ├── mcpServers ❌ 不启动
                             ├── hooks ❌ 不执行
                             └── CLAUDE.md ✅ 由我遵守
```

### 关键发现

VSCode 扩展通过 `transport: "ws"`（WebSocket）直接连接远程 API，**没有本地的 Claude Code 后端进程**。所有需要本地子进程的功能（mcpServers、hooks）都不可用。

## 二、各项功能兼容性

| 功能 | CLI 模式 | VSCode 扩展 | 原因 |
|------|---------|------------|------|
| `settings.json env` | ✅ | ✅ | 纯配置，不依赖进程 |
| `settings.json permissions` | ✅ | ✅ | 纯配置 |
| `settings.json statusLine` | ✅ | ✅ | 由扩展执行 |
| `settings.json mcpServers` | ✅ 自动启动 | ❌ 不生效 | 需要本地后端 spawn 子进程 |
| `settings.json hooks` | ✅ 自动触发 | ❌ 不生效 | 需要本地后端执行 |
| `.mcp.json` | ✅ | ❌ 不生效 | 同样依赖本地后端 |
| `CLAUDE.md` 指令 | ✅ | ✅ | 由 LLM 遵守，无关进程 |
| WebSearch / Bash 工具 | ✅ | ✅ | 由扩展执行或发起 HTTP 请求 |

### MCP 服务器为什么不能自动启动

```javascript
// extension.js 中相关代码（简化的伪代码）
if (mcpServers 存在) {
  claude_args.push("--mcp-config", JSON.stringify({ mcpServers }))
}
// 这行代码只在 spawn 本地后端时执行
// 在 WebSocket 模式下，没有 spawn 过程，所以 mcpServers 被忽略
```

### Hook 为什么不能自动执行

同样的原因——hooks 配置被传递给本地后端进程，但 WebSocket 模式下没有这个进程。

## 三、传输协议

通过分析 VSCode 扩展的 lock 文件：

```json
{
  "transport": "ws",
  "ideName": "Visual Studio Code"
}
```

### WebSocket 模式特征

- 扩展通过 WebSocket 直连远程 API
- 所有工具（Read/Write/Bash/Grep 等）在扩展宿主进程中执行
- LLM 调用直接发往远程 API
- 没有中间后端进程

### stdio 模式特征（CLI）

- Claude Code CLI 启动本地后端进程
- 后端进程通过 stdio 与扩展/CLI 通信
- 后端进程负责 spawn 子进程（MCP、hooks 等）

## 四、CLAUDE.md 指令是唯一可靠的自动化手段

因为 mcpServers 和 hooks 在 VSCode 扩展模式下都不可用，**唯一能让 Claude 自动执行某些操作的机制是 CLAUDE.md 指令**。

### 指令的优缺点

| 方面 | 说明 |
|------|------|
| ✅ 所有模式生效 | CLI 和 VSCode 扩展都加载 |
| ✅ 所有项目可配 | 全局 `~/.claude/CLAUDE.md` + 项目 `.claude.md` |
| ✅ 指令足够强时可靠 | "必须"级指令大部分情况会被遵守 |
| ❌ 不是强制触发 | 复杂多步骤任务可能漏执行 |
| ❌ 不是实时响应 | 不能像 hook 那样在工具执行后即时触发 |
| ❌ 无法绑定特定事件 | 指令是通用的，不能做"当 X 发生时自动 Y" |

## 五、实际可用的替代方案

### 5.1 stdio MCP → Bash 包装脚本

```bash
# 示例：firecrawl.sh / pitfalls.sh
# 原理：每次启动 MCP 服务器 → 发请求 → 拿结果 → 退出
python -c "
  import subprocess, json
  proc = subprocess.Popen(['mcp-server', 'start'], ...)
  proc.stdin.write(初始化握手)
  proc.stdin.write(tools/call 请求)
  result = proc.stdout.read(响应)
  proc.kill()
"
# 优点：VSCode 扩展模式下可用
# 缺点：每次调用需要 1-3 秒启动时间
# 适用：低频调用（搜索/记录知识库）
```

### 5.2 HTTP MCP → 直接 curl

```bash
# 适用：远程 HTTP MCP 服务（如 Firecrawl）
curl -s -X POST "https://mcp-server.example.com/v2/mcp" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",...}'
# 优点：无需本地进程，延迟低
# 缺点：要求 MCP 服务提供 HTTP 接口
```

### 5.3 纯 Bash 脚本（无 MCP）

```bash
# 适用：简单操作的本地工具
# 直接通过命令行调用，不经过 MCP 协议
```

## 六、当前 setup 的最佳实践

基于以上研究，对于需要"系统级自动生效"的 Windows 避坑知识库：

```
自动化方案
├── setup: ~/.claude/settings.json（全局）
│   ├── mcpServers: windows-pitfalls → ❌ VSCode 不生效
│   └── env/permissions → ✅ 生效
│
├── setup: ~/.claude/CLAUDE.md（全局指令）
│   └── "遇到 Windows 问题必须先查后记" → ✅ 生效（强指令）
│
├── setup: pitfalls.sh（bash 包装脚本）
│   ├── search → 每次启动 MCP → 查 → 退出
│   └── record → 写.md → 重建索引 → git commit → push → PR
│
├── setup: GitHub Actions（CI/CD）
│   └── auto-merge-pitfalls.yml → ✅ 生效（云端，无关本地）
│
└── 未来方向
    └── 加入本地模式（CLI）作为补充手段
        └── 需要 MCP 自动启动时，用 claude 命令
```

## 七、未来改进方向

### 短中期（当前架构下可行）

1. **完整测试 CLI 模式** — 确认 `claude` 终端命令下 mcpServers 和 hooks 都正常
2. **优化包装脚本性能** — 减少每次 MCP 调用的启动时间
3. **扩展 pitfalls.sh** — 增加更多工具的直接支持
4. **CLAUDE.md 指令持续优化** — 根据漏执行的情况加强措辞

### 中长期（需要架构改变）

1. **VSCode 扩展支持本地 MCP 桥接** — 扩展的 feature request
2. **切换回标准 Anthropic API** — 使用官方 API + 本地 Claude Code 后端，mcpServers 和 hooks 全部生效
3. **自建 MCP HTTP Gateway** — 将 stdio MCP 服务通过 HTTP 暴露给 VSCode 扩展

## 八、验证要点

部署任何新功能前，必须在 VSCode 扩展模式下验证：

```
① 是否依赖本地后端进程？ → 很可能不生效
② 是否只依赖 CLAUDE.md 指令？ → 生效
③ 是否通过 Bash/HTTP 直接调用？ → 生效
④ 是否在 CLI 模式下运行？ → 生效
```

编写日期: 2026-07-23
