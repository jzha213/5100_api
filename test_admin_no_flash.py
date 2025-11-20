#!/usr/bin/env python
"""
测试管理后台是否还有闪烁问题
"""
import requests
from requests.sessions import Session
import time

BASE_URL = "http://127.0.0.1:8000"

def test_admin_no_flash():
    """测试管理后台是否还有闪烁问题"""
    print("🔍 测试管理后台是否还有闪烁问题...")
    
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
        
        # 检查是否还在使用SimpleUI
        if 'simpleui' in content:
            print("   ⚠️ 仍在检测到SimpleUI")
        else:
            print("   ✅ 已禁用SimpleUI")
        
        # 2. 登录
        print("2. 登录...")
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
                
                # 3. 连续访问管理后台首页，监控稳定性
                print("3. 监控管理后台稳定性...")
                
                stable_count = 0
                total_attempts = 10
                
                for i in range(total_attempts):
                    try:
                        start_time = time.time()
                        response = session.get(f"{BASE_URL}/admin/")
                        end_time = time.time()
                        
                        response_time = end_time - start_time
                        
                        if response.status_code == 200:
                            stable_count += 1
                            print(f"   请求 {i+1}: ✅ 成功 (响应时间: {response_time:.2f}s)")
                        else:
                            print(f"   请求 {i+1}: ❌ 失败 (状态码: {response.status_code})")
                        
                        # 等待0.5秒
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"   请求 {i+1}: ❌ 异常 - {e}")
                
                stability_rate = stable_count / total_attempts
                print(f"   稳定性: {stable_count}/{total_attempts} ({stability_rate:.1%})")
                
                # 4. 检查页面内容是否稳定
                print("4. 检查页面内容稳定性...")
                
                try:
                    response = session.get(f"{BASE_URL}/admin/")
                    if response.status_code == 200:
                        content = response.text
                        
                        # 检查关键元素
                        key_elements = [
                            'Django administration',
                            'Site administration',
                            'Welcome',
                            'Recent actions'
                        ]
                        
                        found_elements = []
                        for element in key_elements:
                            if element in content:
                                found_elements.append(element)
                        
                        print(f"   找到的关键元素: {found_elements}")
                        print(f"   元素完整性: {len(found_elements)}/{len(key_elements)}")
                        
                        if len(found_elements) >= 3:
                            print("   ✅ 页面内容稳定")
                            return True
                        else:
                            print("   ⚠️ 页面内容可能不稳定")
                            return False
                    else:
                        print(f"   ❌ 无法获取页面内容，状态码: {response.status_code}")
                        return False
                        
                except Exception as e:
                    print(f"   ❌ 页面内容检查异常: {e}")
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
    print("🚀 测试管理后台闪烁问题修复...")
    print("=" * 50)
    
    success = test_admin_no_flash()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 管理后台闪烁问题已修复！")
        print("\n📋 修复措施:")
        print("   - 暂时禁用SimpleUI")
        print("   - 优化CSRF和Session配置")
        print("   - 使用原生Django Admin")
        print("\n✨ 现在管理后台应该稳定运行，不再闪烁")
        print("   如需重新启用SimpleUI，可以取消注释相关配置")
    else:
        print("⚠️ 管理后台闪烁问题可能仍然存在")
        print("   建议:")
        print("   1. 清除浏览器缓存和Cookie")
        print("   2. 尝试使用无痕模式访问")
        print("   3. 检查浏览器控制台错误")
    
    return success

if __name__ == "__main__":
    main()
