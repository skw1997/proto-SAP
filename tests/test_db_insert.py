import psycopg2
import os
from dotenv import load_dotenv
from backend.db_pdf_processor import extract_wefaricate_data

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

def test_database_insert():
    """测试数据库插入过程"""
    pdf_path = "pdf_samples/Purchase Order - 4500010045.pdf"
    
    print("=== 测试数据库插入 ===")
    data = extract_wefaricate_data(pdf_path)
    
    # 确保每条数据都有po_line字段
    for entry in data:
        if not entry.get('po_line') and entry.get('po') and entry.get('line'):
            entry['po_line'] = f"{entry['po']}/{entry['line']}"
        print(f"  PO: {entry['po']}, Line: {entry['line']}, PN: {entry['pn']}, PO Line: {entry['po_line']}")
    
    print(f"准备插入 {len(data)} 条数据")
    
    # 连接数据库
    try:
        db_config = get_db_config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        print("成功连接到数据库")
        
        # 插入数据
        success_count = 0
        error_count = 0
        
        for entry in data:
            try:
                # 使用INSERT ... ON CONFLICT语句，直接使用字段名
                insert_query = """
                INSERT INTO purchase_orders.wf_open 
                (po, pn, line, po_line, description, qty, net_price, total_price, 
                 req_date_wf, po_placed_date, purchaser)
                VALUES (%(po)s, %(pn)s, %(line)s, %(po_line)s, %(description)s, %(qty)s, %(net_price)s, %(total_price)s, 
                        %(req_date_wf)s, %(po_placed_date)s, %(purchaser)s)
                ON CONFLICT (po_line) DO UPDATE SET
                    po = EXCLUDED.po,
                    pn = EXCLUDED.pn,
                    line = EXCLUDED.line,
                    description = EXCLUDED.description,
                    qty = EXCLUDED.qty,
                    net_price = EXCLUDED.net_price,
                    total_price = EXCLUDED.total_price,
                    req_date_wf = EXCLUDED.req_date_wf,
                    po_placed_date = EXCLUDED.po_placed_date,
                    purchaser = EXCLUDED.purchaser
                """
                
                cursor.execute(insert_query, entry)
                success_count += 1
                print(f"  成功插入/更新数据: PO={entry['po']}, Line={entry['line']}")
                
            except Exception as e:
                error_count += 1
                print(f"  插入数据时出错: {e}")
                print(f"  出错数据: {entry}")
        
        # 提交事务
        connection.commit()
        print(f"\n数据插入完成: 成功 {success_count} 条, 失败 {error_count} 条")
        
    except Exception as e:
        print(f"数据库连接或操作出错: {e}")
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    test_database_insert()