#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整用户注册和验证流程测试脚本
"""

import sys
import os
import requests
import json

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 设置环境变量
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'purchase_orders'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'pgsql'
os.environ['DB_PORT'] = '5432'

try:
    from backend.models.user_model import UserManager
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


def test_full_user_flow():
    """测试完整的用户注册和验证流程"""
    print("开始测试完整的用户注册和验证流程...")
    
    # 创建用户管理器
    user_manager = UserManager()
    
    # 1. 注册用户
    print("1. 注册用户...")
    test_email = "full_test@wefabricate.com"
    test_password = "fulltestpassword123"
    
    success, result = user_manager.register_user(test_email, test_password)
    print(f"   注册结果: {success}, {result}")
    
    if not success:
        print("   用户注册失败")
        return
    
    # 获取验证令牌
    verification_token = result
    print(f"   验证令牌: {verification_token}")
    
    # 2. 验证令牌
    print("2. 验证令牌...")
    success, result = user_manager.verify_user(verification_token)
    print(f"   验证结果: {success}, {result}")
    
    if not success:
        print("   令牌验证失败")
        return
    
    user_id = result['user_id']
    print(f"   用户ID: {user_id}")
    
    # 3. 设置密码
    print("3. 设置密码...")
    success, message = user_manager.set_user_password(user_id, test_password)
    print(f"   设置密码结果: {success}, {message}")
    
    if not success:
        print("   设置密码失败")
        return
    
    # 4. 用户登录
    print("4. 用户登录...")
    success, result = user_manager.authenticate_user(test_email, test_password)
    print(f"   登录结果: {success}, {result}")
    
    if success:
        print("✓ 完整用户流程测试成功")
    else:
        print("✗ 用户登录失败")
    
    print("完整用户流程测试完成")


if __name__ == "__main__":
    test_full_user_flow()