import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.utils.config import get_db_config
import psycopg2

def create_tables():
    """创建数据库表"""
    print("创建数据库表...")
    
    try:
        # 获取数据库配置
        config = get_db_config()
        print(f"数据库配置: {config}")
        
        # 连接到目标数据库
        connection = psycopg2.connect(**config)
        cursor = connection.cursor()
        
        # 创建Schema
        print("创建Schema...")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS purchase_orders")
        
        # 使用Schema
        cursor.execute("SET search_path TO purchase_orders")
        
        # 创建WF Open表
        print("创建WF Open表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wf_open (
                po VARCHAR(50),
                pn VARCHAR(50) PRIMARY KEY,
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
                latest_departure_date DATE
            )
        """)
        
        # 创建WF Closed表
        print("创建WF Closed表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wf_closed (
                po VARCHAR(50),
                pn VARCHAR(50) PRIMARY KEY,
                line INTEGER,
                pn_line VARCHAR(50),
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
            )
        """)
        
        # 创建Non-WF Open表
        print("创建Non-WF Open表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS non_wf_open (
                po VARCHAR(50),
                pn VARCHAR(50) PRIMARY KEY,
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
                yes_not_paid VARCHAR(10)
            )
        """)
        
        # 创建Non-WF Closed表
        print("创建Non-WF Closed表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS non_wf_closed (
                po VARCHAR(50),
                pn VARCHAR(50) PRIMARY KEY,
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
                yes_not_paid VARCHAR(10)
            )
        """)
        
        # 提交更改
        connection.commit()
        print("✓ 所有表创建成功!")
        
        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print(f"✗ 创建表时出错: {e}")
        return False

if __name__ == "__main__":
    create_tables()