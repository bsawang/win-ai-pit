# Windows 避坑指南 · 代码仓库

AI 驱动的 Windows 开发/运维踩坑知识库 —— **代码仓库**。坑数据在 [win-ai-pit-data](https://github.com/bsawang/win-ai-pit-data)，本仓库只含代码，不含坑内容。

## 架构：代码与数据分离

```
win-ai-pit          ← 本仓库（代码，pip 安装，只读）
  pyrite 源码 + windows-pitfalls 插件（search_pitfall / record_pitfall）

win-ai-pit-data     ← 数据仓库（git clone，唯一可写副本）
  pitfalls/*.md + kb.yaml
  部署位置：~/.windows-pitfalls
```

设计决策见 [docs/design.md](docs/design.md)。

## 安装

```bash
pip install git+https://github.com/bsawang/win-ai-pit.git      # 代码
git clone https://github.com/bsawang/win-ai-pit-data.git ~/.windows-pitfalls   # 数据
windows-pitfalls init                                          # 建索引
```

安装后打开**任何项目目录**的 Claude Code，MCP Server 自动启动。
其他 AI 工具需手动运行 `windows-pitfalls start`。

## 系统需求

- **操作系统** — Windows 10 / Windows 11
- **Python** — 3.11 或更高版本
- **Git** — 用于克隆数据仓库和同步坑数据
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

## 开发

- clone 本仓库改代码
- 单元测试用代码自带 fixture，不依赖数据仓库
- 集成测试连已安装 runtime 的真实数据（`~/.windows-pitfalls`）
- 坑数据不在本仓库，提交代码不会混入数据

## CLI 命令

| 命令 | 用途 |
|------|------|
| `windows-pitfalls init` | 首次初始化，创建 `~/.windows-pitfalls/` 索引 |
| `windows-pitfalls start` | 启动 MCP Server（一般被 Claude Code 自动调用） |
| `windows-pitfalls index` | 手动重建索引 |
| `windows-pitfalls log` | 查看 search / record 调用记录 |

## 组件

| 组件 | 说明 |
|------|------|
| **pyrite** | 知识库引擎，提供 MCP Server、SQLite 索引、Markdown 文件管理 |
| **windows-pitfalls 插件** | 自定义 MCP 工具（search_pitfall、record_pitfall）、领域逻辑 |

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
