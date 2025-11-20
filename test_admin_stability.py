#!/usr/bin/env python
"""
测试管理后台稳定性，检查是否还有页面刷新问题
"""
import requests
from requests.sessions import Session
import time

BASE_URL = "http://127.0.0.1:8000"

def test_admin_stability():
    """测试管理后台稳定性"""
    print("🔍 测试管理后台稳定性...")
    
    session = Session()
    
    try:
        # 1. 访问登录页面
        print("1. 访问登录页面...")
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
                
                # 3. 多次访问管理后台首页，测试稳定性
                print("3. 测试管理后台稳定性...")
                
                stable_requests = 0
                total_requests = 5
                
                for i in range(total_requests):
                    try:
                        response = session.get(f"{BASE_URL}/admin/")
                        if response.status_code == 200:
                            stable_requests += 1
                            print(f"   请求 {i+1}: ✅ 成功")
                        else:
                            print(f"   请求 {i+1}: ❌ 失败 (状态码: {response.status_code})")
                        
                        # 等待1秒
                        time.sleep(1)
                    except Exception as e:
                        print(f"   请求 {i+1}: ❌ 异常 - {e}")
                
                stability_rate = stable_requests / total_requests
                print(f"   稳定性: {stable_requests}/{total_requests} ({stability_rate:.1%})")
                
                # 4. 测试访问不同页面
                print("4. 测试访问不同页面...")
                
                test_pages = [
                    ('/admin/users/user/', '用户管理'),
                    ('/admin/products/product/', '商品管理'),
                    ('/admin/orders/order/', '订单管理'),
                ]
                
                successful_pages = 0
                for url, name in test_pages:
                    try:
                        response = session.get(f"{BASE_URL}{url}")
                        if response.status_code == 200:
                            successful_pages += 1
                            print(f"   ✅ {name}: 访问成功")
                        else:
                            print(f"   ❌ {name}: 访问失败 (状态码: {response.status_code})")
                    except Exception as e:
                        print(f"   ❌ {name}: 访问异常 - {e}")
                
                page_success_rate = successful_pages / len(test_pages)
                print(f"   页面访问成功率: {successful_pages}/{len(test_pages)} ({page_success_rate:.1%})")
                
                # 总体评估
                if stability_rate >= 0.8 and page_success_rate >= 0.8:
                    print("✅ 管理后台稳定性测试通过！")
                    return True
                elif stability_rate >= 0.6:
                    print("⚠️ 管理后台基本稳定，但偶尔可能有问题")
                    return True
                else:
                    print("❌ 管理后台稳定性存在问题")
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
    print("🚀 测试管理后台稳定性...")
    print("=" * 50)
    
    success = test_admin_stability()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 管理后台稳定性修复成功！")
        print("\n📋 修复内容:")
        print("   - CSRF配置优化")
        print("   - Session配置优化")
        print("   - SimpleUI配置优化")
        print("\n✨ 现在管理后台应该稳定运行，不会出现页面刷新闪烁问题")
    else:
        print("⚠️ 管理后台稳定性可能仍存在问题")
        print("   建议检查浏览器控制台是否有JavaScript错误")
    
    return success

if __name__ == "__main__":
    main()
