#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户验证流程测试脚本
"""

import sys
import os

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


def test_user_verification_flow():
    """测试用户验证完整流程"""
    print("开始测试用户验证完整流程...")
    
    # 创建用户管理器
    user_manager = UserManager()
    
    # 1. 注册用户
    print("1. 注册用户...")
    test_email = "test_verify@wefabricate.com"
    test_password = "testpassword123"
    
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
    
    # 4. 检查数据库中的用户状态
    print("4. 检查数据库中的用户状态...")
    try:
        conn = user_manager.get_connection()
        if conn:
            cursor = conn.cursor()
            
            select_query = """
            SELECT id, email, password_hash, is_verified, verification_token 
            FROM purchase_orders.users 
            WHERE id = %s
            """
            cursor.execute(select_query, (user_id,))
            user = cursor.fetchone()
            
            if user:
                user_id, email, password_hash, is_verified, verification_token = user
                print(f"   用户ID: {user_id}")
                print(f"   邮箱: {email}")
                print(f"   密码哈希: {'已设置' if password_hash else '未设置'}")
                print(f"   已验证: {is_verified}")
                print(f"   验证令牌: {'已清除' if not verification_token else '未清除'}")
                
                if password_hash and is_verified and not verification_token:
                    print("✓ 用户验证流程成功完成")
                else:
                    print("✗ 用户验证流程未正确完成")
            else:
                print("   未找到用户")
                
            cursor.close()
            conn.close()
        else:
            print("   无法连接到数据库")
        
    except Exception as e:
        print(f"   检查数据库时出错: {e}")
    
    print("用户验证流程测试完成")


if __name__ == "__main__":
    test_user_verification_flow()