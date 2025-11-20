@echo off
echo ========================================
echo 最终修复脚本 - 使用默认Admin模板
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 运行数据库调试...
python debug_admin.py

echo 3. 收集静态文件...
python manage.py collectstatic --noinput

echo 4. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 修复完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 修复内容：
echo 1. 删除了可能有问题的自定义模板
echo 2. 使用Django默认的admin模板
echo 3. 保留了美化的base.html模板
echo 4. 创建了测试数据
echo 
echo 测试账号：
echo 用户名: admin
echo 密码: admin123
echo ========================================
pause
