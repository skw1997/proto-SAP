#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
更新数据库结构脚本
"""

import psycopg2
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.config import get_db_config

def update_database_structure():
    """更新数据库结构，添加操作记录表"""
    db_config = get_db_config()
    
    try:
        # 连接数据库
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # 创建Schema（如果不存在）
        cursor.execute("CREATE SCHEMA IF NOT EXISTS purchase_orders")
        
        # 使用Schema
        cursor.execute("SET search_path TO purchase_orders")
        
        # 创建操作记录表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS po_records (
            id SERIAL PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            table_name VARCHAR(100) NOT NULL,
            operation VARCHAR(20) NOT NULL, -- 'insert', 'update', 'delete'
            record_data JSONB NOT NULL,
            operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        
        # 创建索引以提高查询性能
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_po_records_user_email ON po_records(user_email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_po_records_table_name ON po_records(table_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_po_records_operation ON po_records(operation)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_po_records_operation_time ON po_records(operation_time)")
        
        # 提交更改
        conn.commit()
        cursor.close()
        conn.close()
        
        print("数据库结构更新成功")
        return True
        
    except Exception as e:
        print(f"更新数据库结构时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始更新数据库结构...")
    
    if update_database_structure():
        print("✓ 数据库结构更新完成")
    else:
        print("✗ 数据库结构更新失败")
        sys.exit(1)

if __name__ == "__main__":
    main()