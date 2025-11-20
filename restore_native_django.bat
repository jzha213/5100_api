@echo off
echo ========================================
echo 恢复到原生Django Admin
echo ========================================

echo 1. 停止Django服务器...
taskkill /f /im python.exe 2>nul

echo 2. 运行简单数据库测试...
python simple_db_test.py

echo 3. 收集静态文件...
python manage.py collectstatic --noinput

echo 4. 启动Django服务器...
start python manage.py runserver

echo ========================================
echo 恢复完成！
echo 请访问: http://127.0.0.1:8000/admin/
echo 
echo 现在使用的是原生Django Admin：
echo 1. 删除了所有自定义模板
echo 2. 删除了自定义CSS样式
echo 3. 删除了防刷新中间件
echo 4. 使用Django默认配置
echo 5. 创建了测试数据
echo 
echo 测试账号：
echo 用户名: admin
echo 密码: admin123
echo ========================================
pause
