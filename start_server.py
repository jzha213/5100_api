#!/usr/bin/env python
"""
快速启动脚本
"""
import os
import sys
import subprocess
import time
import argparse
from pathlib import Path


def check_dependencies():
    """检查依赖"""
    print("检查依赖...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要Python 3.8+")
        return False
    
    print(f"✓ Python版本: {sys.version}")
    
    # 检查必要的包
    required_packages = ['django', 'djangorestframework', 'pymysql']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def setup_database():
    """设置数据库"""
    print("\n设置数据库...")
    
    # 检查环境变量文件
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ 未找到.env文件，请复制env.example并配置")
        return False
    
    print("✓ 环境变量文件存在")
    
    # 运行数据库迁移
    try:
        print("运行数据库迁移...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], check=True, capture_output=True, text=True)
        print("✓ 数据库迁移完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库迁移失败: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    
    return True


def create_superuser():
    """创建超级用户"""
    print("\n检查超级用户...")
    
    try:
        # 检查是否已有超级用户
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            'from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())'
        ], capture_output=True, text=True)
        
        if result.stdout.strip() == 'True':
            print("✓ 超级用户已存在")
            return True
    except:
        pass
    
    print("创建超级用户...")
    print("用户名: admin")
    print("密码: admin123456")
    print("邮箱: admin@5100water.com")
    
    try:
        # 使用环境变量创建超级用户
        env = os.environ.copy()
        env['DJANGO_SUPERUSER_USERNAME'] = 'admin'
        env['DJANGO_SUPERUSER_PASSWORD'] = 'admin123456'
        env['DJANGO_SUPERUSER_EMAIL'] = 'admin@5100water.com'
        
        subprocess.run([
            sys.executable, 'manage.py', 'createsuperuser', '--noinput'
        ], env=env, check=True)
        print("✓ 超级用户创建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建超级用户失败: {e}")
        return False


def init_data():
    """初始化数据"""
    print("\n初始化数据...")
    
    try:
        result = subprocess.run([
            sys.executable, 'scripts/init_data.py'
        ], check=True, capture_output=True, text=True)
        print("✓ 数据初始化完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据初始化失败: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def start_server(host='127.0.0.1', port=8000, settings='development'):
    """启动服务器"""
    print(f"\n启动Django服务器...")
    print(f"地址: http://{host}:{port}")
    print(f"设置: {settings}")
    
    # 设置环境变量
    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = f'config.settings.{settings}'
    
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', f'{host}:{port}'
        ], env=env)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='5100订水小程序快速启动脚本')
    parser.add_argument('--host', default='127.0.0.1',
                       help='服务器地址 (默认: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000,
                       help='服务器端口 (默认: 8000)')
    parser.add_argument('--settings', default='development',
                       choices=['development', 'production'],
                       help='Django设置 (默认: development)')
    parser.add_argument('--skip-setup', action='store_true',
                       help='跳过设置步骤，直接启动服务器')
    parser.add_argument('--setup-only', action='store_true',
                       help='只执行设置，不启动服务器')
    
    args = parser.parse_args()
    
    print("="*60)
    print("5100天然冰川矿泉水订水小程序后端API")
    print("快速启动脚本")
    print("="*60)
    
    if not args.skip_setup:
        # 检查依赖
        if not check_dependencies():
            sys.exit(1)
        
        # 设置数据库
        if not setup_database():
            sys.exit(1)
        
        # 创建超级用户
        if not create_superuser():
            sys.exit(1)
        
        # 初始化数据
        if not init_data():
            sys.exit(1)
        
        print("\n✓ 所有设置完成!")
    
    if args.setup_only:
        print("设置完成，退出")
        return
    
    # 启动服务器
    print("\n" + "="*60)
    print("启动服务器...")
    print("="*60)
    print("访问地址:")
    print(f"  - API文档: http://{args.host}:{args.port}/swagger/")
    print(f"  - 管理后台: http://{args.host}:{args.port}/admin/")
    print(f"  - API接口: http://{args.host}:{args.port}/api/v1/")
    print("="*60)
    print("按 Ctrl+C 停止服务器")
    print("="*60)
    
    start_server(args.host, args.port, args.settings)


if __name__ == '__main__':
    main()
