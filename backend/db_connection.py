import psycopg2
from psycopg2 import sql
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.env_db_config import get_db_config

# 数据库连接参数从环境变量获取
DB_CONFIG = get_db_config()

def connect_to_db():
    """连接到PostgreSQL数据库"""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print("成功连接到数据库")
        return connection
    except Exception as error:
        print(f"连接数据库时出错: {error}")
        return None

def query_table(connection, table_name):
    """查询指定表的所有数据"""
    try:
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM purchase_orders.{}").format(
            sql.Identifier(table_name)
        )
        cursor.execute(query)
        records = cursor.fetchall()
        
        # 获取列名
        colnames = [desc[0] for desc in cursor.description]
        print(f"表 {table_name} 的列名: {colnames}")
        print(f"表 {table_name} 的数据:")
        for record in records:
            print(record)
            
        cursor.close()
        return records
    except Exception as error:
        print(f"查询表 {table_name} 时出错: {error}")
        return None

def insert_sample_data(connection):
    """插入示例数据"""
    try:
        cursor = connection.cursor()
        
        # 插入WF Open表示例数据
        insert_query = """
        INSERT INTO purchase_orders.wf_open 
        (po, pn, line, po_line, description, qty, net_price, total_price, 
         req_date_wf, eta_wfsz, shipping_mode, comment, po_placed_date, 
         purchaser, record_no, shipping_cost, tracking_no, so_number, latest_departure_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (pn) DO NOTHING
        """
        
        sample_data = (
            'PO-1001', 'PN-2001', 1, 'PO-1001/1', '安全帽', 100, 50.00, 5000.00,
            '2023-01-15', '2023-02-01', '海运', '紧急订单', '2023-01-10',
            '张三', 'REC-001', 500.00, 'TRK-123456', 'SO-1001', '2023-01-25'
        )
        
        cursor.execute(insert_query, sample_data)
        connection.commit()
        print("示例数据插入成功")
        cursor.close()
    except Exception as error:
        print(f"插入示例数据时出错: {error}")

if __name__ == "__main__":
    # 连接数据库
    conn = connect_to_db()
    
    if conn:
        # 插入示例数据
        insert_sample_data(conn)
        
        # 查询各表数据
        query_table(conn, 'wf_open')
        query_table(conn, 'wf_closed')
        query_table(conn, 'non_wf_open')
        query_table(conn, 'non_wf_closed')
        
        # 关闭连接
        conn.close()
        print("数据库连接已关闭")