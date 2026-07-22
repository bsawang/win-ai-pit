---
id: msys-utf8-to-gbk
title: MSYS 下写出 UTF-8 中文到 cmd 环境变乱码
type: windows_pitfall
symptom: 在 Git Bash 中用 echo/printf 写出含中文的 .bat 文件，在 cmd.exe 中运行显示乱码
root_cause: MSYS 使用 UTF-8 编码，但 Windows 中文版 cmd.exe 默认使用 GBK 编码
environment:
  os: [windows-10, windows-11]
  tool: msys
  tool_versions: [msys2-3.4.x]
solution: 用 Python 二进制模式转 GBK 后再写出
severity: medium
tags: [msys, encoding, gbk, utf8, bat]
created: 2026-07-22
---

## 症状

在 Git Bash 中生成含中文的 .bat 文件：

```bash
echo 这是中文 > test.bat
```

该文件在 cmd.exe 中运行时中文字符显示为乱码，或执行报错。

## 根因

MSYS（Git Bash）终端默认使用 UTF-8 编码。但 Windows 中文版 cmd.exe
使用 GBK（代码页 936）。直接从 MSYS 写出 UTF-8 文本到文件后，
cmd.exe 用 GBK 解码自然乱码。

## 解决

### 方案一：Python 二进制模式转 GBK（推荐）

```python
# 用 Claude Code Write 工具先创建文件（UTF-8 + LF，不走 MSYS）
# 再用 Python 转 ANSI + CRLF
with open('file.bat', 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
gbk = text.encode('gbk')
gbk = gbk.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
with open('file.bat', 'wb') as f:
    f.write(gbk)
```

### 方案二：避免 MSYS 写出

直接在 cmd.exe 中创建文件，或在 VSCode 等非 MSYS 编辑器中保存为
ANSI/GBK 编码。

### 方案三：cmd 下临时切 UTF-8

不推荐，部分 Windows 命令不支持 UTF-8 代码页（65001）。

## 参考

- [[msys-nul-to-dev-null]] — MSYS 路径转换系列问题
