@echo off
REM Windows 避坑指南 — MCP Server 启动脚本
REM 首次使用前先运行 python scripts/setup.py

cd /d "%~dp0.."
python -m pyrite.server.mcp_server --tier admin
pause
