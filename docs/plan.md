---
title: 开发计划
_note: true
---

# 开发计划

## 数据流与同步架构

```
search 本地索引
    ├─ 命中 → 给方案
    │
    └─ 未命中 → 比对本地已有条目（去重检测）
         │
         ├─ 发现已有 → 不用记
         │
         └─ 确实没有 → git fetch（轻量检查）
              │
              ├─ 无变化 → record_pitfall 记新坑
              │             │
              │             └─ 写 .md → 重建索引 → git add/commit/push
              │
              └─ 有变化 → git pull → 重建索引 → 重搜
                   │
                   ├─ 搜到了 → 给方案
                   │
                   └─ 还是没有 → record_pitfall 记新坑
                                   │
                                   └─ 写 .md → 重建索引 → git add/commit/push
```

**核心规则：**
1. `git fetch` 做轻量检查，只有远程有变化时才 `pull`
2. 记新坑后自动 commit + push，别人立刻可见
3. 不记"待解决"坑，只在解决问题后一次性写入（症状+根因+方案全）

## 阶段一：基础完善（当前 → MVP）

### P0 - 核心功能补缺

- [ ] **search_pitfall 使用 sanitize_fts_query**
  - 目前 `search_pitfall` 直接把用户输入传给 FTS5，特殊字符（`>`, `/`, `-`）会报错
  - 修复：调用 `SearchService.sanitize_fts_query(query)` 后再搜索
- [ ] **search_pitfall 接口也做中文友好**
  - 跟 `record_pitfall` 类似，中文 query 需要适当处理
- [ ] **重建索引自动化**
  - 目前重建索引需要手敲一大段 python 命令
  - 方案：写一个 CLI 命令 `pyrite-reindex` 或 make / fab 任务

### P1 - 坑内容扩充

- [ ] **收录已有 Windows 踩坑经验**
  - encoding/ 目录：CMD/PowerShell 中文编码问题
  - filesystem/ 目录：NTFS 大小写敏感、长路径限制
  - registry/ 目录：注册表操作注意事项
  - services/ 目录：Windows 服务管理相关
- [ ] **补充各坑的 severity 分级和版本标记**
- [ ] **给现有坑补充参考链接和验证步骤**

### P2 - 使用体验

- [ ] **启动脚本** — 一键启动 MCP Server 的 `.bat`/`.sh`
- [ ] **验证去重在真实场景下生效** — 用相似问题反复测试
- [ ] **编写 MCP Server 的 Claude Code 配置指南**
  - 让 Claude Code 自动调用 `search_pitfall` + `record_pitfall`

---

## 阶段二：智能增强

- [ ] **语义搜索** — 集成 sqlite-vec，支持语义相似度匹配
  - 解决 FTS5 对短词/同义词/英文拼写变体的局限性
  - 需要 sentence-transformers 模型（已列为 optional dependency）
- [ ] **去重升级** — 结合语义相似度做更准确去重
  - 当前基于词重叠，语义搜索能发现"写文件失败"和"文件写入报错"的相似性
- [ ] **自动验证** — 新增坑时自动检查 solution 是否能跑通
  - 用 CI 在 Windows sandbox 中验证命令
- [ ] **query 扩展** — 自动纠正常见的 Windows/Unix 术语混淆
  - 如用户搜 "bash" 时也匹配 "Git Bash"、"msys"

---

## 阶段三：生态建设

- [ ] **跨 AI 适配**
  - 当前假设通过 MCP 协议调用，验证 DeepSeek / GLM 等也能用
  - 如果对方不支持 MCP，提供 REST API 备选
- [ ] **坑贡献工作流**
  - 非 AI 用户手动提 PR 的模板和指南
  - 自动检查 frontmatter 格式的 CI 脚本
- [ ] **统计与反馈**
  - 记录每条坑的命中次数
  - 用户反馈"这条没用"→ 自动降低排序权重
- [ ] **Web UI**
  - 提供一个简单的本地页面浏览/搜索/记录坑
  - pyrite 自带 FastAPI server，可以直接复用

---

## 阶段四：规模化

- [ ] **多知识库支持**
  - 区分 Windows 版本（Win10 / Win11 / Server）
  - 按工具领域分库（DevOps / 开发 / 运维）
- [ ] **社区共享**
  - 公共坑订阅源
  - 贡献者排行榜
- [ ] **自动爬坑**
  - 监控 AI 对话日志，自动提取新的 Windows 踩坑模式

---

## 优先级建议

```
现在做：阶段一 P0（搜索修复 + 重建索引脚本）
接着做：阶段一 P1（收录更多坑）
然后做：阶段一 P2（启动脚本 + MCP 集成指南）
有余力：阶段二（语义搜索 + 去重升级）
```
