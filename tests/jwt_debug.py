import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

import jwt
import datetime
import os

# 从环境变量获取密钥
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'wefabricate_default_secret_key')
print(f"使用的密钥: {SECRET_KEY}")

# 获取当前时间
now = datetime.datetime.now()
print(f"当前系统时间: {now}")

# 生成token
user_id = 42
email = "tokentest@wefabricate.com"
payload = {
    'user_id': user_id,
    'email': email,
    'exp': now + datetime.timedelta(hours=24),
    'iat': now - datetime.timedelta(minutes=5)
}
print(f"Payload: {payload}")

try:
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print(f"生成的token: {token}")
    
    # 验证token
    print("开始验证token...")
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], leeway=60)
    print(f"解码后的payload: {decoded_payload}")
    print("Token验证成功!")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()