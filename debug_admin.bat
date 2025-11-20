@echo off
echo ========================================
echo Admin后台数据调试脚本
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 运行调试脚本...
python debug_admin.py

echo 3. 收集静态文件...
python manage.py collectstatic --noinput

echo 4. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 调试完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 如果还是看不到数据，请：
echo 1. 按Ctrl+F5强制刷新浏览器
echo 2. 清除浏览器缓存
echo 3. 检查控制台错误信息
echo ========================================
pause
