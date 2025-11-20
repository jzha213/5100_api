#!/usr/bin/env python
"""
简化的SimpleUI测试
"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_simpleui_loaded():
    """测试SimpleUI是否加载"""
    print("🔍 测试SimpleUI是否加载...")
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查SimpleUI特征
            simpleui_indicators = [
                'simpleui',
                'Django 站点管理员-登录',
                'layui',
                'simpleui.css',
                'simpleui.js'
            ]
            
            found_indicators = []
            for indicator in simpleui_indicators:
                if indicator in content:
                    found_indicators.append(indicator)
            
            print(f"找到SimpleUI特征: {found_indicators}")
            
            if found_indicators:
                print("✅ SimpleUI已加载")
                return True
            else:
                print("❌ SimpleUI未加载")
                return False
        else:
            print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_static_files():
    """测试静态文件"""
    print("\n🔍 测试静态文件...")
    
    static_files = [
        '/static/admin/css/base.css',
        '/static/simpleui/css/simpleui.css',
        '/static/simpleui/js/simpleui.js',
        '/static/admin/css/widgets.css',
    ]
    
    for static_file in static_files:
        try:
            response = requests.get(f"{BASE_URL}{static_file}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {static_file}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {static_file}: 异常")

def main():
    """主测试函数"""
    print("🚀 简化SimpleUI测试...")
    print("=" * 40)
    
    # 测试SimpleUI加载
    simpleui_loaded = test_simpleui_loaded()
    
    # 测试静态文件
    test_static_files()
    
    print("\n" + "=" * 40)
    if simpleui_loaded:
        print("🎉 SimpleUI已成功加载！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 您可以在浏览器中访问管理后台查看SimpleUI美化效果")
    else:
        print("❌ SimpleUI未正确加载")
    
    return simpleui_loaded

if __name__ == "__main__":
    main()
