import requests
import time
import psycopg2
import hashlib

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        database='purchase_orders',
        user='postgres',
        password='pgsql',
        port='5432'
    )

def check_user_status(user_id):
    """检查用户状态"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SET search_path TO purchase_orders')
    cur.execute('SELECT id, email, password_hash, is_verified FROM users WHERE id = %s', (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def test_full_user_flow():
    base_url = "http://localhost:5000"
    
    print("=== 测试用户完整流程 ===")
    
    # 1. 清理测试用户（如果存在）
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SET search_path TO purchase_orders')
    cur.execute("DELETE FROM users WHERE email = %s", ('kevin.shen@wefabricate.com',))
    conn.commit()
    cur.close()
    conn.close()
    print("1. 已清理测试用户")
    
    # 2. 注册用户
    print("\n2. 注册用户...")
    register_data = {
        "email": "kevin.shen@wefabricate.com",
        "password": "initial_password"
    }
    
    response = requests.post(f"{base_url}/api/user/register", json=register_data)
    print(f"   注册响应: {response.status_code} - {response.json()}")
    
    if response.status_code != 201:
        print("   注册失败，退出测试")
        return
    
    # 等待邮件发送
    time.sleep(3)
    
    # 3. 检查数据库状态（注册后）
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SET search_path TO purchase_orders')
    cur.execute("SELECT id, email, password_hash, is_verified, verification_token FROM users WHERE email = %s", ('kevin.shen@wefabricate.com',))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        user_id, email, password_hash, is_verified, verification_token = user
        print(f"   注册后用户状态: ID={user_id}, Email={email}, PasswordHash={password_hash}, IsVerified={is_verified}, Token={verification_token[:10] if verification_token else None}")
    else:
        print("   未找到注册用户")
        return
    
    # 4. 验证令牌
    print("\n3. 验证令牌...")
    response = requests.get(f"{base_url}/api/user/verify-email?token={verification_token}")
    print(f"   验证响应: {response.status_code} - {response.json()}")
    
    # 5. 设置密码
    print("\n4. 设置密码...")
    password_data = {
        "user_id": user_id,
        "password": "new_password_123"
    }
    
    response = requests.post(f"{base_url}/api/user/set-password", json=password_data)
    print(f"   设置密码响应: {response.status_code} - {response.json()}")
    
    # 6. 检查最终数据库状态
    print("\n5. 检查最终状态...")
    final_status = check_user_status(user_id)
    if final_status:
        final_user_id, final_email, final_password_hash, final_is_verified = final_status
        print(f"   最终用户状态: ID={final_user_id}, Email={final_email}, PasswordHash={'已设置' if final_password_hash else '未设置'}, IsVerified={final_is_verified}")
        
        if final_password_hash and final_is_verified:
            print("\n✅ 测试成功完成！用户已成功验证并设置密码。")
        else:
            print("\n❌ 测试失败！用户状态未正确更新。")
    else:
        print("\n❌ 测试失败！未找到用户。")

if __name__ == "__main__":
    test_full_user_flow()