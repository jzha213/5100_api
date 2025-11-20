#!/usr/bin/env python
"""
测试当前管理后台状态
"""
import requests
from requests.sessions import Session
import time

BASE_URL = "http://127.0.0.1:8000"

def test_admin_stability():
    """测试管理后台稳定性"""
    print("🔍 测试当前管理后台状态...")
    
    session = Session()
    
    try:
        # 1. 访问登录页面
        print("1. 访问登录页面...")
        response = session.get(f"{BASE_URL}/admin/login/")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ 无法访问登录页面")
            return False
        
        content = response.text
        
        # 检查当前使用的样式
        if 'simpleui' in content:
            print("   📱 当前使用: SimpleUI")
        else:
            print("   📱 当前使用: 原生Django Admin")
        
        # 2. 登录测试
        print("2. 登录测试...")
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
                
                # 3. 测试页面稳定性
                print("3. 测试页面稳定性...")
                
                stable_count = 0
                total_tests = 5
                
                for i in range(total_tests):
                    try:
                        start_time = time.time()
                        response = session.get(f"{BASE_URL}/admin/")
                        end_time = time.time()
                        
                        response_time = end_time - start_time
                        
                        if response.status_code == 200:
                            stable_count += 1
                            print(f"   测试 {i+1}: ✅ 成功 ({response_time:.2f}s)")
                        else:
                            print(f"   测试 {i+1}: ❌ 失败 ({response.status_code})")
                        
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"   测试 {i+1}: ❌ 异常 - {e}")
                
                stability = stable_count / total_tests
                print(f"   稳定性: {stable_count}/{total_tests} ({stability:.1%})")
                
                if stability >= 0.8:
                    print("✅ 管理后台运行稳定！")
                    return True
                else:
                    print("⚠️ 管理后台可能存在稳定性问题")
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
    print("🚀 测试当前管理后台状态...")
    print("=" * 50)
    
    success = test_admin_stability()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 管理后台运行正常！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 如果页面仍有问题，可以运行:")
        print("   python choose_admin_style.py")
    else:
        print("⚠️ 管理后台可能存在问题")
        print("\n🔧 建议:")
        print("   1. 运行: python choose_admin_style.py")
        print("   2. 选择更稳定的样式选项")
        print("   3. 重启服务器")
    
    return success

if __name__ == "__main__":
    main()

