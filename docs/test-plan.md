---
title: 测试计划
_note: true
---

# 测试计划

## 测试结果 (2026-07-22)

| 测试 | 状态 | 说明 |
|------|------|------|
| T1 代码验证 | ✅ | 全部通过 |
| T2 本地安装 | ✅ | 全部通过 |
| T3 完整安装流程 | ✅ | 全部通过 |
| T4 MCP 功能 | ✅ | 全部通过 |
| T5 Git 同步 | ✅ | 全部通过 |

## T1: 代码验证

- [ ] 插件模块 import 正常
- [ ] CLI 模块 import 正常
- [ ] `sanitize_fts_query` 能处理 `>`, `/`, `-` 等特殊字符

## T2: 本地安装

- [ ] `pip install .` 成功
- [ ] `windows-pitfalls --help` 显示子命令
- [ ] `windows-pitfalls start --help` 显示参数

## T3: 完整安装流程（模拟新用户）

- [ ] `pip install` 从 GitHub 或本地装
- [ ] `windows-pitfalls init` 成功（clone + 索引 + Claude 配置）
- [ ] 检查 `~/.windows-pitfalls/` 结构和内容
- [ ] 检查 `~/.pyrite/config.yaml` 路径正确
- [ ] 检查 `~/.claude/settings.json` 包含 MCP 配置
- [ ] 检查索引中有坑

## T4: MCP 功能

- [ ] MCP Server 启动无报错
- [ ] search 正常关键词返回结果
- [ ] search 特殊字符（`>nul`）不报错
- [ ] search 不存在的词触发 git fetch（不会崩即可）
- [ ] record 新坑成功
- [ ] record 重复标题触发去重
- [ ] record 后索引更新，能搜到刚记的坑

## T5: Git 同步

- [ ] `record_pitfall` 后 `~/.windows-pitfalls/` 下有 git commit
- [ ] commit message 包含坑标题
- [ ] 正常推送到 remote
- [ ] 搜索没命中时触发 git fetch（不崩即可）
