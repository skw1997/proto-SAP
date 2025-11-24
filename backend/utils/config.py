import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_db_config():
    """获取数据库配置"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'purchase_orders_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'port': os.getenv('DB_PORT', '5432')
    }

def get_app_config():
    """获取应用配置"""
    return {
        'host': os.getenv('APP_HOST', '127.0.0.1'),
        'port': int(os.getenv('APP_PORT', '5000')),
        'debug': os.getenv('APP_DEBUG', 'True').lower() == 'true'
    }