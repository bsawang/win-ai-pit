---
id: explorer-cache-refresh
title: 修改注册表后右键菜单不变，需重启 explorer
type: windows_pitfall
symptom: 删除了注册表中的右键菜单项，但实际右键菜单没有变化
root_cause: Windows Explorer 缓存了注册表状态，修改后不自动刷新
environment:
  os: [windows-10, windows-11]
  tool: [regedit, explorer]
solution: 重启 explorer.exe 清除缓存
severity: low
tags: [registry, explorer, cache, cleanup]
created: 2026-07-22
---

## 症状

修改或删除注册表中的右键菜单项后，在桌面或文件资源管理器中
右键仍然看到旧的菜单项。

## 根因

Windows Explorer（explorer.exe）在启动时加载右键菜单注册表项
并缓存。修改注册表后，explorer 不会自动重新加载，需要重启
才能看到变更。

## 解决

重启 explorer.exe 清除缓存：

```cmd
taskkill /f /im explorer.exe && start explorer.exe
```

或者重启电脑。

## 注意

- 部分软件的右键菜单（如 Everything）由服务动态注册，重启 explorer
  后如果服务仍在运行，菜单会重新出现。需要配合停服务处理。
- 建议分批修改注册表：删一批 → 重启 explorer → 让用户确认 →
  再删下一批，避免一次删太多出问题难以定位。

## 参考

- [[dynamic-service-registration]] — 服务动态注册导致的问题
