---
title: 开发模式 vs 运行模式
_note: true
---

# 开发模式 vs 运行模式

> 记录日期: 2026-07-23

## 两个本地目录，同一远程仓库

本项目存在两个本地目录指向同一个 GitHub 仓库 (`github.com/bsawang/win-ai-pit`)，但用途不同，不可混淆。

```
E:\work\ai\win-ai-pit          ← 开发模式（源码目录）
  ├── pyrite 源码
  ├── CLI 和 MCP 工具代码
  ├── 配置（kb.yaml）
  ├── 文档（docs/）
  └── 不应在此做数据推送

pip install windows-pitfalls     ← 运行模式（已安装到系统）
  ├── 命令: windows-pitfalls（PE 可执行文件）
  ├── 数据目录: ~/.windows-pitfalls/
  ├── MCP 调用: ~/.claude/scripts/pitfalls.sh 调的是这个
  └── 数据同步在此进行
```

## 操作边界

| 操作 | 应在开发项目 (E:\) | 应在运行目录 (~/.windows-pitfalls) |
|------|:-:|:-:|
| 改 pyrite 源码 | ✅ | ❌ |
| 写设计文档 | ✅ | ❌ |
| 更新 .claude.md | ✅ | ❌ |
| 改 MCP 工具 | ✅ | ❌ |
| 更新 auto-merge workflow | ✅ 改代码 | ❌ |
| 重新打包发布 | ✅ `pip install -e .` | ⚠️ `pip install --upgrade` |
| pitfalls.sh 记新坑 | ❌ | ✅ 自动化 add/ 分支 → PR → 合入 |
| 知识库 git commit/push | ❌ | ✅ 自动或手动 |
| 跑索引重建 | ❌ | ✅ `windows-pitfalls index` |
| 查看活动日志 | ❌ | ✅ `windows-pitfalls log` |

## 为什么指向同一个远程

- 开发项目推**代码**到 `master`
- `pip install windows-pitfalls` 是从 GitHub 安装的
- 运行目录 `~/.windows-pitfalls/` 是一个独立的 `git clone`，用于**数据同步**
- 两边 `origin` 相同，但职责不同

## 核心规则

```
⚠️ 开发项目：只推代码改动（master）
⚠️ 运行目录：只推数据（自动走 add/ 分支 → PR → 合入）
❌ 不要在两边的 master 上混着推，历史会交叉混乱
```

## 数据流示意图

```
您或 Claude
    │
    ├─ pitfalls.sh search → windows-pitfalls 命令 → ~/.windows-pitfalls/ 数据
    │
    └─ pitfalls.sh record → 写 .md → 重建索引
         → git commit (add/ 分支)
         → git push (add/ 分支)
         → gh PR → GitHub Actions auto-merge → master
         ↑
    所有操作在 ~/.windows-pitfalls/ 内完成，不涉及开发项目
```
