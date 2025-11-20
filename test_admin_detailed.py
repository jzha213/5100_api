#!/usr/bin/env python
"""
详细测试SimpleUI管理后台
"""
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_admin_page():
    """详细测试管理后台页面"""
    print("🔍 详细测试管理后台页面...")
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查各种SimpleUI特征
            simpleui_checks = {
                'simpleui': 'simpleui' in content,
                'layui': 'layui' in content,
                'fa fa-': 'fa fa-' in content,
                'admin/css/simpleui': 'admin/css/simpleui' in content,
                'admin/js/simpleui': 'admin/js/simpleui' in content,
                'simpleui.css': 'simpleui.css' in content,
                'simpleui.js': 'simpleui.js' in content,
            }
            
            print("\n📊 SimpleUI特征检查:")
            for check, result in simpleui_checks.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check}: {result}")
            
            # 检查页面标题
            if '<title>' in content:
                title_start = content.find('<title>') + 7
                title_end = content.find('</title>')
                title = content[title_start:title_end]
                print(f"\n📋 页面标题: {title}")
            
            # 检查是否有Django默认样式
            django_default = {
                'admin/css/base.css': 'admin/css/base.css' in content,
                'admin/css/dashboard.css': 'admin/css/dashboard.css' in content,
                'admin/css/forms.css': 'admin/css/forms.css' in content,
            }
            
            print("\n📊 Django默认样式检查:")
            for check, result in django_default.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check}: {result}")
            
            # 检查是否有SimpleUI特有的元素
            simpleui_elements = {
                'data-layui': 'data-layui' in content,
                'layui-layout': 'layui-layout' in content,
                'simpleui-menu': 'simpleui-menu' in content,
                'layui-nav': 'layui-nav' in content,
            }
            
            print("\n📊 SimpleUI元素检查:")
            for check, result in simpleui_elements.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check}: {result}")
            
            # 总体判断
            simpleui_count = sum(simpleui_checks.values())
            django_count = sum(django_default.values())
            
            print(f"\n📊 统计结果:")
            print(f"   SimpleUI特征: {simpleui_count}/{len(simpleui_checks)}")
            print(f"   Django默认特征: {django_count}/{len(django_default)}")
            
            if simpleui_count > 0:
                print("✅ SimpleUI已加载")
                return True
            else:
                print("❌ SimpleUI未加载，使用Django默认样式")
                return False
                
        else:
            print(f"❌ 管理后台访问失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 管理后台访问异常: {e}")
        return False

def test_static_files():
    """测试静态文件"""
    print("\n🔍 测试静态文件...")
    
    static_files = [
        '/static/admin/css/base.css',
        '/static/simpleui/css/simpleui.css',
        '/static/simpleui/js/simpleui.js',
    ]
    
    for static_file in static_files:
        try:
            response = requests.get(f"{BASE_URL}{static_file}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {static_file}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {static_file}: 异常 - {e}")

def main():
    """主测试函数"""
    print("🚀 详细测试SimpleUI管理后台...")
    print("=" * 60)
    
    # 测试管理后台页面
    admin_success = test_admin_page()
    
    # 测试静态文件
    test_static_files()
    
    print("\n" + "=" * 60)
    if admin_success:
        print("🎉 SimpleUI已成功加载！")
        print("\n📋 管理后台信息:")
        print("   🌐 访问地址: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
    else:
        print("⚠️  SimpleUI可能未正确配置")
        print("   建议检查:")
        print("   1. SimpleUI是否在INSTALLED_APPS中")
        print("   2. 静态文件是否正确收集")
        print("   3. SimpleUI版本是否兼容")
    
    return admin_success

if __name__ == "__main__":
    main()
