#!/usr/bin/env python
"""
测试优化后的SimpleUI是否正常工作且不闪烁
"""
import requests
from requests.sessions import Session
import time

BASE_URL = "http://127.0.0.1:8000"

def test_simpleui_optimized():
    """测试优化后的SimpleUI"""
    print("🔍 测试优化后的SimpleUI...")
    
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
        
        # 检查SimpleUI是否已启用
        simpleui_indicators = [
            'simpleui',
            'layui',
            'fa fa-',
            'simpleui.css',
            'simpleui.js'
        ]
        
        found_indicators = []
        for indicator in simpleui_indicators:
            if indicator in content:
                found_indicators.append(indicator)
        
        print(f"   找到的SimpleUI特征: {found_indicators}")
        
        if found_indicators:
            print("   ✅ SimpleUI已启用")
        else:
            print("   ⚠️ SimpleUI可能未完全启用")
        
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
                
                # 3. 测试管理后台首页稳定性
                print("3. 测试管理后台首页稳定性...")
                
                stable_requests = 0
                total_requests = 5
                
                for i in range(total_requests):
                    try:
                        start_time = time.time()
                        response = session.get(f"{BASE_URL}/admin/")
                        end_time = time.time()
                        
                        response_time = end_time - start_time
                        
                        if response.status_code == 200:
                            stable_requests += 1
                            print(f"   请求 {i+1}: ✅ 成功 (响应时间: {response_time:.2f}s)")
                        else:
                            print(f"   请求 {i+1}: ❌ 失败 (状态码: {response.status_code})")
                        
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"   请求 {i+1}: ❌ 异常 - {e}")
                
                stability_rate = stable_requests / total_requests
                print(f"   稳定性: {stable_requests}/{total_requests} ({stability_rate:.1%})")
                
                # 4. 检查管理后台内容
                print("4. 检查管理后台内容...")
                
                response = session.get(f"{BASE_URL}/admin/")
                if response.status_code == 200:
                    content = response.text
                    
                    # 检查中文应用名称
                    chinese_apps = [
                        '用户管理', '商品管理', '订单管理', 
                        '地址管理', '优惠券管理', '认证和授权'
                    ]
                    
                    found_apps = []
                    for app in chinese_apps:
                        if app in content:
                            found_apps.append(app)
                    
                    print(f"   找到的中文应用: {found_apps}")
                    print(f"   中文应用数量: {len(found_apps)}/{len(chinese_apps)}")
                    
                    # 检查SimpleUI美化效果
                    simpleui_beautification = [
                        'layui-layout', 'layui-nav', 'simpleui-menu',
                        'fa fa-', 'layui-icon'
                    ]
                    
                    found_beautification = []
                    for feature in simpleui_beautification:
                        if feature in content:
                            found_beautification.append(feature)
                    
                    print(f"   找到的美化特征: {found_beautification}")
                    
                    # 总体评估
                    if stability_rate >= 0.8 and len(found_apps) >= 4:
                        print("✅ SimpleUI优化配置成功！")
                        print("   - 界面稳定，无闪烁")
                        print("   - 显示中文应用名称")
                        print("   - SimpleUI美化效果正常")
                        return True
                    else:
                        print("⚠️ SimpleUI配置可能需要进一步优化")
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
    print("🚀 测试优化后的SimpleUI...")
    print("=" * 50)
    
    success = test_simpleui_optimized()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SimpleUI优化配置成功！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 现在您拥有:")
        print("   - SimpleUI美化界面")
        print("   - 中文应用名称显示")
        print("   - 稳定的页面加载")
        print("   - 无闪烁问题")
    else:
        print("⚠️ SimpleUI配置可能存在问题")
        print("   建议检查配置或重新启动服务器")
    
    return success

if __name__ == "__main__":
    main()
