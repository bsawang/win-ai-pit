# Windows 避坑指南

Windows 用户在命令行执行：

```bash
git clone https://github.com/bsawang/win-ai-pit.git
cd win-ai-pit
install.bat
```

或手动按下方步骤操作。

AI 驱动的 Windows 开发/运维踩坑知识库。专门解决 AI 在 Windows 环境下给出 Unix 风格错误答案的问题。

## 核心理念

大部分 AI 模型的训练数据严重偏向 Linux/Unix 生态。当 AI 回答 Windows 问题时，会自然倾向于输出 Unix 风格的解决方案。本项目是一个"补偿层"——AI 在 Windows 环境下踩过的坑、被纠正过的知识，结构化记录下来，供以后任何 AI 检索复用。

## 架构

```
AI（Claude Code / DeepSeek 等）
    ↕ MCP 协议（stdio 或 HTTP）
pyrite MCP Server（本地进程）
    ↕
SQLite 索引（FTS5 全文搜索） ←→ Markdown 文件目录（Git 仓库）
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

## 安装

```bash
git clone https://github.com/bsawang/win-ai-pit.git
cd win-ai-pit

# 一键安装（Windows 用户双击 install.bat 也行）
pip install -e .
python scripts/setup.py
```

## 使用

### MCP Server（自动启动）

配好 `.claude/settings.json`（已自带），Claude Code 打开项目时自动拉起。

### MCP Server（手动启动）

```bash
python -m pyrite.server.mcp_server --tier admin
```

### MCP 工具

#### search_pitfall
搜索已知坑。支持按工具、OS、严重程度过滤。

#### record_pitfall
记录新坑。自动去重（按标题/症状相似度匹配），写文件后自动重建索引。

## 设计原则

1. **AI 优先** — 人和 AI 同时服务，优先保 AI 效率
2. **低配置入职** — 一次 `pip install`，不绑定模型
3. **贡献无感** — AI 发现新坑时自动记录，即时或非即时提交
4. **去重必须** — 同一条坑不记两次
5. **自动验证** — 不依赖人工逐条审核
6. **细记录，粗匹配** — 记录时如实记版本，查询时宽松匹配
7. **本地/云端可选** — 同一套接口，两种部署模式
8. **版本标记** — 每条坑必须标记适用版本和环境

## 许可证

MIT License。本仓库包含 [pyrite](https://github.com/markramm/pyrite) (MIT, Copyright (c) 2025-2026 markr) 的核心源码。
