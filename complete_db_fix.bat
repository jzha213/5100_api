@echo off
echo ========================================
echo 完整数据库修复脚本
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 检查MySQL端口...
python check_mysql_port.py

echo 3. 运行数据库诊断...
python diagnose_db.py

echo 4. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 数据库修复完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 测试账号：
echo 用户名: admin
echo 密码: admin123
echo ========================================
pause
