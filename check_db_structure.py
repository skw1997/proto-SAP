#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构的脚本
"""

import psycopg2
import os
from dotenv import load_dotenv

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

def check_table_structure(cursor, table_name):
    """检查表结构"""
    print(f"\n=== {table_name} 表结构 ===")
    
    # 获取列信息
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_schema = 'purchase_orders' AND table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))
    
    columns = cursor.fetchall()
    print("列信息:")
    for col in columns:
        print(f"  {col[0]}: {col[1]} (可空: {col[2]}, 默认值: {col[3]})")
    
    # 获取主键信息
    cursor.execute("""
        SELECT tc.constraint_name, kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_schema = 'purchase_orders' 
        AND tc.table_name = %s 
        AND tc.constraint_type = 'PRIMARY KEY'
    """, (table_name,))
    
    primary_keys = cursor.fetchall()
    print("主键:")
    for pk in primary_keys:
        print(f"  约束名: {pk[0]}, 列名: {pk[1]}")
    
    # 获取唯一约束信息
    cursor.execute("""
        SELECT tc.constraint_name, kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_schema = 'purchase_orders' 
        AND tc.table_name = %s 
        AND tc.constraint_type = 'UNIQUE'
    """, (table_name,))
    
    unique_constraints = cursor.fetchall()
    print("唯一约束:")
    for uc in unique_constraints:
        print(f"  约束名: {uc[0]}, 列名: {uc[1]}")

def main():
    """主函数"""
    print("检查数据库表结构...")
    
    try:
        # 连接数据库
        db_config = get_db_config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        print("✓ 成功连接到数据库")
        
        # 检查所有表的结构
        tables = ['wf_open', 'wf_closed', 'non_wf_open', 'non_wf_closed']
        for table in tables:
            check_table_structure(cursor, table)
        
    except Exception as e:
        print(f"✗ 检查数据库结构时出错: {e}")
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("\n✓ 数据库连接已关闭")

if __name__ == "__main__":
    main()