@echo off
echo ========================================
echo 数据库连接检查和测试数据创建
echo ========================================

echo 1. 检查MySQL服务状态...
sc query MySQL80 | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo ❌ MySQL服务未运行，正在尝试启动...
    net start MySQL80
    if %errorlevel% neq 0 (
        echo ❌ 无法启动MySQL服务，请手动启动MySQL服务
        echo 或者检查MySQL服务名称是否正确
        pause
        exit /b 1
    )
) else (
    echo ✅ MySQL服务正在运行
)

echo 2. 运行数据库测试脚本...
python test_db.py

echo 3. 重启Django服务器...
taskkill /f /im python.exe 2>nul
start python manage.py runserver

echo ========================================
echo 数据库设置完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 测试账号：
echo 用户名: admin
echo 密码: admin123
echo ========================================
pause
