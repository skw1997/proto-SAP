import psycopg2
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_db_password():
    """从环境变量获取数据库密码"""
    return os.getenv('DB_PASSWORD', 'your_password')

def create_database():
    """创建purchase_orders数据库"""
    try:
        # 先连接到默认的postgres数据库
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database='postgres',
            user=os.getenv('DB_USER', 'postgres'),
            password=get_db_password(),  # 从环境变量获取密码
            port=os.getenv('DB_PORT', '5432')
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # 检查数据库是否已存在
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'purchase_orders'")
        exists = cursor.fetchone()
        
        if not exists:
            # 创建数据库
            cursor.execute("CREATE DATABASE purchase_orders")
            print("✓ 数据库 purchase_orders 创建成功!")
        else:
            print("✓ 数据库 purchase_orders 已存在")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建数据库时出错: {e}")
        return False

def create_tables():
    """创建表结构"""
    try:
        # 连接到purchase_orders数据库
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database='purchase_orders',
            user=os.getenv('DB_USER', 'postgres'),
            password=get_db_password(),  # 从环境变量获取密码
            port=os.getenv('DB_PORT', '5432')
        )
        cursor = conn.cursor()
        
        # 创建Schema
        cursor.execute("CREATE SCHEMA IF NOT EXISTS purchase_orders")
        
        # 使用Schema
        cursor.execute("SET search_path TO purchase_orders")
        
        # 创建表
        create_table_sql = """
        -- WF Open 表
        CREATE TABLE IF NOT EXISTS wf_open (
            po VARCHAR(50),
            pn VARCHAR(50),
            line INTEGER,
            po_line VARCHAR(50) PRIMARY KEY,
            description TEXT,
            qty DECIMAL(10, 2),
            net_price DECIMAL(10, 2),
            total_price DECIMAL(10, 2),
            req_date_wf DATE,
            eta_wfsz DATE,
            shipping_mode VARCHAR(50),
            comment TEXT,
            po_placed_date DATE,
            purchaser VARCHAR(100),
            record_no VARCHAR(50),
            shipping_cost DECIMAL(10, 2),
            tracking_no VARCHAR(100),
            so_number VARCHAR(50),
            latest_departure_date DATE,
            chinese_name VARCHAR(100),
            unit VARCHAR(20)
        );

        -- WF Closed 表
        CREATE TABLE IF NOT EXISTS wf_closed (
            id SERIAL PRIMARY KEY,
            po VARCHAR(50),
            pn VARCHAR(50),
            line INTEGER,
            po_line VARCHAR(50),
            description TEXT,
            qty DECIMAL(10, 2),
            net_price DECIMAL(10, 2),
            total_price DECIMAL(10, 2),
            req_date_wf DATE,
            eta_wfsz DATE,
            shipping_mode VARCHAR(50),
            comment TEXT,
            po_placed_date DATE,
            purchaser VARCHAR(100),
            record_no VARCHAR(50),
            shipping_cost DECIMAL(10, 2),
            tracking_no VARCHAR(100),
            so_number VARCHAR(50),
            chinese_name VARCHAR(100),
            unit VARCHAR(20)
        );

        -- Non-WF Open 表
        CREATE TABLE IF NOT EXISTS non_wf_open (
            po VARCHAR(50),
            pn VARCHAR(50),
            description TEXT,
            qty DECIMAL(10, 2),
            net_price DECIMAL(10, 2),
            total_price DECIMAL(10, 2),
            req_date DATE,
            eta_wfsz DATE,
            shipping_mode VARCHAR(50),
            comment TEXT,
            po_placed_date DATE,
            qc_result VARCHAR(50),
            shipping_cost DECIMAL(10, 2),
            tracking_no VARCHAR(100),
            so_number VARCHAR(50),
            yes_not_paid VARCHAR(10),
            line VARCHAR(50),
            po_line VARCHAR(100) PRIMARY KEY
        );

        -- Non-WF Closed 表
        CREATE TABLE IF NOT EXISTS non_wf_closed (
            id SERIAL PRIMARY KEY,
            po VARCHAR(50),
            pn VARCHAR(50),
            description TEXT,
            qty DECIMAL(10, 2),
            net_price DECIMAL(10, 2),
            total_price DECIMAL(10, 2),
            req_date DATE,
            eta_wfsz DATE,
            shipping_mode VARCHAR(50),
            comment TEXT,
            po_placed_date DATE,
            purchaser VARCHAR(100),
            shipping_cost DECIMAL(10, 2),
            tracking_no VARCHAR(100),
            so_number VARCHAR(50),
            yes_not_paid VARCHAR(10),
            line VARCHAR(50),
            po_line VARCHAR(100)
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✓ 所有表创建成功!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ 创建表时出错: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL数据库和表创建工具")
    print("=" * 30)
    
    # 创建数据库
    if create_database():
        # 创建表
        if create_tables():
            print("\n✓ 数据库和表创建完成!")
            print("\n现在你可以:")
            print("1. 编辑 .env 文件，确保数据库连接信息正确")
            print("2. 运行 python test_db_connection.py 测试连接")
            print("3. 运行 python pdf_parser.py 解析PDF文件")
        else:
            print("\n✗ 表创建失败")
            sys.exit(1)
    else:
        print("\n✗ 数据库创建失败")
        sys.exit(1)