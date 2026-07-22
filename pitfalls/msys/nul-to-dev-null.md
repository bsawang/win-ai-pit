---
id: msys-nul-to-dev-null
title: MSYS 下 >nul 被转为 /dev/null
type: windows_pitfall
symptom: |
  在 Git Bash 中执行类 Unix 的重定向命令时，nul 被意外的替换为 /dev/null，
  导致本应丢弃的输出写入了意料之外的文件。
root_cause: MSYS DLL 拦截子进程中的文件写入操作，将 "nul" 字符序列自动替换为
  "/dev/null"，这是 MSYS 路径转换机制的副作用。
environment:
  os:
    - windows-10
    - windows-11
  tool: msys
  tool_versions:
    - msys2-3.4.x
    - msys-1.x
solution: |
  脱离 MSYS 环境创建文件。最可靠的方式是用脱离 MSYS 的工具
  （如 Claude Code Write 工具）直接创建文件。
severity: critical
tags:
  - msys
  - filesystem
  - encoding
created: 2026-07-22
updated: 2026-07-22
---

## 症状

在 Git Bash（MSYS2 环境）中执行以下命令时：

```bash
cmd /c "echo hello >nul world"
```

期望结果是向 `nul`（空设备）输出，实际却创建了一个名为 `world` 的文件，
内容为 `hello >/dev/null`。

## 影响范围

以下方式全部踩坑验证：

- `cmd /c "echo ^>nul text"` ❌
- `powershell Set-Content -Encoding Default` ❌
- `python open('w', encoding='gbk')` ❌
- `python open('wb') + b'>nul'` ❌（连 bytes 都改）

## 根因

MSYS 的 DLL 层会自动将 Windows 路径概念转换为 Unix 风格。`nul` 作为
Windows 的空设备，在 MSYS 的映射表中被关联到 `/dev/null`。
当 MSYS 检测到子进程的输入输出中包含 `nul` 时，会将其替换为 `/dev/null`，
但此替换在处理普通文件写入时也会发生，造成了非预期的行为。

## 解决

### 方案一：脱离 MSYS 环境（推荐）

使用不经过 MSYS DLL 的工具创建文件。例如用 Claude Code 的 Write 工具，
或者用 VSCode 直接编辑文件。

```python
# 唯一可靠的绕过方式
with open('file.txt', 'wb') as f:
    f.write(b'hello >nul world')
```

<!-- 注意：以下 Python 代码必须在非 MSYS 环境（如 cmd 直接运行）下执行 -->

### 方案二：如果必须在 MSYS 下操作

可以用临时文件绕过：

```bash
# 将输出先写到一个临时文件
echo hello > tmp.txt
# 再复制到目标位置，避免直接操作 nul
```

### 版本更新

MSYS2 的最新版本（2024+）已部分修复此问题，但建议仍采用方案一以确保兼容性。

## 参考

- [MSYS 路径转换](/pitfalls/msys/path-conversion)
