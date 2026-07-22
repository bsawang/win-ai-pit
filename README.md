# Windows 避坑指南

AI 驱动的 Windows 开发/运维踩坑知识库。专门解决 AI 在 Windows 环境下给出 Unix 风格错误答案的问题。

## 安装

```bash
pip install git+https://github.com/bsawang/win-ai-pit.git
windows-pitfalls init
```

安装后打开 **任何项目目录** 的 Claude Code，MCP Server 自动启动。
其他 AI 工具需手动运行 `windows-pitfalls start`。

## 系统需求

- **操作系统** — Windows 10 / Windows 11
- **Python** — 3.11 或更高版本
- **Git** — 用于克隆仓库和同步坑数据
- **GitHub CLI `gh`** — 用于自动提 PR（记新坑时自动走 fork → PR → 合入）
- **Claude Code**（推荐）— 自动启动 MCP Server，其他 AI 工具需手动配置

## 使用说明

安装后正常用 AI 就行：

- **你** — 正常使用 AI，不需要为知识库做任何事
- **MCP 自动做** — 搜索已知坑、对比去重、记录新坑、提 PR 合入
- **不需要** — 手动管理文件、重建索引、敲命令

查看调用记录：

```bash
windows-pitfalls log
```

## MCP 工具

### search_pitfall
搜索已知坑。支持按工具、OS、严重程度过滤。

### record_pitfall
记录新坑。自动去重（按标题/症状相似度匹配），写文件后自动重建索引 + git commit + 提 PR。

## CLI 命令

| 命令 | 用途 |
|------|------|
| `windows-pitfalls init` | 首次初始化，创建 `~/.windows-pitfalls/` |
| `windows-pitfalls start` | 启动 MCP Server（一般被 Claude Code 自动调用） |
| `windows-pitfalls index` | 手动重建索引 |
| `windows-pitfalls log` | 查看 search / record 调用记录 |

## 架构

```
AI（Claude Code / DeepSeek 等）
    ↕ MCP 协议（stdio）
pyrite MCP Server（本地进程）
    ↕
SQLite 索引（FTS5 全文搜索） ←→ Markdown 文件目录（Git 仓库）
                                   ↕
                               GitHub（多人同步）
```

### 组件

| 组件 | 说明 |
|------|------|
| **pyrite** | 知识库引擎，提供 MCP Server、SQLite 索引、Markdown 文件管理 |
| **windows-pitfalls 插件** | 自定义 MCP 工具（search_pitfall、record_pitfall）、领域逻辑 |
| **pitfalls/** | 坑内容，Markdown + YAML frontmatter 格式 |
| **kb.yaml** | 知识库配置，定义 windows_pitfall 类型和字段 |

### 存储格式

每条坑一个 Markdown 文件，YAML frontmatter 存储结构化元数据，body 写详细内容：

```markdown
---
id: msys-nul-to-dev-null
title: MSYS 下 >nul 被转为 /dev/null
type: windows_pitfall
symptom: 在 Git Bash 中执行重定向命令时...
root_cause: MSYS DLL 拦截子进程文件写入...
environment:
  os: [windows-10, windows-11]
  tool: msys
  tool_versions: [msys2-3.4.x, msys-1.x]
solution: 脱离 MSYS 环境创建文件
severity: critical
tags: [msys, filesystem, encoding]
created: 2026-07-22
---

## 症状
...

## 根因
...

## 解决
...
```

## 贡献坑

任何人都能加坑——装好 `gh` 并登录后，`record_pitfall` 记坑时自动：

```
commit → push 分支 → gh pr create → GitHub Action 验证（只增不删）→ 自动合入 master
```

不需要 fork、不需要提 Issue、不需要等人审核。坑数据直接进库，下次别人 pull 就能搜到。

## 设计原则

1. **AI 优先** — 人和 AI 同时服务，优先保 AI 效率
2. **低配置入职** — 一次 `pip install`，不绑定模型
3. **贡献无感** — AI 发现新坑时自动记录，自动提 PR 合入
4. **去重必须** — 同一条坑不记两次
5. **自动验证** — 不依赖人工逐条审核
6. **细记录，粗匹配** — 记录时如实记版本，查询时宽松匹配
7. **本地/云端可选** — 同一套接口，两种部署模式
8. **版本标记** — 每条坑必须标记适用版本和环境

## 许可证

MIT License。本仓库包含 [pyrite](https://github.com/markramm/pyrite) (MIT, Copyright (c) 2025-2026 markr) 的核心源码。
