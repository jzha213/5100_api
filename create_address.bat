@echo off
cd /d "E:\微信小程序\5100_api"
python -c "
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
sys.path.append('.')
django.setup()

from apps.users.models import User
from apps.addresses.models import Address

try:
    user = User.objects.get(username='admin')
    print(f'找到用户: {user.username}')
    
    existing = Address.objects.filter(user=user).first()
    if existing:
        print(f'用户已有地址: {existing.id}')
    else:
        address = Address.objects.create(
            user=user,
            name='测试收货人',
            phone='13800138000',
            province='北京市',
            city='北京市',
            district='朝阳区',
            street='三里屯街道',
            detail_address='三里屯SOHO A座1001室',
            is_default=True
        )
        print(f'创建测试地址成功: {address.id}')
except Exception as e:
    print(f'错误: {e}')
"
pause

