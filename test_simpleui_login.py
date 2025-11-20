#!/usr/bin/env python
"""
测试SimpleUI管理后台登录功能
"""
import requests
from requests.sessions import Session

BASE_URL = "http://127.0.0.1:8000"

def test_admin_login():
    """测试管理后台登录"""
    print("🔍 测试SimpleUI管理后台登录...")
    
    session = Session()
    
    try:
        # 1. 获取登录页面
        print("1. 获取登录页面...")
        response = session.get(f"{BASE_URL}/admin/login/")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ 无法访问登录页面")
            return False
        
        # 检查页面内容
        content = response.text
        if 'simpleui' in content:
            print("✅ 登录页面使用SimpleUI主题")
        else:
            print("❌ 登录页面未使用SimpleUI主题")
        
        # 2. 提取CSRF token
        csrf_token = None
        if 'csrfmiddlewaretoken' in content:
            # 从隐藏输入中提取CSRF token
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print("✅ 成功提取CSRF token")
            else:
                print("❌ 无法提取CSRF token")
                return False
        else:
            print("❌ 页面中没有CSRF token")
            return False
        
        # 3. 尝试登录
        print("2. 尝试登录...")
        login_data = {
            'username': 'jzha213',
            'password': 'zjzj828',
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        # 设置必要的headers
        headers = {
            'Referer': f"{BASE_URL}/admin/login/",
            'X-CSRFToken': csrf_token,
        }
        
        response = session.post(f"{BASE_URL}/admin/login/", data=login_data, headers=headers)
        print(f"   状态码: {response.status_code}")
        
        # 4. 检查登录结果
        if response.status_code == 302:
            print("✅ 登录成功，重定向到管理后台")
            
            # 5. 访问管理后台首页
            print("3. 访问管理后台首页...")
            response = session.get(f"{BASE_URL}/admin/")
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # 检查管理后台内容
                checks = {
                    'simpleui': 'simpleui' in content,
                    '管理后台': '管理后台' in content or 'Django' in content,
                    '用户': '用户' in content,
                    '商品': '商品' in content or 'Products' in content,
                    '订单': '订单' in content or 'Orders' in content,
                }
                
                print("   管理后台内容检查:")
                for check, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"     {status} {check}: {result}")
                
                # 检查是否有SimpleUI特有的元素
                if 'simpleui' in content:
                    print("✅ 管理后台使用SimpleUI主题")
                    return True
                else:
                    print("❌ 管理后台未使用SimpleUI主题")
                    return False
            else:
                print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
                return False
        else:
            print("❌ 登录失败")
            # 检查是否是密码错误
            if '密码' in response.text or 'password' in response.text.lower():
                print("   可能是用户名或密码错误")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试异常: {e}")
        return False

def test_admin_features():
    """测试管理后台功能"""
    print("\n🔍 测试管理后台功能...")
    
    session = Session()
    
    try:
        # 先登录
        response = session.get(f"{BASE_URL}/admin/login/")
        if response.status_code != 200:
            print("❌ 无法访问登录页面")
            return False
        
        content = response.text
        csrf_token = None
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        if csrf_match:
            csrf_token = csrf_match.group(1)
        
        # 登录
        login_data = {
            'username': 'jzha213',
            'password': 'zjzj828',
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        headers = {
            'Referer': f"{BASE_URL}/admin/login/",
            'X-CSRFToken': csrf_token,
        }
        
        response = session.post(f"{BASE_URL}/admin/login/", data=login_data, headers=headers)
        
        if response.status_code == 302:
            # 访问各个管理页面
            admin_pages = [
                ('/admin/', '管理后台首页'),
                ('/admin/users/', '用户管理'),
                ('/admin/products/', '商品管理'),
                ('/admin/orders/', '订单管理'),
            ]
            
            for page_url, page_name in admin_pages:
                try:
                    response = session.get(f"{BASE_URL}{page_url}")
                    status = "✅" if response.status_code == 200 else "❌"
                    print(f"   {status} {page_name}: {response.status_code}")
                except Exception as e:
                    print(f"   ❌ {page_name}: 异常 - {e}")
            
            return True
        else:
            print("❌ 登录失败，无法测试管理功能")
            return False
            
    except Exception as e:
        print(f"❌ 管理功能测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试SimpleUI管理后台登录功能...")
    print("=" * 60)
    
    # 测试登录
    login_success = test_admin_login()
    
    # 测试管理功能
    features_success = test_admin_features()
    
    print("\n" + "=" * 60)
    print("📊 SimpleUI管理后台测试结果:")
    print(f"   - 登录功能: {'✅' if login_success else '❌'}")
    print(f"   - 管理功能: {'✅' if features_success else '❌'}")
    
    if login_success and features_success:
        print("\n🎉 SimpleUI管理后台配置成功！")
        print("\n📋 管理后台访问信息:")
        print("   🌐 访问地址: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ SimpleUI美化功能:")
        print("   - 现代化登录界面")
        print("   - 响应式管理后台")
        print("   - 美观的菜单导航")
        print("   - 优化的数据展示")
    else:
        print("\n⚠️  SimpleUI管理后台配置可能存在问题")
    
    return login_success and features_success

if __name__ == "__main__":
    main()
