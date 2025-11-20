@echo off
echo ========================================
echo 修复UserAdmin字段错误
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 运行数据库迁移...
python manage.py makemigrations
python manage.py migrate

echo 3. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 修复完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 修复内容：
echo 1. 修正了UserAdmin中的字段名
echo 2. 将 'avatar' 改为 'avatar_url'
echo 3. 现在可以正常编辑用户信息了
echo ========================================
pause
