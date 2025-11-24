import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 从环境变量获取密钥，如果没有则使用默认值
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'wefabricate_default_secret_key')

def generate_token(user_id, email):
    """
    生成JWT token
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=24)  # token 24小时后过期
        # 移除iat字段以避免时钟偏差问题
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """
    验证JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"require": ["exp"]})
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Token已过期'
    except jwt.InvalidTokenError as e:
        return False, f'无效的Token: {str(e)}'

def token_required(f):
    """
    装饰器：验证请求中的token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头中获取token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # 期望格式: Bearer <token>
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'error': 'Token格式错误'}), 401
        
        if not token:
            return jsonify({'success': False, 'error': '缺少Token'}), 401
        
        success, result = verify_token(token)
        if not success:
            return jsonify({'success': False, 'error': result}), 401
        
        # 将用户信息添加到请求上下文中
        request.current_user = result
        return f(*args, **kwargs)
    
    return decorated