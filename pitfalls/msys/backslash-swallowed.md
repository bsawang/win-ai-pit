---
id: msys-backslash-swallowed
title: MSYS 下反斜杠在命令行参数中被吞
type: windows_pitfall
symptom: 在 Git Bash 中执行 reg delete HKLM\Software\... /f 时，报"无效语法"错误
root_cause: MSYS DLL 将反斜杠 \ 解释为转义字符，在参数传递前将其吞掉或转换
environment:
  os: [windows-10, windows-11]
  tool: msys
  tool_versions: [msys2-3.4.x]
solution: 用 cmd //c 前缀绕过 MSYS 参数转换
severity: medium
tags: [msys, cmd, registry]
created: 2026-07-22
---

## 症状

在 Git Bash（MSYS2 环境）中执行注册表删除命令时：

```bash
reg delete HKLM\SOFTWARE\Classes\*\shell\xxx /f
```

报错：`无效语法` 或 `参数错误`

## 根因

MSYS 的 DLL 层会自动转换 Unix 风格的路径参数。反斜杠 `\` 在 MSYS
中被视为转义字符或路径分隔符，在传递给 Windows 原生程序前被 MSYS
预处理吞掉。`reg.exe` 收到的是已经被破坏的参数。

## 解决

在命令前加 `cmd //c` 绕过 MSYS 的参数转换：

```bash
cmd //c "reg delete HKLM\SOFTWARE\Classes\*\shell\xxx /f"
```

`//c` 告诉 MSYS 不要处理后面的参数，直接透传给 cmd.exe。

## 参考

- [[msys-nul-to-dev-null]] — MSYS 路径转换系列问题
