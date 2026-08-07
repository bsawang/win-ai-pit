---
id: pyrite-gitservice-subprocess-text-true-gbk
title: pyrite GitService subprocess text=True 在 GBK 系统解码中文分支名崩溃
type: windows_pitfall
importance: 5
metadata:
  type: windows_pitfall
  symptom: kb_push 推送含中文的分支名时报 NoneType object has no attribute strip（error_code=INTERNAL, retryable=true），但 git push 实际已成功、PR 也能正常创建
  root_cause: GitService.push 的 subprocess.run(capture_output=True, text=True) 用系统 locale(GBK) 解码 git 输出的 UTF-8 中文，reader thread 崩溃导致 stdout/stderr 变 None，随后 .strip() 抛异常
  solution: 脚本或环境设 PYTHONUTF8=1（UTF-8 模式）让 subprocess text 解码走 UTF-8；库内应显式 subprocess.run(..., encoding=utf-8, errors=replace) 根治
  environment: &id001
    tool: python
  severity: low
symptom: kb_push 推送含中文的分支名时报 NoneType object has no attribute strip（error_code=INTERNAL, retryable=true），但 git push 实际已成功、PR 也能正常创建
root_cause: GitService.push 的 subprocess.run(capture_output=True, text=True) 用系统 locale(GBK) 解码 git 输出的 UTF-8 中文，reader thread 崩溃导致 stdout/stderr 变 None，随后 .strip() 抛异常
solution: 脚本或环境设 PYTHONUTF8=1（UTF-8 模式）让 subprocess text 解码走 UTF-8；库内应显式 subprocess.run(..., encoding=utf-8, errors=replace) 根治
environment: *id001
severity: low
---

## 症状

kb_push 推送含中文的分支名时报 NoneType object has no attribute strip（error_code=INTERNAL, retryable=true），但 git push 实际已成功、PR 也能正常创建

## 根因

GitService.push 的 subprocess.run(capture_output=True, text=True) 用系统 locale(GBK) 解码 git 输出的 UTF-8 中文，reader thread 崩溃导致 stdout/stderr 变 None，随后 .strip() 抛异常

## 解决

脚本或环境设 PYTHONUTF8=1（UTF-8 模式）让 subprocess text 解码走 UTF-8；库内应显式 subprocess.run(..., encoding=utf-8, errors=replace) 根治

