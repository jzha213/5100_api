from .base import *

# Production settings
DEBUG = False

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =======================
# Media files（生产环境）
# =======================
# 说明：
# - 开发环境（development.py）使用 BASE_DIR / 'media'
# - 生产环境统一使用服务器上的 /var/www/5100_media 目录，方便 Nginx 直接映射
# - 这样分类图标、商品图片、头像等所有上传文件都会保存到 /var/www/5100_media 下
from pathlib import Path
MEDIA_ROOT = Path('/var/www/5100_media')

# 保持 URL 前缀不变，仍然是 /media/
# Nginx 需要有类似配置：
#   location /media/ {
#       alias /var/www/5100_media/;
#   }

# 使用本地文件系统存储
# 如果将来要用云存储（如 OSS、S3），可以在这里替换存储后端
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Logging for production
LOGGING['handlers']['file']['filename'] = BASE_DIR / 'logs' / '5100water.log'
LOGGING['handlers']['file']['level'] = 'WARNING'

# Sentry (if configured)
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )
