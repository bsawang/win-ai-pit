---
id: registry-context-menu-locations
title: 右键菜单注册表位置大全
type: windows_pitfall
symptom: 清理右键菜单时找不到对应注册表位置，同个软件出现在多个路径下
root_cause: Windows 右键菜单分布在多个注册表路径，按作用域和类型分类，不同软件注册在不同位置
environment:
  os: [windows-10, windows-11]
  tool: [regedit, registry]
solution: 按优先级顺序逐一检查各注册表位置
severity: medium
tags: [registry, rightclick, reference]
created: 2026-07-22
---

## 症状

想要清理某个软件的右键菜单，只删了常见路径的注册表项，
但菜单仍然存在。软件可能在多个位置注册了菜单项。

## 根因

Windows 右键菜单分布在多个注册表路径，按文件和文件夹类型、
用户/系统范围、COM/non-COM 分类：

### 文件类型右键

| 路径 | 覆盖范围 | 常见软件 |
|------|---------|---------|
| `*\shellex\ContextMenuHandlers` | 所有文件 | QQ, 迅雷, WPS, 360 |
| `*\shell` | 所有文件（非COM） | 迅雷云盘, ToDesk |
| `AllFileSystemObjects\shellex\ContextMenuHandlers` | 所有文件系统对象 | QQ |

### 文件夹右键

| 路径 | 覆盖范围 | 常见软件 |
|------|---------|---------|
| `Folder\shellex\ContextMenuHandlers` | 文件夹图标 | QQ |
| `Directory\shellex\ContextMenuHandlers` | 文件夹图标 | 迅雷, 百度网盘 |
| `Directory\Background\shellex\ContextMenuHandlers` | 空白处右键 | WPS, 360 |
| `Directory\Background\shell` | 空白处右键（非COM） | AnyCode, 抖音 |

### 其他

| 路径 | 覆盖范围 | 常见软件 |
|------|---------|---------|
| `Drive\shellex\ContextMenuHandlers` | 磁盘驱动器 | 迅雷 |
| `HKCU\Software\Classes\*\shellex\ContextMenuHandlers` | 用户级文件 | WPS, 迅雷 |
| `HKCU\Software\Classes\*\shell` | 用户级文件（非COM） | 抖音 |

> 完整路径前缀：`HKLM\SOFTWARE\Classes\`

## 解决

按以下步骤排查：

1. 先用 reg query 查全部位置
2. 删完一批后重启 explorer 验证
3. 如果还在，查用户级（HKCU）位置
4. 如果还是不变，可能是服务动态注册

## 参考

- [[registry-special-char-keynames]] — 特殊字符键名
- [[explorer-cache-refresh]] — 重启 explorer 生效
- [[dynamic-service-registration]] — 服务动态注册
