---
title: 项目笔记
_note: true
---

# 项目笔记

> 自动维护，记录跨会话的讨论要点。不要手动删，AI 依靠这个恢复上下文。

## 当前状态 (2026-07-22)

Windows 踩坑知识库 MVP 阶段。基于 pyrite + MCP，本地存储。已完成项目结构、1 条示例坑、去重逻辑修复。存在 5 个已知问题（详见下方）。

## 已知问题

1. `search_pitfall` 没对特殊字符做 FTS5 转义，`>`, `/`, `-` 会报错
2. `docs/design.md` / `plan.md` / `notes.md` 缺 YAML frontmatter，索引时报错
3. 全局配置引用旧路径（已修复，需要确认）
4. 只有 1 条坑，内容不足

## 已决定的架构设计

**搜索→未命中→比对→fetch→pull→重搜→未命中→记** (见 `docs/plan.md`)
- 搜不到时才 git fetch 检查远程，有变化才 pull
- record_pitfall 写 .md + 重建索引 + git commit + push
- 不在发现问题时记，只在解决后一次性写入（症状+根因+方案全）

## 已讨论但未实施

- 云端存储方案（具体方案丢失，待重新讨论）
- 开发计划见 `docs/plan.md`

## 修复记录

| 日期 | 内容 |
|------|------|
| 2026-07-22 | 项目路径 windows-guide → win-ai-pit |
| 2026-07-22 | record_pitfall 去重修复：中文字符级拆分 + fallback 搜索 |
| 2026-07-22 | record_pitfall 写文件后自动重建索引 |
| 2026-07-22 | git init + 推送到 GitHub |
| 2026-07-22 | `scripts/setup.py` — 一键配置项目；`scripts/start-mcp.bat` — 启动脚本 |

## 当前已知问题

1. `search_pitfall` 没对特殊字符做 FTS5 转义，`>`, `/`, `-` 会报错
2. `docs/` 下的 .md 无 frontmatter，索引时报错
3. 只有 1 条坑

## 已确定的架构

**同步流程：** search 本地 → 未命中 → 比对去重 → 确实没有 → git fetch → 有变化才 pull → 重建索引 → 重搜 → 仍未命中 → record → commit+push

**存储：** 源码和坑数据在同一仓库，每人本机跑 MCP stdio，通过 Git 同步。不设远程 MCP 服务器。

**记录时机：** 只在解决问题后一次性写入（症状+根因+方案全），不记"待解决"坑。
