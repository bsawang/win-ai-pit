---
id: desktop-path-symlink
title: C:\\Users\\xxx\\Desktop 可能是空符号链接
type: windows_pitfall
symptom: 在 MSYS 或代码中访问 C:\\Users\\xxx\\Desktop 返回空或路径不存在
root_cause: Windows 将桌面路径重定向到非系统盘（如 D 盘），C 盘下的 Desktop 是空符号链接
environment:
  os: [windows-10, windows-11]
  tool: [msys, cmd, powershell]
solution: 用 PowerShell 命令 [Environment]::GetFolderPath('Desktop') 获取实际路径
severity: medium
tags: [filesystem, path, symlink, desktop]
created: 2026-07-22
---

## 症状

在 MSYS 或代码中访问用户桌面目录时：

```bash
ls -la /c/Users/bsawang/Desktop/
# 返回空或显示符号链接
```

实际文件存在但 Desktop 目录是空的。

## 根因

Windows 允许将用户文件夹（桌面、文档等）重定向到非系统盘。
当用户在系统安装后将桌面移到 D 盘时，`C:\Users\xxx\Desktop`
变成一个指向新位置的符号链接（reparse point），实际文件在
`D:\用户文件\桌面\` 下。

## 解决

### 获取实际桌面路径

```powershell
[Environment]::GetFolderPath('Desktop')
```

### 在脚本中正确处理

```python
import ctypes
from ctypes import wintypes

# Windows API 获取实际桌面路径
CSIDL_DESKTOP = 0x0000
buf = ctypes.create_unicode_buffer(260)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, 0, buf)
desktop = buf.value  # 返回实际路径
```

## 注意

在 MSYS 中 `C:\Users\xxx\Desktop` 路径可能可以通过 `/c/Users/xxx/Desktop`
访问，但该路径是空符号链接。AI 在生成文件路径时应优先使用
PowerShell 命令确认实际位置。
