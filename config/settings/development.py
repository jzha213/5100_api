from .base import *

# Development settings
DEBUG = True

# Database for development - 连接服务器上的 MySQL
DATABASES['default'].update({
    'HOST': '8.134.151.99',  # 服务器 IP 地址
    'PORT': '3306',  # 服务器 MySQL 端口
    'NAME': '5100water',
    'USER': 'jzha213',  # 服务器 MySQL 用户名
    'PASSWORD': 'zHaijun8288?',  # 服务器 MySQL 密码
})

# Disable cache in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable SSL redirect
SECURE_SSL_REDIRECT = False

# Django Debug Toolbar (optional)
# Uncomment the following lines if you want to install django-debug-toolbar
# if DEBUG:
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#     INTERNAL_IPS = ['127.0.0.1']
