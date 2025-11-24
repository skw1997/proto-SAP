import requests
import time
import psycopg2

def test_user_registration_flow():
    # 1. 注册新用户
    print("=== 测试用户注册流程 ===")
    
    # 使用新的邮箱地址
    email = "testflow@wefabricate.com"
    password = "testpassword123"
    
    print(f"1. 注册用户: {email}")
    register_data = {
        'email': email,
        'password': password
    }
    
    try:
        response = requests.post('http://localhost:5000/api/user/register', json=register_data)
        print(f"   注册响应: {response.status_code} - {response.json()}")
        
        if response.status_code != 201:
            print("   注册失败，退出测试")
            return
            
    except Exception as e:
        print(f"   注册请求失败: {e}")
        return
    
    # 等待几秒确保邮件发送完成
    time.sleep(3)
    
    # 2. 从数据库获取验证令牌
    print("2. 获取验证令牌")
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='purchase_orders',
            user='postgres',
            password='pgsql',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute('SET search_path TO purchase_orders')
        cur.execute('SELECT verification_token FROM users WHERE email = %s', (email,))
        token_result = cur.fetchone()
        cur.close()
        conn.close()
        
        if not token_result:
            print("   未找到用户或令牌")
            return
            
        token = token_result[0]
        print(f"   获取到令牌: {token}")
        
    except Exception as e:
        print(f"   获取令牌失败: {e}")
        return
    
    # 3. 验证令牌
    print("3. 验证令牌")
    try:
        response = requests.get(f'http://localhost:5000/api/user/verify-email?token={token}')
        print(f"   验证响应: {response.status_code} - {response.json()}")
        
        if response.status_code != 200:
            print("   令牌验证失败，退出测试")
            return
            
        user_info = response.json().get('user', {})
        user_id = user_info.get('user_id')
        user_email = user_info.get('email')
        print(f"   用户信息: ID={user_id}, Email={user_email}")
        
    except Exception as e:
        print(f"   令牌验证失败: {e}")
        return
    
    # 4. 设置密码
    print("4. 设置密码")
    password_data = {
        'user_id': user_id,
        'password': 'newpassword123'
    }
    
    try:
        response = requests.post('http://localhost:5000/api/user/set-password', json=password_data)
        print(f"   设置密码响应: {response.status_code} - {response.json()}")
        
        if response.status_code != 200:
            print("   设置密码失败")
            return
            
    except Exception as e:
        print(f"   设置密码请求失败: {e}")
        return
    
    # 5. 检查数据库最终状态
    print("5. 检查数据库最终状态")
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='purchase_orders',
            user='postgres',
            password='pgsql',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute('SET search_path TO purchase_orders')
        cur.execute('SELECT id, email, password_hash, is_verified FROM users WHERE id = %s', (user_id,))
        user_result = cur.fetchone()
        cur.close()
        conn.close()
        
        if user_result:
            user_id_db, email_db, password_hash_db, is_verified_db = user_result
            print(f"   数据库用户状态:")
            print(f"     ID: {user_id_db}")
            print(f"     邮箱: {email_db}")
            print(f"     密码哈希: {password_hash_db[:20]}..." if password_hash_db else "     密码哈希: None")
            print(f"     已验证: {is_verified_db}")
        else:
            print("   未找到用户记录")
            
    except Exception as e:
        print(f"   检查数据库状态失败: {e}")

if __name__ == "__main__":
    test_user_registration_flow()