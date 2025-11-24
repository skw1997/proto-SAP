#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试用户验证问题
"""

import sys
import os
import psycopg2

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


def debug_user_verification():
    """调试用户验证问题"""
    print("开始调试用户验证问题...")
    
    # 创建用户管理器
    user_manager = UserManager()
    
    try:
        # 连接数据库
        conn = user_manager.get_connection()
        if not conn:
            print("无法连接到数据库")
            return
            
        cursor = conn.cursor()
        
        # 查找最近注册的用户
        select_query = """
        SELECT id, email, password_hash, is_verified, verification_token 
        FROM purchase_orders.users 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        cursor.execute(select_query)
        user = cursor.fetchone()
        
        if user:
            user_id, email, password_hash, is_verified, verification_token = user
            print(f"最近注册的用户:")
            print(f"  用户ID: {user_id}")
            print(f"  邮箱: {email}")
            print(f"  密码哈希: {password_hash}")
            print(f"  已验证: {is_verified}")
            print(f"  验证令牌: {verification_token}")
            
            # 尝试设置密码
            print("\n尝试设置密码...")
            test_password = "testpassword123"
            success, message = user_manager.set_user_password(user_id, test_password)
            print(f"  设置密码结果: {success}, {message}")
            
            if not success:
                print(f"  错误详情: {message}")
                
                # 检查用户是否存在
                check_query = """
                SELECT id, email, is_verified 
                FROM purchase_orders.users 
                WHERE id = %s
                """
                cursor.execute(check_query, (user_id,))
                check_user = cursor.fetchone()
                
                if check_user:
                    check_user_id, check_email, check_is_verified = check_user
                    print(f"  检查用户: ID={check_user_id}, 邮箱={check_email}, 已验证={check_is_verified}")
                else:
                    print(f"  用户 {user_id} 不存在")
            
            # 再次查询用户状态
            cursor.execute(select_query)
            user = cursor.fetchone()
            if user:
                user_id, email, password_hash, is_verified, verification_token = user
                print(f"\n更新后的用户状态:")
                print(f"  用户ID: {user_id}")
                print(f"  邮箱: {email}")
                print(f"  密码哈希: {password_hash}")
                print(f"  已验证: {is_verified}")
                print(f"  验证令牌: {verification_token}")
            
        else:
            print("没有找到用户")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"调试时出错: {e}")


if __name__ == "__main__":
    debug_user_verification()