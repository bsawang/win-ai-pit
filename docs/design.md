---
title: 设计文档
_note: true
---

# 设计文档

## 背景

在 Windows 上使用 AI 助手时，模型倾向于给出 Unix 风格的答案，因为训练数据中 Unix/Linux 生态占主导。这不是某个模型的问题，而是整个 AI 训练数据生态的偏向。本项目作为一个"补偿层"，让 AI 在 Windows 环境下踩过的坑被结构化记录下来，供后续检索复用。

## 原则

| # | 原则 | 说明 |
|---|------|------|
| 1 | AI 优先 | 人和 AI 同时服务，优先保 AI 效率 |
| 2 | 低配置入职 | 适当配置但不绑定模型，Claude/DeepSeek/其他 AI 走一样流程 |
| 3 | 贡献无感 | AI 发现新坑时以最少的步骤记下来，即时或非即时提交 |
| 4 | 去重必须 | 同一条坑不记两次 |
| 5 | 自动验证 | 不依赖人工逐条判断，自动校验 |
| 6 | 细记录粗匹配 | 记录时如实记版本，查询时宽松匹配 |
| 7 | 本地/云端可选 | 同一套接口，两种适配器 |
| 8 | 版本标记 | 每条坑必须标记适用版本和环境，按环境自动过滤 |
| 9 | 模型通用 | 本质不是模型训练问题，是 Windows 环境差异问题 |

## 选型

### 框架：pyrite

基于 [pyrite](https://github.com/markramm/pyrite) (MIT) 构建。

**选择理由：**

| 需求 | pyrite 支持方式 |
|------|---------------|
| Markdown+YAML 存储 | 原生 |
| MCP 接口（AI 查/记） | 原生 |
| 全文搜索 + 语义搜索 | SQLite FTS5 + sqlite-vec |
| 自定义字段 | kb.yaml fields 配置 |
| 本地/云端部署 | stdio MCP / FastAPI |
| 插件机制 | 自定义 entry type + MCP 工具 |

**我们原创的部分：**
- Windows 坑的领域模型（症状、根因、解决、版本、严重程度）
- 版本匹配逻辑（按 OS/工具版本过滤）
- 去重逻辑（搜索已有条目比对标题/症状）
- `search_pitfall` / `record_pitfall` MCP 工具

### 集成方式：整包

pyrite 源码直接拷入本仓库，不通过 pip 依赖，不绑定 git submodule。上游有更新时手动 cherry-pick。

**保留的核心模块：** server/（MCP）、models/（数据模型）、schema/（配置解析）、storage/（SQLite 索引）、services/（搜索）、plugins/（插件机制）
**不保留：** web/（SvelteKit 前端）、extensions/（其他领域插件）、kb/（pyrite 自己的 KB）、docs/、tests/、migrations/

## 数据模型

### 核心概念

- **问题 = 主键** — 症状 + 根因 相同就是同一条坑，版本差异作为附属信息
- **frontmatter 用于 AI 匹配，body 用于 AI 阅读**
- **细记录粗匹配** — 记录时如实记版本，查询时宽松匹配

### 字段定义

```yaml
id:                    # 唯一 slug，去重引用用
title:                 # 简短标题，搜索命中显示
symptom:               # 现象描述，去重比对用
root_cause:            # 根因简述，去重比对用
environment:
  os: []               # 在哪个 OS 上观察到
  tool:                # 主要涉及的工具
  tool_versions: []    # 被验证过的工具版本
solution:              # 简要解法
severity:              # critical / medium / low
tags: []               # 自由标签
created:               # 创建日期
updated:               # 更新日期
```

### 版本处理

```
记录时细：
  os: [windows-10-22H2]       ← 只记这个版本
  tool_versions: [msys2-3.4.5]

匹配时粗：
  当前环境 win11-23H2, msys2
  → os 不冲突，tool 命中 → 展示（标注"win10验证，win11预计适用"）

版本差异写 body：
  ## 解决
  ### MSYS 1.x（已验证） → 解法 A
  ### MSYS2 3.x（已验证） → 解法 B
  ### MSYS2 最新版 → 已修复
```

## 实施状态

### 已就绪
- [x] 项目结构搭建（pyrite 核心源码已拷贝精简）
- [x] YAML 编码修复（UTF-8 支持中文）
- [x] kb.yaml 配置（windows_pitfall type）
- [x] 插件框架（pyrite_windows_pitfalls 包）
- [x] MCP 工具 search_pitfall（FTS5 + 工具/OS 过滤）
- [x] MCP 工具 record_pitfall（写入 + 基础去重）
- [x] 第一条示例坑（MSYS >nul）
- [x] 插件注册（entry points）
- [x] 许可证（MIT + pyrite 版权声明）
