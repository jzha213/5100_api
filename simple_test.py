#!/usr/bin/env python
"""
简化的API测试脚本
测试基本功能
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_admin_access():
    """测试管理后台访问"""
    print("\n🔍 测试管理后台访问...")
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        if response.status_code == 200:
            print("✅ 管理后台可访问")
            return True
        else:
            print(f"❌ 管理后台访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 管理后台访问异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试5100订水API基本功能...")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_admin_access,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 基本功能测试通过！服务器运行正常！")
    else:
        print("⚠️  部分测试失败，请检查服务器状态")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 可以访问管理后台：http://127.0.0.1:8000/admin/")
        print("   用户名：jzha213")
        print("   密码：zjzj828")
