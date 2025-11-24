import psycopg2
import json
import os

def get_db_config():
    """获取数据库配置信息"""
    print("PostgreSQL数据库配置设置")
    print("=" * 30)
    
    config = {
        'host': input("请输入数据库主机地址 (默认: localhost): ").strip() or 'localhost',
        'port': input("请输入数据库端口 (默认: 5432): ").strip() or '5432',
        'user': input("请输入数据库用户名 (默认: postgres): ").strip() or 'postgres',
        'password': input("请输入数据库密码: ").strip(),
        'database': input("请输入数据库名称 (默认: purchase_orders): ").strip() or 'purchase_orders'
    }
    
    return config

def test_db_connection(config):
    """测试数据库连接"""
    try:
        # 先测试连接到默认的postgres数据库
        test_config = config.copy()
        test_config['database'] = 'postgres'
        
        connection = psycopg2.connect(**test_config)
        print("✓ PostgreSQL服务连接成功!")
        connection.close()
        
        # 再测试连接到目标数据库
        connection = psycopg2.connect(**config)
        print("✓ 目标数据库连接成功!")
        connection.close()
        
        return True
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            print("✗ 密码认证失败，请检查用户名和密码")
        elif "Connection refused" in str(e):
            print("✗ 连接被拒绝，请确保PostgreSQL服务正在运行")
        elif "does not exist" in str(e):
            print("✗ 数据库不存在，需要先创建")
        else:
            print(f"✗ 连接错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 连接时发生未知错误: {e}")
        return False

def create_database(config):
    """创建数据库"""
    try:
        # 连接到默认的postgres数据库来创建新数据库
        test_config = config.copy()
        test_config['database'] = 'postgres'
        
        connection = psycopg2.connect(**test_config)
        connection.autocommit = True
        cursor = connection.cursor()
        
        # 检查数据库是否已存在
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (config['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {config['database']}")
            print(f"✓ 数据库 {config['database']} 创建成功!")
        else:
            print(f"✓ 数据库 {config['database']} 已存在")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"✗ 创建数据库时出错: {e}")
        return False

def save_config(config, filename='db_config.json'):
    """保存配置到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✓ 配置已保存到 {filename}")
        return True
    except Exception as e:
        print(f"✗ 保存配置时出错: {e}")
        return False

def load_config(filename='db_config.json'):
    """从文件加载配置"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✓ 已从 {filename} 加载配置")
            return config
        except Exception as e:
            print(f"✗ 加载配置时出错: {e}")
    return None

def main():
    print("PostgreSQL数据库配置工具")
    print("=" * 30)
    
    # 尝试加载现有配置
    config = load_config()
    
    if config:
        use_existing = input("发现现有配置，是否使用? (y/n, 默认: y): ").strip().lower()
        if use_existing != 'n':
            if test_db_connection(config):
                print("✓ 使用现有配置连接成功!")
                return config
            else:
                print("✗ 现有配置无法连接，需要重新配置")
    
    # 获取新的配置
    while True:
        config = get_db_config()
        
        # 测试连接
        if test_db_connection(config):
            print("✓ 数据库连接测试成功!")
            break
        else:
            retry = input("连接失败，是否重新输入配置? (y/n, 默认: y): ").strip().lower()
            if retry == 'n':
                return None
    
    # 保存配置
    save_config(config)
    
    # 创建数据库（如果不存在）
    create_database(config)
    
    return config

if __name__ == "__main__":
    config = main()
    if config:
        print("\n配置完成! 您现在可以运行以下命令来测试连接:")
        print("  python test_db_connection.py")
        print("\n或者直接运行PDF解析器:")
        print("  python pdf_parser.py")