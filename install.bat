@echo off
chcp 65001 >nul
title Windows 避坑指南 — 安装
cd /d "%~dp0"
echo === 安装依赖 ===
pip install -e .
if %errorlevel% neq 0 (
    echo [错误] pip 安装失败，请确认已安装 Python 3.11+
    pause
    exit /b 1
)
echo.
echo === 配置项目 ===
python scripts/setup.py
if %errorlevel% neq 0 (
    echo [错误] 配置失败
    pause
    exit /b 1
)
echo.
echo === 安装完成 ===
echo 现在可以打开 Claude Code，MCP Server 会自动启动。
echo 也可以双击 start-mcp.bat 手动启动。
pause
