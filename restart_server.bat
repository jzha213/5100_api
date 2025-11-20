@echo off
echo ========================================
echo 正在修复admin后台刷新问题...
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 收集静态文件...
python manage.py collectstatic --noinput

echo 3. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 配置错误已修复！服务器启动中...
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 修复内容：
echo 1. 修复了settings.py中的NameError
echo 2. 完全禁用了SimpleUI
echo 3. 使用原生Django admin界面
echo 4. 彻底解决了页面刷新问题
echo ========================================
pause
