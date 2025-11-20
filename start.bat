@echo off
chcp 65001 >nul
echo ========================================
echo 5100天然冰川矿泉水订水小程序后端API
echo 快速启动脚本 (Windows)
echo ========================================
echo.

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo ✓ Python环境正常
echo.

echo 启动服务器...
python start_server.py

pause
