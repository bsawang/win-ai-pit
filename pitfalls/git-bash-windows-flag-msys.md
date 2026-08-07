---
id: git-bash-windows-flag-msys
title: Git Bash 调 Windows 原生命令 /flag 参数被 MSYS 路径转换篡改
type: windows_pitfall
importance: 5
metadata:
  type: windows_pitfall
  symptom: whoami /groups、cmd /c "whoami /groups" 等调用 Windows 原生命令时，/groups /user /c 等以斜杠开头的参数被转成 C:/Program Files/Git/groups，报「无效选项/参数」；错误输出还是 GBK 编码显示为乱码
  root_cause: MSYS2/Git Bash 自动路径转换(Path Conversion)把所有 / 开头参数当相对路径转成 Windows 绝对路径，Windows 原生命令收到错误参数
  solution: 调用前加前缀 MSYS_NO_PATHCONV=1 禁用转换，例：MSYS_NO_PATHCONV=1 /c/Windows/System32/whoami.exe /groups；不要用 GNU 版 whoami(无 /groups 选项) 也不要用 cmd /c 包裹
  environment: &id001
    tool: bash
  severity: medium
symptom: whoami /groups、cmd /c "whoami /groups" 等调用 Windows 原生命令时，/groups /user /c 等以斜杠开头的参数被转成 C:/Program Files/Git/groups，报「无效选项/参数」；错误输出还是 GBK 编码显示为乱码
root_cause: MSYS2/Git Bash 自动路径转换(Path Conversion)把所有 / 开头参数当相对路径转成 Windows 绝对路径，Windows 原生命令收到错误参数
solution: 调用前加前缀 MSYS_NO_PATHCONV=1 禁用转换，例：MSYS_NO_PATHCONV=1 /c/Windows/System32/whoami.exe /groups；不要用 GNU 版 whoami(无 /groups 选项) 也不要用 cmd /c 包裹
environment: *id001
severity: medium
---

## 症状

whoami /groups、cmd /c "whoami /groups" 等调用 Windows 原生命令时，/groups /user /c 等以斜杠开头的参数被转成 C:/Program Files/Git/groups，报「无效选项/参数」；错误输出还是 GBK 编码显示为乱码

## 根因

MSYS2/Git Bash 自动路径转换(Path Conversion)把所有 / 开头参数当相对路径转成 Windows 绝对路径，Windows 原生命令收到错误参数

## 解决

调用前加前缀 MSYS_NO_PATHCONV=1 禁用转换，例：MSYS_NO_PATHCONV=1 /c/Windows/System32/whoami.exe /groups；不要用 GNU 版 whoami(无 /groups 选项) 也不要用 cmd /c 包裹

