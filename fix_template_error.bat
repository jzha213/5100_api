@echo off
echo ========================================
echo 修复模板语法错误...
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 收集静态文件...
python manage.py collectstatic --noinput

echo 3. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 模板语法错误已修复！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 修复内容：
echo 1. 添加了 {% load i18n %} 标签
echo 2. 修复了模板继承问题
echo 3. 现在应该可以正常显示美化后的界面
echo ========================================
pause
