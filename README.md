# 5100天然冰川矿泉水订水小程序后端API

## 项目简介

这是一个基于Django REST Framework的5100天然冰川矿泉水订水小程序后端API项目，提供完整的订水服务功能。

## 功能特性

- 用户认证与管理
- 商品管理
- 订单管理
- 支付处理
- 配送管理
- 地址管理
- 优惠券系统
- 消息通知
- 数据分析

## 技术栈

- **后端框架**: Django 4.2 LTS
- **API框架**: Django REST Framework
- **数据库**: MySQL 8.0
- **缓存**: Redis 6.0+
- **任务队列**: Celery
- **部署**: Docker + Nginx

## 项目结构

```
5100_api/
├── config/                 # 配置文件
│   ├── settings/           # 设置文件
│   ├── urls.py            # 主URL配置
│   └── wsgi.py            # WSGI配置
├── apps/                   # 应用目录
│   ├── common/            # 公共应用
│   ├── users/             # 用户管理
│   ├── products/          # 商品管理
│   ├── orders/            # 订单管理
│   ├── payments/          # 支付管理
│   ├── delivery/          # 配送管理
│   ├── addresses/         # 地址管理
│   ├── coupons/           # 优惠券管理
│   ├── notifications/     # 通知管理
│   └── analytics/         # 数据分析
├── static/                # 静态文件
├── media/                 # 媒体文件
├── logs/                  # 日志文件
├── scripts/               # 脚本文件
├── tests/                 # 测试文件
├── manage.py              # Django管理脚本
├── requirements.txt       # 依赖包
├── Dockerfile            # Docker配置
├── docker-compose.yml    # Docker编排
└── nginx.conf            # Nginx配置
```

## 快速开始

### 环境要求

- Python 3.11+
- MySQL 8.0+
- Redis 6.0+
- Docker (可选)

### 本地开发

1. 克隆项目
```bash
git clone <repository-url>
cd 5100_api
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE 5100water CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. 配置环境变量
```bash
cp env.example .env
# 编辑.env文件，设置数据库连接等信息
```

6. 运行迁移
```bash
python manage.py migrate
```

7. 创建超级用户
```bash
python manage.py createsuperuser
```

8. 初始化数据
```bash
python scripts/init_data.py
```

9. 启动开发服务器
```bash
python manage.py runserver
```

### Docker部署

1. 构建并启动服务
```bash
docker-compose up -d
```

2. 运行迁移
```bash
docker-compose exec web python manage.py migrate
```

3. 创建超级用户
```bash
docker-compose exec web python manage.py createsuperuser
```

4. 初始化数据
```bash
docker-compose exec web python scripts/init_data.py
```

## API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## 主要API接口

### 用户认证
- `POST /api/v1/auth/register/` - 用户注册
- `POST /api/v1/auth/wechat/login/` - 微信登录
- `POST /api/v1/auth/phone/login/` - 手机号登录

### 用户管理
- `GET /api/v1/users/profile/` - 获取用户信息
- `PUT /api/v1/users/profile/` - 更新用户信息
- `POST /api/v1/users/avatar/upload/` - 上传头像

### 商品管理
- `GET /api/v1/products/` - 商品列表
- `GET /api/v1/products/{id}/` - 商品详情
- `GET /api/v1/products/categories/` - 商品分类

### 订单管理
- `GET /api/v1/orders/` - 订单列表
- `POST /api/v1/orders/create/` - 创建订单
- `GET /api/v1/orders/{id}/` - 订单详情
- `POST /api/v1/orders/{id}/cancel/` - 取消订单

### 购物车
- `GET /api/v1/cart/` - 购物车列表
- `POST /api/v1/cart/create/` - 添加到购物车
- `PUT /api/v1/cart/{id}/update/` - 更新购物车
- `DELETE /api/v1/cart/{id}/delete/` - 删除购物车商品

### 支付管理
- `POST /api/v1/payments/create/` - 创建支付
- `POST /api/v1/payments/wechat/create/` - 微信支付
- `POST /api/v1/payments/wechat/callback/` - 微信支付回调

### 地址管理
- `GET /api/v1/addresses/` - 地址列表
- `POST /api/v1/addresses/` - 新增地址
- `PUT /api/v1/addresses/{id}/` - 更新地址
- `DELETE /api/v1/addresses/{id}/` - 删除地址

### 优惠券
- `GET /api/v1/coupons/` - 优惠券列表
- `POST /api/v1/coupons/user/create/` - 领取优惠券
- `POST /api/v1/coupons/validate/` - 验证优惠券
- `POST /api/v1/coupons/use/` - 使用优惠券

## 数据库配置

默认数据库配置：
- 主机: 127.0.0.1
- 端口: 3307
- 数据库: 5100water
- 用户: root
- 密码: zjzj828

## 开发规范

### 代码风格
- 遵循PEP8规范
- 使用4个空格缩进
- 函数和类之间空2行

### Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关

### 分支管理
- main: 主分支，生产环境
- develop: 开发分支
- feature/*: 功能分支
- hotfix/*: 热修复分支

## 测试

运行测试：
```bash
python manage.py test
```

## 部署

### 生产环境部署

1. 设置生产环境变量
2. 配置Nginx
3. 配置SSL证书
4. 使用Docker部署
5. 配置监控和日志

### 性能优化

- 使用Redis缓存
- 数据库查询优化
- 静态文件CDN
- 图片压缩
- API限流

## 监控和日志

- 使用Sentry进行错误监控
- 配置日志收集
- 性能监控
- 业务指标监控

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题，请联系开发团队。
