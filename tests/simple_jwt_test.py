import jwt
import datetime

# 简单测试
SECRET_KEY = 'test_secret'

# 不使用iat字段
future_time = datetime.datetime.now() + datetime.timedelta(hours=1)

payload = {
    'user_id': 1,
    'exp': future_time
    # 移除iat字段
}

print(f"Payload: {payload}")
print(f"当前时间: {datetime.datetime.now()}")

# 生成token
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
print(f"生成的token: {token}")

# 验证token
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"require": ["exp"]})
    print(f"解码成功: {decoded}")
except Exception as e:
    print(f"解码失败: {e}")
    import traceback
    traceback.print_exc()