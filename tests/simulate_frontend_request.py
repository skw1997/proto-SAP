#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟前端请求测试
"""

import sys
import os
import requests
import json

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def simulate_frontend_request():
    """模拟前端请求"""
    base_url = "http://localhost:5000"
    
    # 1. 注册用户
    print("1. 注册用户...")
    register_data = {
        "email": "test_frontend@wefabricate.com",
        "password": "frontendtest123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/user/register", 
                               json=register_data,
                               headers={"Content-Type": "application/json"})
        print(f"   注册响应状态: {response.status_code}")
        print(f"   注册响应数据: {response.json()}")
        
        if response.status_code != 201:
            print("   注册失败")
            return
            
    except Exception as e:
        print(f"   注册请求失败: {e}")
        return
    
    # 2. 为了测试，我们直接从数据库获取验证令牌
    try:
        # 连接数据库获取令牌
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            database='purchase_orders',
            user='postgres',
            password='pgsql',
            port='5432'
        )
        cursor = conn.cursor()
        
        select_query = """
        SELECT verification_token 
        FROM purchase_orders.users 
        WHERE email = %s
        """
        cursor.execute(select_query, (register_data["email"],))
        result = cursor.fetchone()
        
        if result:
            verification_token = result[0]
            print(f"   获取到验证令牌: {verification_token}")
        else:
            print("   未找到用户")
            return
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"   数据库查询失败: {e}")
        return
    
    # 3. 验证令牌
    print("2. 验证令牌...")
    try:
        response = requests.get(f"{base_url}/api/user/verify-email?token={verification_token}")
        print(f"   验证响应状态: {response.status_code}")
        print(f"   验证响应数据: {response.json()}")
        
        if response.status_code != 200:
            print("   验证失败")
            return
            
        user_data = response.json()
        user_id = user_data["user"]["user_id"]
        print(f"   获取到用户ID: {user_id}")
        
    except Exception as e:
        print(f"   验证请求失败: {e}")
        return
    
    # 4. 设置密码
    print("3. 设置密码...")
    set_password_data = {
        "user_id": user_id,
        "password": "newpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/user/set-password",
                               json=set_password_data,
                               headers={"Content-Type": "application/json"})
        print(f"   设置密码响应状态: {response.status_code}")
        print(f"   设置密码响应数据: {response.json()}")
        
        if response.status_code == 200:
            print("✓ 前端请求模拟测试成功")
        else:
            print("✗ 设置密码失败")
            
    except Exception as e:
        print(f"   设置密码请求失败: {e}")
    
    # 5. 检查数据库中的最终状态
    print("4. 检查数据库中的最终状态...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='purchase_orders',
            user='postgres',
            password='pgsql',
            port='5432'
        )
        cursor = conn.cursor()
        
        select_query = """
        SELECT id, email, password_hash, is_verified, verification_token 
        FROM purchase_orders.users 
        WHERE email = %s
        """
        cursor.execute(select_query, (register_data["email"],))
        result = cursor.fetchone()
        
        if result:
            user_id, email, password_hash, is_verified, verification_token = result
            print(f"   用户ID: {user_id}")
            print(f"   邮箱: {email}")
            print(f"   密码哈希: {'已设置' if password_hash else '未设置'}")
            print(f"   已验证: {is_verified}")
            print(f"   验证令牌: {'已清除' if not verification_token else '未清除'}")
            
            if password_hash and is_verified and not verification_token:
                print("✓ 数据库状态正确")
            else:
                print("✗ 数据库状态不正确")
        else:
            print("   未找到用户")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"   数据库查询失败: {e}")


if __name__ == "__main__":
    simulate_frontend_request()