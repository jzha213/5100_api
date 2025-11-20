#!/usr/bin/env python
"""
用户认证API测试脚本
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_user_register():
    """测试用户注册API"""
    print("🔍 测试用户注册API...")
    try:
        # 测试数据
        register_data = {
            'username': 'testuser_auth',
            'password': 'test123456',
            'email': 'testuser_auth@example.com',
            'phone': '13900139000',
            'nickname': '测试认证用户'
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/register/", 
                               json=register_data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ 用户注册成功")
            print(f"   用户名: {data.get('data', {}).get('username', 'N/A')}")
            print(f"   昵称: {data.get('data', {}).get('nickname', 'N/A')}")
            return True
        else:
            data = response.json()
            print(f"❌ 用户注册失败: {data.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 用户注册API异常: {e}")
        return False

def test_user_login():
    """测试用户登录API"""
    print("\n🔍 测试用户登录API...")
    try:
        # 使用测试用户登录
        login_data = {
            'username': 'testuser_auth',
            'password': 'test123456'
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login/", 
                               json=login_data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 用户登录成功")
            print(f"   用户名: {data.get('data', {}).get('user', {}).get('username', 'N/A')}")
            print(f"   昵称: {data.get('data', {}).get('user', {}).get('nickname', 'N/A')}")
            print(f"   有access_token: {'access_token' in data.get('data', {})}")
            return data.get('data', {}).get('access_token')
        else:
            data = response.json()
            print(f"❌ 用户登录失败: {data.get('message', '未知错误')}")
            return None
    except Exception as e:
        print(f"❌ 用户登录API异常: {e}")
        return None

def test_user_profile(access_token):
    """测试获取用户信息API"""
    print("\n🔍 测试获取用户信息API...")
    if not access_token:
        print("❌ 没有access_token，跳过测试")
        return False
        
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(f"{BASE_URL}/api/v1/auth/profile/", 
                              headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取用户信息成功")
            print(f"   用户名: {data.get('data', {}).get('username', 'N/A')}")
            print(f"   邮箱: {data.get('data', {}).get('email', 'N/A')}")
            print(f"   手机: {data.get('data', {}).get('phone', 'N/A')}")
            return True
        else:
            data = response.json()
            print(f"❌ 获取用户信息失败: {data.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 获取用户信息API异常: {e}")
        return False

def test_superuser_login():
    """测试超级用户登录API"""
    print("\n🔍 测试超级用户登录API...")
    try:
        # 使用超级用户登录
        login_data = {
            'username': 'jzha213',
            'password': 'zjzj828'
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login/", 
                               json=login_data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 超级用户登录成功")
            print(f"   用户名: {data.get('data', {}).get('user', {}).get('username', 'N/A')}")
            print(f"   是超级用户: {data.get('data', {}).get('user', {}).get('is_superuser', False)}")
            return data.get('data', {}).get('access_token')
        else:
            data = response.json()
            print(f"❌ 超级用户登录失败: {data.get('message', '未知错误')}")
            return None
    except Exception as e:
        print(f"❌ 超级用户登录API异常: {e}")
        return None

def test_invalid_login():
    """测试无效登录"""
    print("\n🔍 测试无效登录...")
    try:
        # 使用错误的密码
        login_data = {
            'username': 'jzha213',
            'password': 'wrongpassword'
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login/", 
                               json=login_data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 401:
            data = response.json()
            print(f"✅ 无效登录测试通过 - 正确返回401错误")
            print(f"   错误信息: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ 无效登录测试失败 - 应该返回401错误")
            return False
    except Exception as e:
        print(f"❌ 无效登录测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试5100订水用户认证API...")
    print("=" * 60)
    
    # 测试用户注册
    register_success = test_user_register()
    
    # 测试用户登录
    access_token = test_user_login()
    
    # 测试获取用户信息
    profile_success = test_user_profile(access_token)
    
    # 测试超级用户登录
    superuser_token = test_superuser_login()
    
    # 测试无效登录
    invalid_login_success = test_invalid_login()
    
    print("\n" + "=" * 60)
    print("📊 认证API测试结果:")
    print(f"   - 用户注册: {'✅' if register_success else '❌'}")
    print(f"   - 用户登录: {'✅' if access_token else '❌'}")
    print(f"   - 获取用户信息: {'✅' if profile_success else '❌'}")
    print(f"   - 超级用户登录: {'✅' if superuser_token else '❌'}")
    print(f"   - 无效登录测试: {'✅' if invalid_login_success else '❌'}")
    
    total_tests = 5
    passed_tests = sum([register_success, bool(access_token), profile_success, 
                       bool(superuser_token), invalid_login_success])
    
    print(f"\n📊 总体结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 用户认证API测试全部通过！")
    else:
        print("⚠️  部分测试失败，请检查认证配置")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 用户认证API运行正常！")
        print("📋 可用的认证API端点:")
        print("   - POST /api/v1/auth/register/ (用户注册)")
        print("   - POST /api/v1/auth/login/ (用户登录)")
        print("   - GET /api/v1/auth/profile/ (获取用户信息)")
        print("   - POST /api/v1/auth/refresh/ (刷新token)")
        print("   - POST /api/v1/auth/logout/ (用户登出)")
    else:
        print("\n❌ 用户认证API测试失败！")
