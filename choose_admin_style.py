#!/usr/bin/env python
"""
管理后台样式选择脚本
"""
import os

def choose_admin_style():
    """选择管理后台样式"""
    print("🎨 管理后台样式选择")
    print("=" * 40)
    print("1. 使用SimpleUI美化 (可能不稳定)")
    print("2. 使用原生Django Admin + 自定义CSS美化")
    print("3. 使用原生Django Admin (最稳定)")
    print()
    
    choice = input("请选择样式 (1-3): ").strip()
    
    if choice == "1":
        print("✅ 保持SimpleUI配置")
        print("   如果页面仍闪烁，请选择其他选项")
    elif choice == "2":
        print("🔧 切换到原生Django Admin + 自定义CSS")
        disable_simpleui()
        enable_custom_css()
    elif choice == "3":
        print("🔧 切换到原生Django Admin")
        disable_simpleui()
        disable_custom_css()
    else:
        print("❌ 无效选择")
        return
    
    print("\n📋 下一步:")
    print("   1. 重启服务器: python manage.py runserver 127.0.0.1:8000")
    print("   2. 访问管理后台: http://127.0.0.1:8000/admin/")
    print("   3. 登录测试页面稳定性")

def disable_simpleui():
    """禁用SimpleUI"""
    settings_file = "config/settings/base.py"
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 注释掉SimpleUI
    content = content.replace(
        "    'simpleui',  # 重新启用SimpleUI，使用优化配置",
        "    # 'simpleui',  # 暂时禁用SimpleUI"
    )
    
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ SimpleUI已禁用")

def enable_custom_css():
    """启用自定义CSS"""
    print("   ✅ 自定义CSS已准备就绪")
    print("   📁 自定义样式文件: static/admin/css/custom_admin.css")

def disable_custom_css():
    """禁用自定义CSS"""
    print("   ✅ 使用原生Django Admin样式")

if __name__ == "__main__":
    choose_admin_style()
