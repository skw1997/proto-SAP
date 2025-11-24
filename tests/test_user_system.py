#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户系统测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.models.user_model import UserManager
from backend.controllers.user_controller import UserController


def test_user_system():
    """测试用户系统"""
    print("开始测试用户系统...")
    
    # 创建用户管理器
    user_manager = UserManager()
    
    # 创建用户表
    print("1. 创建用户表...")
    success, message = user_manager.create_users_table()
    print(f"   结果: {message}")
    
    if not success:
        print("   用户表创建失败，测试终止")
        return
    
    # 测试用户注册
    print("2. 测试用户注册...")
    test_email = "test@wefabricate.com"
    test_password = "testpassword123"
    
    success, message = user_manager.register_user(test_email, test_password)
    print(f"   注册结果: {message}")
    
    if not success:
        print("   用户注册失败")
        return
    
    # 测试无效邮箱注册
    print("3. 测试无效邮箱注册...")
    invalid_email = "test@gmail.com"
    success, message = user_manager.register_user(invalid_email, test_password)
    print(f"   无效邮箱注册结果: {message}")
    
    # 测试重复邮箱注册
    print("4. 测试重复邮箱注册...")
    success, message = user_manager.register_user(test_email, test_password)
    print(f"   重复邮箱注册结果: {message}")
    
    print("用户系统测试完成")


if __name__ == "__main__":
    test_user_system()