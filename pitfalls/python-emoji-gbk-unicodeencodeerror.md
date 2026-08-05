---
id: python-emoji-gbk-unicodeencodeerror
title: Python 日志含 emoji 在 GBK 终端崩溃（UnicodeEncodeError）
type: windows_pitfall
importance: 5
metadata:
  type: windows_pitfall
  symptom: 'Python 进程 logging 输出含 emoji（如 U+1F4C2 等非 BMP 字符）时，中文 Windows 终端 stderr 默认 GBK(cp936) 抛 UnicodeEncodeError: gbk codec can not encode，logging 刷屏但非致命。同一日志经 UTF-8 通道（web console）显示正常，仅 GBK stderr 崩溃。'
  root_cause: 中文 Windows 的 Python stdout/stderr 默认编码 GBK(cp936)，只能编码 GBK 字符集内的 BMP 字符；emoji（U+1F000+ 非 BMP 区）超出范围，logging.emit 写入时抛 UnicodeEncodeError。
  solution: ①根治：改源码去掉日志 emoji 前缀（升级会被覆盖）；②通用 shim：启动时 sys.stdout.reconfigure(errors=replace) 和 sys.stderr.reconfigure(errors=replace)，保持 GBK 中文正常、不可编码字符变 ?，不崩溃；③环境变量 PYTHONIOENCODING=utf-8 或 PYTHONUTF8=1（输出切 UTF-8，中文可能在 GBK 终端乱码）。实例：majoor-assetsmanager 的 mjr_am_shared/log.py PREFIX 硬编码文件夹 emoji，在 ComfyUI 中文 Windows 终端触发。
  environment: &id001
    tool: python, logging
  severity: medium
symptom: 'Python 进程 logging 输出含 emoji（如 U+1F4C2 等非 BMP 字符）时，中文 Windows 终端 stderr 默认 GBK(cp936) 抛 UnicodeEncodeError: gbk codec can not encode，logging 刷屏但非致命。同一日志经 UTF-8 通道（web console）显示正常，仅 GBK stderr 崩溃。'
root_cause: 中文 Windows 的 Python stdout/stderr 默认编码 GBK(cp936)，只能编码 GBK 字符集内的 BMP 字符；emoji（U+1F000+ 非 BMP 区）超出范围，logging.emit 写入时抛 UnicodeEncodeError。
solution: ①根治：改源码去掉日志 emoji 前缀（升级会被覆盖）；②通用 shim：启动时 sys.stdout.reconfigure(errors=replace) 和 sys.stderr.reconfigure(errors=replace)，保持 GBK 中文正常、不可编码字符变 ?，不崩溃；③环境变量 PYTHONIOENCODING=utf-8 或 PYTHONUTF8=1（输出切 UTF-8，中文可能在 GBK 终端乱码）。实例：majoor-assetsmanager 的 mjr_am_shared/log.py PREFIX 硬编码文件夹 emoji，在 ComfyUI 中文 Windows 终端触发。
environment: *id001
severity: medium
---

## 症状

Python 进程 logging 输出含 emoji（如 U+1F4C2 等非 BMP 字符）时，中文 Windows 终端 stderr 默认 GBK(cp936) 抛 UnicodeEncodeError: gbk codec can not encode，logging 刷屏但非致命。同一日志经 UTF-8 通道（web console）显示正常，仅 GBK stderr 崩溃。

## 根因

中文 Windows 的 Python stdout/stderr 默认编码 GBK(cp936)，只能编码 GBK 字符集内的 BMP 字符；emoji（U+1F000+ 非 BMP 区）超出范围，logging.emit 写入时抛 UnicodeEncodeError。

## 解决

①根治：改源码去掉日志 emoji 前缀（升级会被覆盖）；②通用 shim：启动时 sys.stdout.reconfigure(errors=replace) 和 sys.stderr.reconfigure(errors=replace)，保持 GBK 中文正常、不可编码字符变 ?，不崩溃；③环境变量 PYTHONIOENCODING=utf-8 或 PYTHONUTF8=1（输出切 UTF-8，中文可能在 GBK 终端乱码）。实例：majoor-assetsmanager 的 mjr_am_shared/log.py PREFIX 硬编码文件夹 emoji，在 ComfyUI 中文 Windows 终端触发。

