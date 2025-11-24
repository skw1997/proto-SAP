import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.utils.jwt_utils import generate_token, verify_token

# 测试token生成和验证
print("=== JWT Token测试 ===")

# 生成token
user_id = 42
email = "tokentest@wefabricate.com"
token = generate_token(user_id, email)
print(f"生成的token: {token}")

# 验证token
success, result = verify_token(token)
print(f"验证结果: success={success}, result={result}")

# 测试无效token
invalid_token = "invalid.token.here"
success, result = verify_token(invalid_token)
print(f"无效token验证结果: success={success}, result={result}")