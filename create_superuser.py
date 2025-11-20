#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 创建超级用户
if not User.objects.filter(username='jzha213').exists():
    User.objects.create_superuser(
        username='jzha213',
        email='jzha213@5100water.com',
        password='zjzj828'
    )
    print('超级用户创建成功！用户名: jzha213, 密码: zjzj828')
else:
    print('超级用户已存在')
