---
id: dynamic-service-registration
title: 软件右键菜单由服务动态注册，改注册表后需停服务
type: windows_pitfall
symptom: 删除了注册表中的右键菜单项，但重启 explorer 后菜单又出现了
root_cause: 软件（Everything、鲁大师 DeepSearch 等）由后台服务运行时动态注册右键菜单，删除注册表后被服务重新写入
environment:
  os: [windows-10, windows-11]
  tool: [everything, regedit]
solution: 删除注册表项的同时停掉对应后台服务
severity: medium
tags: [registry, services, cleanup, rightclick]
created: 2026-07-22
---

## 症状

右键菜单清理步骤如下，但菜单项仍然存在：

1. 删除注册表 `HKLM\...\ContextMenuHandlers\xxx`
2. 重启 explorer.exe
3. 右键菜单依然出现

## 根因

部分软件（Everything、鲁大师 DeepSearch 等）的右键菜单不是直接
写在注册表中，而是由它们的后台服务（常驻进程）在运行时动态注册。
即使手动删除了注册表项，服务进程检测到后会重新写入。

## 解决

删除注册表项后，还需要停掉对应的后台服务：

```cmd
taskkill /f /im Everything.exe
net stop Everything
```

或者在软件本身的设置界面中关闭"集成到右键菜单"选项。

## 验证

删除 + 停服务后，重启 explorer 验证菜单是否消失。如果还在，
说明软件有其他注册机制（如开机自启重新注册）。
