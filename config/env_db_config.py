import psycopg2
import os
from dotenv import load_dotenv, set_key

# 尝试加载.env文件
load_dotenv()

def get_db_config():
    """从环境变量获取数据库配置"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'purchase_orders'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', '5432')
    }

def setup_env_config():
    """设置环境变量配置"""
    print("PostgreSQL数据库环境变量配置")
    print("=" * 35)
    
    # 获取配置值
    host = input(f"数据库主机地址 (默认: {os.getenv('DB_HOST', 'localhost')}): ").strip() or os.getenv('DB_HOST', 'localhost')
    port = input(f"数据库端口 (默认: {os.getenv('DB_PORT', '5432')}): ").strip() or os.getenv('DB_PORT', '5432')
    user = input(f"数据库用户名 (默认: {os.getenv('DB_USER', 'postgres')}): ").strip() or os.getenv('DB_USER', 'postgres')
    password = input("数据库密码: ").strip()
    database = input(f"数据库名称 (默认: {os.getenv('DB_NAME', 'purchase_orders')}): ").strip() or os.getenv('DB_NAME', 'purchase_orders')
    
    # 保存到.env文件
    set_key('.env', 'DB_HOST', host)
    set_key('.env', 'DB_PORT', port)
    set_key('.env', 'DB_USER', user)
    set_key('.env', 'DB_PASSWORD', password)
    set_key('.env', 'DB_NAME', database)
    
    print("✓ 配置已保存到 .env 文件")
    
    # 重新加载环境变量
    load_dotenv(override=True)
    
    return get_db_config()

def test_connection(config=None):
    """测试数据库连接"""
    if config is None:
        config = get_db_config()
    
    print(f"测试连接到: {config['host']}:{config['port']}")
    print(f"数据库: {config['database']}")
    print(f"用户: {config['user']}")
    
    try:
        connection = psycopg2.connect(**config)
        print("✓ 数据库连接成功!")
        
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL版本: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            print("✗ 密码认证失败")
            print("  请检查用户名和密码是否正确")
        elif "Connection refused" in str(e):
            print("✗ 连接被拒绝")
            print("  请确保PostgreSQL服务正在运行")
        elif "does not exist" in str(e):
            print("✗ 数据库不存在")
            print("  请先创建数据库")
        else:
            print(f"✗ 连接错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 连接时发生错误: {e}")
        return False

def create_env_file():
    """创建默认的.env文件"""
    default_env = """# PostgreSQL数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=purchase_orders
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(default_env)
        print("✓ 已创建默认 .env 配置文件")
        print("  请编辑 .env 文件填写正确的数据库连接信息")
    else:
        print("✓ .env 文件已存在")

if __name__ == "__main__":
    print("PostgreSQL数据库环境变量配置工具")
    print("=" * 35)
    
    # 创建.env文件（如果不存在）
    create_env_file()
    
    # 测试当前配置
    print("\n测试当前配置:")
    config = get_db_config()
    if not test_connection(config):
        print("\n配置测试失败，建议:")
        print("1. 编辑 .env 文件修改数据库连接信息")
        print("2. 或运行 python env_db_config.py --setup 来重新配置")
        
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == '--setup':
            setup_env_config()
            test_connection()