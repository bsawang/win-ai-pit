---
id: bat-chcp-65001-gbk
title: .bat chcp 65001 + GBK 编码冲突导致中文乱码
type: windows_pitfall
tags:
- encoding
- bat
- chcp
- GBK
- UTF-8
- garbled
importance: 5
metadata:
  type: windows_pitfall
  symptom: GBK编码的.bat文件开头加了 chcp 65001，在中文Windows上运行时echo的中文显示为乱码。
  root_cause: chcp 65001 将终端切换到UTF-8代码页，但.bat文件实际是GBK编码。中文Windows默认代码页936(GBK)，设了65001后终端按UTF-8解读GBK字节导致乱码。
  solution: GBK编码的.bat不要加 chcp 65001，让终端保持默认的936代码页即可正常显示中文。如果需要UTF-8输出，应将.bat保存为UTF-8编码且不加BOM。
  environment: &id001
    os:
    - Windows 10/11
    tool: cmd, bat
  severity: medium
symptom: GBK编码的.bat文件开头加了 chcp 65001，在中文Windows上运行时echo的中文显示为乱码。
root_cause: chcp 65001 将终端切换到UTF-8代码页，但.bat文件实际是GBK编码。中文Windows默认代码页936(GBK)，设了65001后终端按UTF-8解读GBK字节导致乱码。
solution: GBK编码的.bat不要加 chcp 65001，让终端保持默认的936代码页即可正常显示中文。如果需要UTF-8输出，应将.bat保存为UTF-8编码且不加BOM。
environment: *id001
severity: medium
---

## 症状

GBK编码的.bat文件开头加了 chcp 65001，在中文Windows上运行时echo的中文显示为乱码。

## 根因

chcp 65001 将终端切换到UTF-8代码页，但.bat文件实际是GBK编码。中文Windows默认代码页936(GBK)，设了65001后终端按UTF-8解读GBK字节导致乱码。

## 解决

GBK编码的.bat不要加 chcp 65001，让终端保持默认的936代码页即可正常显示中文。如果需要UTF-8输出，应将.bat保存为UTF-8编码且不加BOM。

