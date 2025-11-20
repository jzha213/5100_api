@echo off
echo ========================================
echo 正在应用admin美化效果...
echo ========================================

echo 1. 收集静态文件...
python manage.py collectstatic --noinput

echo 2. 重启Django服务器...
taskkill /f /im python.exe 2>nul
start python manage.py runserver

echo ========================================
echo 美化效果已应用！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 美化内容：
echo 1. 现代化渐变背景和卡片设计
echo 2. 美观的图标和字体
echo 3. 响应式布局适配移动端
echo 4. 流畅的动画效果
echo 5. 专业的配色方案
echo 6. 优化的用户体验
echo ========================================
pause
