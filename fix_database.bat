@echo off
echo ========================================
echo 数据库连接修复脚本
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 运行数据库诊断...
python diagnose_db.py

echo 3. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 数据库修复完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 如果还有问题，请检查：
echo 1. MySQL服务是否启动
echo 2. 端口3307是否正确
echo 3. 数据库5100water是否存在
echo ========================================
pause
