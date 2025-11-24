import psycopg2
from psycopg2 import sql
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.env_db_config import get_db_config

def update_table_structure():
    """更新表结构，添加自增序号字段作为主键"""
    db_config = get_db_config()
    
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        # 设置搜索路径
        cursor.execute("SET search_path TO purchase_orders")
        
        # 为 wf_closed 表添加自增序号字段
        print("正在更新 wf_closed 表...")
        
        # 1. 添加自增序号字段
        cursor.execute("ALTER TABLE wf_closed ADD COLUMN id SERIAL")
        
        # 2. 去除现有的主键约束
        cursor.execute("ALTER TABLE wf_closed DROP CONSTRAINT wf_closed_pkey")
        
        # 3. 将 id 字段设为主键
        cursor.execute("ALTER TABLE wf_closed ADD PRIMARY KEY (id)")
        
        print("wf_closed 表更新完成")
        
        # 为 non_wf_closed 表添加自增序号字段
        print("正在更新 non_wf_closed 表...")
        
        # 1. 添加自增序号字段
        cursor.execute("ALTER TABLE non_wf_closed ADD COLUMN id SERIAL")
        
        # 2. 去除现有的主键约束
        cursor.execute("ALTER TABLE non_wf_closed DROP CONSTRAINT non_wf_closed_pkey")
        
        # 3. 将 id 字段设为主键
        cursor.execute("ALTER TABLE non_wf_closed ADD PRIMARY KEY (id)")
        
        print("non_wf_closed 表更新完成")
        
        # 提交更改
        connection.commit()
        print("所有表结构更新完成")
        
    except Exception as error:
        print(f"更新表结构时出错: {error}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    update_table_structure()