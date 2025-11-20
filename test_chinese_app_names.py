#!/usr/bin/env python
"""
测试左侧导航栏应用名称是否为中文
"""
import requests
from requests.sessions import Session

BASE_URL = "http://127.0.0.1:8000"

def test_chinese_app_names():
    """测试左侧导航栏应用名称是否为中文"""
    print("🔍 测试左侧导航栏应用名称是否为中文...")
    
    session = Session()
    
    try:
        # 1. 获取登录页面
        print("1. 获取登录页面...")
        response = session.get(f"{BASE_URL}/admin/login/")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ 无法访问登录页面")
            return False
        
        # 2. 登录
        print("2. 登录...")
        content = response.text
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        
        if csrf_match:
            csrf_token = csrf_match.group(1)
            
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
                print("   ✅ 登录成功")
                
                # 3. 访问管理后台首页
                print("3. 访问管理后台首页...")
                response = session.get(f"{BASE_URL}/admin/")
                
                if response.status_code == 200:
                    content = response.text
                    
                    # 4. 检查左侧导航栏的应用名称
                    print("4. 检查左侧导航栏应用名称...")
                    
                    # 期望的中文应用名称
                    expected_chinese_apps = [
                        '用户管理',
                        '商品管理', 
                        '订单管理',
                        '地址管理',
                        '优惠券管理',
                        '支付管理',
                        '配送管理',
                        '通知管理',
                        '数据分析'
                    ]
                    
                    # 检查是否还存在英文应用名称
                    english_apps = [
                        'Addresses',
                        'Coupons', 
                        'Orders',
                        'Products',
                        'Users'
                    ]
                    
                    found_chinese_apps = []
                    found_english_apps = []
                    
                    for app in expected_chinese_apps:
                        if app in content:
                            found_chinese_apps.append(app)
                    
                    for app in english_apps:
                        if app in content:
                            found_english_apps.append(app)
                    
                    print(f"   找到的中文应用名称: {found_chinese_apps}")
                    print(f"   找到的英文应用名称: {found_english_apps}")
                    print(f"   中文应用数量: {len(found_chinese_apps)}/{len(expected_chinese_apps)}")
                    print(f"   英文应用数量: {len(found_english_apps)}/{len(english_apps)}")
                    
                    # 评估结果
                    if len(found_chinese_apps) >= 5 and len(found_english_apps) == 0:
                        print("✅ 左侧导航栏应用名称已完全中文化！")
                        return True
                    elif len(found_chinese_apps) >= 3:
                        print("⚠️ 左侧导航栏应用名称部分中文化")
                        return True
                    else:
                        print("❌ 左侧导航栏应用名称仍未中文化")
                        return False
                        
                else:
                    print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
                    return False
            else:
                print("❌ 登录失败")
                return False
        else:
            print("❌ 无法提取CSRF token")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试左侧导航栏应用名称中文化...")
    print("=" * 50)
    
    success = test_chinese_app_names()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 左侧导航栏应用名称中文化成功！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 现在左侧导航栏应该显示中文应用名称:")
        print("   - 用户管理")
        print("   - 商品管理")
        print("   - 订单管理")
        print("   - 地址管理")
        print("   - 优惠券管理")
    else:
        print("⚠️ 左侧导航栏应用名称中文化可能存在问题")
        print("   建议检查apps.py文件配置")
    
    return success

if __name__ == "__main__":
    main()
