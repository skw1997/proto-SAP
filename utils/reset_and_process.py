import psycopg2
import os
from dotenv import load_dotenv
from backend.db_pdf_processor import extract_wefaricate_data, extract_centurion_data, insert_wf_open_data, insert_non_wf_open_data

# 加载环境变量
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

def connect_to_db():
    """连接到PostgreSQL数据库"""
    try:
        db_config = get_db_config()
        connection = psycopg2.connect(**db_config)
        return connection
    except Exception as error:
        print(f"连接数据库时出错: {error}")
        return None

def clear_existing_data():
    """清空现有的WF Open和Non-WF Open数据"""
    connection = connect_to_db()
    if not connection:
        return False
        
    try:
        cursor = connection.cursor()
        
        # 清空WF Open表
        cursor.execute("DELETE FROM purchase_orders.wf_open")
        print(f"已清空WF Open表中的 {cursor.rowcount} 条记录")
        
        # 清空Non-WF Open表
        cursor.execute("DELETE FROM purchase_orders.non_wf_open")
        print(f"已清空Non-WF Open表中的 {cursor.rowcount} 条记录")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"清空数据时出错: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False

def main():
    print("重置并重新处理PDF数据...")
    print("=" * 40)
    
    # 清空现有数据
    if clear_existing_data():
        print("数据清空成功")
    else:
        print("数据清空失败")
        return
    
    # 处理Wefaricate PDF
    wefaricate_pdf = "Purchase Order - 4500010647.pdf"
    print(f"\n处理 {wefaricate_pdf}...")
    wefaricate_data = extract_wefaricate_data(wefaricate_pdf)
    print(f"从Wefaricate PDF提取了 {len(wefaricate_data)} 条数据")
    
    # 处理Centurion PDF
    centurion_pdf = "Centurion Safety Products Purchase Order PO-100130.pdf"
    print(f"\n处理 {centurion_pdf}...")
    centurion_data = extract_centurion_data(centurion_pdf)
    print(f"从Centurion PDF提取了 {len(centurion_data)} 条数据")
    
    # 插入数据到数据库
    if wefaricate_data:
        insert_wf_open_data(wefaricate_data)
    
    if centurion_data:
        insert_non_wf_open_data(centurion_data)
    
    print("\n处理完成！")

if __name__ == "__main__":
    main()