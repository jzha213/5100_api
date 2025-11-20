@echo off
cd /d "E:\微信小程序\5100_api"
echo 正在收集静态文件...
python manage.py collectstatic --noinput
echo 静态文件收集完成！
echo 请重启Django服务器以使更改生效
pause
