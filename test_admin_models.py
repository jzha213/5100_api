#!/usr/bin/env python
"""
测试管理后台中的自定义模型
"""
import requests
from requests.sessions import Session

BASE_URL = "http://127.0.0.1:8000"

def test_admin_models():
    """测试管理后台中的自定义模型"""
    print("🔍 测试管理后台中的自定义模型...")
    
    session = Session()
    
    try:
        # 1. 获取登录页面
        print("1. 获取登录页面...")
        response = session.get(f"{BASE_URL}/admin/login/")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ 无法访问登录页面")
            return False
        
        # 2. 提取CSRF token并登录
        print("2. 登录管理后台...")
        content = response.text
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        if not csrf_match:
            print("❌ 无法提取CSRF token")
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
        
        if response.status_code != 302:
            print("❌ 登录失败")
            return False
        
        print("✅ 登录成功")
        
        # 3. 访问管理后台首页
        print("3. 访问管理后台首页...")
        response = session.get(f"{BASE_URL}/admin/")
        
        if response.status_code != 200:
            print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
            return False
        
        content = response.text
        
        # 4. 检查我们的自定义模型是否在页面中
        print("4. 检查自定义模型...")
        
        expected_models = [
            '用户', '用户资料', '用户登录日志',
            '商品分类', '商品', '商品图片', '商品规格', '商品评价',
            '订单', '订单商品', '购物车', '订单状态日志',
            '用户地址',
            '优惠券', '用户优惠券', '优惠券使用记录'
        ]
        
        found_models = []
        missing_models = []
        
        for model in expected_models:
            if model in content:
                found_models.append(model)
                print(f"   ✅ 找到: {model}")
            else:
                missing_models.append(model)
                print(f"   ❌ 缺少: {model}")
        
        print(f"\n📊 检查结果:")
        print(f"   找到的模型: {len(found_models)}/{len(expected_models)}")
        print(f"   缺少的模型: {len(missing_models)}")
        
        if missing_models:
            print(f"   缺少的模型列表: {missing_models}")
        
        # 5. 尝试访问具体的模型页面
        print("\n5. 测试访问具体模型页面...")
        
        model_urls = [
            ('/admin/users/user/', '用户管理'),
            ('/admin/products/product/', '商品管理'),
            ('/admin/orders/order/', '订单管理'),
            ('/admin/addresses/address/', '地址管理'),
            ('/admin/coupons/coupon/', '优惠券管理'),
        ]
        
        accessible_models = []
        for url, name in model_urls:
            try:
                response = session.get(f"{BASE_URL}{url}")
                if response.status_code == 200:
                    accessible_models.append(name)
                    print(f"   ✅ {name}: 可访问")
                else:
                    print(f"   ❌ {name}: 状态码 {response.status_code}")
            except Exception as e:
                print(f"   ❌ {name}: 异常 - {e}")
        
        print(f"\n📊 可访问的模型页面: {len(accessible_models)}/{len(model_urls)}")
        
        # 总体评估
        success_rate = (len(found_models) + len(accessible_models)) / (len(expected_models) + len(model_urls))
        print(f"\n📊 总体成功率: {success_rate:.1%}")
        
        if success_rate >= 0.8:
            print("🎉 管理后台配置基本成功！")
            return True
        else:
            print("⚠️ 管理后台配置可能存在问题")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试管理后台中的自定义模型...")
    print("=" * 60)
    
    success = test_admin_models()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 管理后台中的自定义模型配置成功！")
        print("\n📋 您现在可以在浏览器中访问管理后台查看所有自定义模型")
        print("   🌐 地址: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
    else:
        print("❌ 管理后台配置可能存在问题，请检查配置")
    
    return success

if __name__ == "__main__":
    main()
