---
id: windows-cmd-vt-ansi
title: Windows cmd VT 默认关闭导致 ANSI 颜色码显示为字面乱码
type: windows_pitfall
importance: 5
metadata:
  type: windows_pitfall
  symptom: cmd 窗口跑输出 ANSI 颜色码的程序（ComfyUI 日志、uvicorn 等），启动初期颜色码显示为 [32m[INFO][0m 字面乱码，中途某个库启用 VT 后才正常。同一窗口开头乱码、后面正常。
  root_cause: Windows 10 cmd 的虚拟终端(VT)处理默认关闭（HKCU Console 无 VirtualTerminalLevel），ANSI 转义码不渲染显示为字面文本，直到某库中途 SetConsoleMode 启用 VT。
  solution: 设置 HKCU Console 的 VirtualTerminalLevel = 1 (REG_DWORD) 全局启用 VT，重开 cmd 后从第一行渲染。Git Bash 下 reg add 的斜杠参数会被 MSYS 转义，改用 PowerShell Set-ItemProperty。顺带解决 uvicorn 在 cmd 的颜色乱码。
  environment: &id001
    tool: cmd, console, ansi, vt
  severity: medium
symptom: cmd 窗口跑输出 ANSI 颜色码的程序（ComfyUI 日志、uvicorn 等），启动初期颜色码显示为 [32m[INFO][0m 字面乱码，中途某个库启用 VT 后才正常。同一窗口开头乱码、后面正常。
root_cause: Windows 10 cmd 的虚拟终端(VT)处理默认关闭（HKCU Console 无 VirtualTerminalLevel），ANSI 转义码不渲染显示为字面文本，直到某库中途 SetConsoleMode 启用 VT。
solution: 设置 HKCU Console 的 VirtualTerminalLevel = 1 (REG_DWORD) 全局启用 VT，重开 cmd 后从第一行渲染。Git Bash 下 reg add 的斜杠参数会被 MSYS 转义，改用 PowerShell Set-ItemProperty。顺带解决 uvicorn 在 cmd 的颜色乱码。
environment: *id001
severity: medium
---

## 症状

cmd 窗口跑输出 ANSI 颜色码的程序（ComfyUI 日志、uvicorn 等），启动初期颜色码显示为 [32m[INFO][0m 字面乱码，中途某个库启用 VT 后才正常。同一窗口开头乱码、后面正常。

## 根因

Windows 10 cmd 的虚拟终端(VT)处理默认关闭（HKCU Console 无 VirtualTerminalLevel），ANSI 转义码不渲染显示为字面文本，直到某库中途 SetConsoleMode 启用 VT。

## 解决

设置 HKCU Console 的 VirtualTerminalLevel = 1 (REG_DWORD) 全局启用 VT，重开 cmd 后从第一行渲染。Git Bash 下 reg add 的斜杠参数会被 MSYS 转义，改用 PowerShell Set-ItemProperty。顺带解决 uvicorn 在 cmd 的颜色乱码。

