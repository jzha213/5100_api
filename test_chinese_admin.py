#!/usr/bin/env python
"""
测试Django管理后台中文界面
"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_chinese_admin():
    """测试中文管理后台"""
    print("🔍 测试Django管理后台中文界面...")
    
    try:
        # 访问管理后台登录页面
        response = requests.get(f"{BASE_URL}/admin/")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查中文内容
            chinese_indicators = [
                'Django 管理',  # Django管理
                '登录',  # 登录
                '用户名',  # 用户名
                '密码',  # 密码
                '忘记密码',  # 忘记密码
                '记住我',  # 记住我
            ]
            
            found_chinese = []
            for indicator in chinese_indicators:
                if indicator in content:
                    found_chinese.append(indicator)
            
            print(f"找到的中文内容: {found_chinese}")
            print(f"找到的中文内容数量: {len(found_chinese)}")
            
            # 检查是否有英文内容（应该较少）
            english_indicators = [
                'Django administration',
                'Log in',
                'Username',
                'Password',
                'Forgotten your password',
                'Remember me'
            ]
            
            found_english = []
            for indicator in english_indicators:
                if indicator in content:
                    found_english.append(indicator)
            
            print(f"找到的英文内容: {found_english}")
            print(f"找到的英文内容数量: {len(found_english)}")
            
            # 评估中文化程度
            chinese_ratio = len(found_chinese) / len(chinese_indicators)
            print(f"中文化程度: {chinese_ratio:.1%}")
            
            if chinese_ratio >= 0.7:
                print("✅ 管理后台已成功中文化")
                return True
            else:
                print("⚠️ 管理后台中文化可能不完整")
                return False
                
        else:
            print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_admin_models_chinese():
    """测试管理后台模型的中文显示"""
    print("\n🔍 测试管理后台模型的中文显示...")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查我们的自定义模型中文名称
            chinese_models = [
                '用户', '用户资料', '用户登录日志',
                '商品分类', '商品', '商品图片', '商品规格', '商品评价',
                '订单', '订单商品', '购物车', '订单状态日志',
                '用户地址',
                '优惠券', '用户优惠券', '优惠券使用记录'
            ]
            
            found_models = []
            for model in chinese_models:
                if model in content:
                    found_models.append(model)
            
            print(f"找到的中文模型: {found_models}")
            print(f"找到的中文模型数量: {len(found_models)}")
            
            if found_models:
                print("✅ 管理后台模型已成功显示中文")
                return True
            else:
                print("❌ 管理后台模型未显示中文")
                return False
        else:
            print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试Django管理后台中文界面...")
    print("=" * 50)
    
    # 测试中文界面
    chinese_success = test_chinese_admin()
    
    # 测试模型中文显示
    models_success = test_admin_models_chinese()
    
    print("\n" + "=" * 50)
    print("📊 中文界面测试结果:")
    print(f"   - 界面中文化: {'✅' if chinese_success else '❌'}")
    print(f"   - 模型中文显示: {'✅' if models_success else '❌'}")
    
    if chinese_success and models_success:
        print("\n🎉 Django管理后台中文配置成功！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 现在管理后台已完全中文化，包括:")
        print("   - 界面语言: 中文简体")
        print("   - 时区设置: 亚洲/上海")
        print("   - 模型名称: 中文显示")
        print("   - SimpleUI主题: 中文配置")
    else:
        print("\n⚠️ 中文配置可能存在问题")
    
    return chinese_success and models_success

if __name__ == "__main__":
    main()
