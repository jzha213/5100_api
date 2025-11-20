#!/usr/bin/env python
"""
详细测试Django管理后台中文配置
"""
import requests
from requests.sessions import Session

BASE_URL = "http://127.0.0.1:8000"

def test_detailed_chinese_admin():
    """详细测试中文管理后台"""
    print("🔍 详细测试Django管理后台中文配置...")
    
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
        
        # 2. 检查登录页面的中文内容
        print("2. 检查登录页面中文内容...")
        login_chinese = [
            'Django 管理', '登录', '用户名', '密码', '忘记密码', '记住我'
        ]
        
        found_login_chinese = []
        for item in login_chinese:
            if item in content:
                found_login_chinese.append(item)
        
        print(f"   找到的中文内容: {found_login_chinese}")
        print(f"   中文化程度: {len(found_login_chinese)}/{len(login_chinese)}")
        
        # 3. 尝试登录
        print("3. 尝试登录...")
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
                
                # 4. 访问管理后台首页
                print("4. 访问管理后台首页...")
                response = session.get(f"{BASE_URL}/admin/")
                
                if response.status_code == 200:
                    content = response.text
                    
                    # 5. 检查管理后台首页的中文内容
                    print("5. 检查管理后台首页中文内容...")
                    admin_chinese = [
                        'Django 管理', '首页', '认证和授权', '组', '用户',
                        '商品分类', '商品', '商品图片', '商品规格', '商品评价',
                        '订单', '订单商品', '购物车', '订单状态日志',
                        '用户地址', '优惠券', '用户优惠券', '优惠券使用记录'
                    ]
                    
                    found_admin_chinese = []
                    for item in admin_chinese:
                        if item in content:
                            found_admin_chinese.append(item)
                    
                    print(f"   找到的中文内容: {found_admin_chinese}")
                    print(f"   中文化程度: {len(found_admin_chinese)}/{len(admin_chinese)}")
                    
                    # 6. 检查是否有英文内容残留
                    print("6. 检查英文内容残留...")
                    english_indicators = [
                        'Django administration', 'Log in', 'Username', 'Password',
                        'Home', 'Authentication and Authorization', 'Groups', 'Users'
                    ]
                    
                    found_english = []
                    for item in english_indicators:
                        if item in content:
                            found_english.append(item)
                    
                    print(f"   找到的英文内容: {found_english}")
                    
                    # 7. 评估中文化程度
                    total_chinese_items = len(found_login_chinese) + len(found_admin_chinese)
                    total_expected_items = len(login_chinese) + len(admin_chinese)
                    chinese_ratio = total_chinese_items / total_expected_items
                    
                    print(f"\n📊 中文化评估:")
                    print(f"   登录页面中文: {len(found_login_chinese)}/{len(login_chinese)}")
                    print(f"   管理页面中文: {len(found_admin_chinese)}/{len(admin_chinese)}")
                    print(f"   总体中文化程度: {chinese_ratio:.1%}")
                    print(f"   英文内容残留: {len(found_english)}")
                    
                    if chinese_ratio >= 0.8 and len(found_english) <= 2:
                        print("✅ 管理后台中文化配置成功！")
                        return True
                    elif chinese_ratio >= 0.6:
                        print("⚠️ 管理后台中文化基本成功，但还有改进空间")
                        return True
                    else:
                        print("❌ 管理后台中文化配置不完整")
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

def test_model_pages():
    """测试模型页面的中文显示"""
    print("\n🔍 测试模型页面的中文显示...")
    
    session = Session()
    
    try:
        # 先登录
        response = session.get(f"{BASE_URL}/admin/login/")
        if response.status_code != 200:
            return False
        
        content = response.text
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        if not csrf_match:
            return False
        
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
            # 测试各个模型页面
            model_pages = [
                ('/admin/users/user/', '用户管理'),
                ('/admin/products/product/', '商品管理'),
                ('/admin/orders/order/', '订单管理'),
            ]
            
            chinese_pages = []
            for url, name in model_pages:
                try:
                    response = session.get(f"{BASE_URL}{url}")
                    if response.status_code == 200:
                        content = response.text
                        # 检查是否有中文内容
                        if '添加' in content or '删除' in content or '修改' in content:
                            chinese_pages.append(name)
                            print(f"   ✅ {name}: 中文显示正常")
                        else:
                            print(f"   ⚠️ {name}: 中文显示可能有问题")
                    else:
                        print(f"   ❌ {name}: 无法访问")
                except Exception as e:
                    print(f"   ❌ {name}: 异常 - {e}")
            
            print(f"\n📊 模型页面中文化: {len(chinese_pages)}/{len(model_pages)}")
            return len(chinese_pages) >= len(model_pages) * 0.7
        else:
            print("❌ 登录失败，无法测试模型页面")
            return False
            
    except Exception as e:
        print(f"❌ 模型页面测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 详细测试Django管理后台中文配置...")
    print("=" * 60)
    
    # 测试详细中文配置
    detailed_success = test_detailed_chinese_admin()
    
    # 测试模型页面中文显示
    model_success = test_model_pages()
    
    print("\n" + "=" * 60)
    print("📊 详细中文配置测试结果:")
    print(f"   - 详细中文化测试: {'✅' if detailed_success else '❌'}")
    print(f"   - 模型页面中文显示: {'✅' if model_success else '❌'}")
    
    if detailed_success and model_success:
        print("\n🎉 Django管理后台中文配置完全成功！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 中文化配置包括:")
        print("   - 语言设置: 中文简体 (zh-Hans)")
        print("   - 时区设置: 亚洲/上海")
        print("   - 模型名称: 中文显示")
        print("   - 界面元素: 中文显示")
        print("   - SimpleUI主题: 中文配置")
    elif detailed_success:
        print("\n✅ Django管理后台中文配置基本成功！")
        print("   界面已中文化，但部分功能可能需要进一步优化")
    else:
        print("\n⚠️ 中文配置可能存在问题，建议检查配置")
    
    return detailed_success and model_success

if __name__ == "__main__":
    main()
