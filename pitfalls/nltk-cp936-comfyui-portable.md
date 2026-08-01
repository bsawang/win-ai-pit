---
id: nltk-cp936-comfyui-portable
title: nltk 3.10 在 ComfyUI 便携版导入失败 (unknown encoding: cp936 / blocked import from cwd)
type: windows_pitfall
tags:
- nltk
- ComfyUI
- python
- cp936
- encoding
- security-finder
importance: 5
metadata:
  type: windows_pitfall
  symptom: import nltk 报 LookupError: unknown encoding: cp936 或 Blocked import of locale from current working directory；导致 SP-Nodes 插件加载失败，SP_DynamicCombo 等节点注册不了而报错。
  root_cause: nltk 3.10 新增 inisec.py CWD 安全隔离 finder，会拦截「从当前工作目录(CWD)导入」的模块。ComfyUI 便携版把 python_standalone 放在工作目录 H:\ComfyUI_Windows_portable 内，stdlib 的 locale/collections/functools 等被误判为 CWD 内模块而拦截，nltk 内部一 import stdlib 就抛 ImportError。
  solution: 在导入 nltk 之前设置环境变量 NLTK_DISABLE_IMPORT_SECURITY=1（inisec.py 官方开关）。例如在 SP-Nodes __init__.py 顶部加 os.environ.setdefault("NLTK_DISABLE_IMPORT_SECURITY","1")；同时预下载 punkt 数据。
  environment:
    os:
    - Windows 10/11
    tool: python, nltk, ComfyUI
  severity: high
symptom: import nltk 报 LookupError: unknown encoding: cp936 或 Blocked import of locale from current working directory；导致 SP-Nodes 插件加载失败，SP_DynamicCombo 等节点注册不了而报错。
root_cause: nltk 3.10 新增 inisec.py CWD 安全隔离 finder，会拦截「从当前工作目录(CWD)导入」的模块。ComfyUI 便携版把 python_standalone 放在工作目录 H:\ComfyUI_Windows_portable 内，stdlib 的 locale/collections/functools 等被误判为 CWD 内模块而拦截，nltk 内部一 import stdlib 就抛 ImportError。
solution: 在导入 nltk 之前设置环境变量 NLTK_DISABLE_IMPORT_SECURITY=1（inisec.py 官方开关）。例如在 SP-Nodes __init__.py 顶部加 os.environ.setdefault("NLTK_DISABLE_IMPORT_SECURITY","1")；同时预下载 punkt 数据。
severity: high
---

## 症状

`import nltk` 报 `LookupError: unknown encoding: cp936` 或 `Blocked import of locale from current working directory`。ComfyUI 中表现为 SP-Nodes 插件加载失败，`SP_DynamicCombo` 等节点无法注册，工作流打开时报节点缺失错误。

## 根因

nltk 3.10 的 `inisec.py` 引入了一个安全隔离 meta-path finder（CVE 防护），它会拦截「从当前工作目录(CWD)或其子目录导入」的模块——前提是导入由 nltk 发起。ComfyUI 便携版把 Python 运行时放在 `python_standalone\`，而它就在工作目录 `H:\ComfyUI_Windows_portable\` 内部，于是 stdlib 的 `locale`/`collections`/`functools` 等全被误判为"CWD 内模块"，nltk 内部一 import 标准库就被拦截抛 ImportError。`unknown encoding: cp936` 是它拦 `locale` 时连带出的假象。

## 解决

在导入 nltk 之前设置官方开关 `NLTK_DISABLE_IMPORT_SECURITY=1`。最省事的做法是在依赖 nltk 的插件 `__init__.py` 顶部加：

```python
import os
os.environ.setdefault("NLTK_DISABLE_IMPORT_SECURITY", "1")
```

再正常 `import nltk`。同时用 `nltk.download('punkt')` 预下载 punkt 数据。
