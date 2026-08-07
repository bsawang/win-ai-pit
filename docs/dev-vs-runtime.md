---
title: 开发模式 vs 运行模式
_note: true
---

# 开发模式 vs 运行模式

> 记录日期: 2026-07-23 · 更新: 2026-08-07（双仓库拆分后）

## 架构（代码/数据分离）

```
win-ai-pit            ← 代码仓库（github.com/bsawang/win-ai-pit）
  pyrite 源码 + 插件 + kb.yaml（schema 权威源，包内）
  开发模式：clone 此仓库，改代码/文档，推 master

win-ai-pit-data       ← 数据仓库（github.com/bsawang/win-ai-pit-data）
  pitfalls/*.md 纯数据 + auto-merge workflow
  运行模式：clone 到 ~/.windows-pitfalls，记坑/查坑，走 add/ 分支 PR → 合入

两个仓库 remote 不同，物理隔离 —— 不再需要「不混推」纪律
```

## 操作边界

| 操作 | 应在代码仓库 (E:\work\ai\win-ai-pit) | 应在运行目录 (~/.windows-pitfalls) |
|------|:-:|:-:|
| 改 pyrite / 插件源码 | ✅ | ❌ |
| 写文档（design/.claude.md/README） | ✅ | ❌ |
| 改 kb.yaml（schema） | ✅（包内权威源，改完发布） | ❌（runtime 由 init 写入） |
| 记坑 / 查坑 | ❌ | ✅（pitfalls.sh → 数据仓库 add/ 分支 → PR → 合入） |
| 数据 git 同步 | ❌ | ✅（clone 数据仓库） |
| 重建索引 | ❌ | ✅ `windows-pitfalls index` |

## 安装 / 部署

```
pip install git+https://github.com/bsawang/win-ai-pit.git      # 代码（含 kb.yaml 模板）
git clone https://github.com/bsawang/win-ai-pit-data.git ~/.windows-pitfalls   # 数据
windows-pitfalls init       # 写入 kb.yaml（从包内）+ 建索引 + 配全局 MCP
```

`kb.yaml` 是运行时文件：init 从代码包内复制到 `~/.windows-pitfalls/kb.yaml`，**不属于数据仓库**（已 gitignore）。

## 一句话认知

```
代码仓库（win-ai-pit）  = 造轮子的（源码 + schema 定义）
数据仓库（win-ai-pit-data） = 纯数据副本 + PR 写入口，无任何控制逻辑
运行时（~/.windows-pitfalls）= clone 数据仓库，轮子跑起来的地方
```

详见 `docs/design.md` 的「部署架构：代码与数据分离」。
