---
id: ultraedit-folder-shellex
title: UltraEdit 文件夹菜单藏在 Folder\shellex 下
type: windows_pitfall
tags:
- registry
- context-menu
- UltraEdit
- Folder
- shellex
importance: 5
metadata:
  type: windows_pitfall
  symptom: 文件夹右键菜单出现"在 %s 中打开文件夹"项，%s未替换，注册表在 *\shellex 和 Directory\shell 中找不到，实际藏在 HKCU\Folder\shellex\ContextMenuHandlers\UltraEdit。
  root_cause: COM组件注册的shell扩展可能挂在 Folder 类下而非通用的 Directory 或 * 路径。Folder\shellex 是最容易被忽略的右键菜单注册位置。
  solution: 文件夹右键菜单查不全时要检查：HKLM和HKCU下的 Folder\shellex 位置。
  environment: &id001
    os:
    - Windows 10/11
    tool: reg, regedit
  severity: low
symptom: 文件夹右键菜单出现"在 %s 中打开文件夹"项，%s未替换，注册表在 *\shellex 和 Directory\shell 中找不到，实际藏在 HKCU\Folder\shellex\ContextMenuHandlers\UltraEdit。
root_cause: COM组件注册的shell扩展可能挂在 Folder 类下而非通用的 Directory 或 * 路径。Folder\shellex 是最容易被忽略的右键菜单注册位置。
solution: 文件夹右键菜单查不全时要检查：HKLM和HKCU下的 Folder\shellex 位置。
environment: *id001
severity: low
---

## 症状

文件夹右键菜单出现"在 %s 中打开文件夹"项，%s未替换，注册表在 *\shellex 和 Directory\shell 中找不到，实际藏在 HKCU\Folder\shellex\ContextMenuHandlers\UltraEdit。

## 根因

COM组件注册的shell扩展可能挂在 Folder 类下而非通用的 Directory 或 * 路径。Folder\shellex 是最容易被忽略的右键菜单注册位置。

## 解决

文件夹右键菜单查不全时要检查：HKLM和HKCU下的 Folder\shellex 位置。

