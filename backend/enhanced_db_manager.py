import psycopg2
from psycopg2 import sql
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.env_db_config import get_db_config
import hashlib
import time
from datetime import datetime
import pandas as pd

class DatabaseManager:
    def __init__(self):
        self.db_config = get_db_config()
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except Exception as error:
            print(f"数据库连接失败: {error}")
            return None
    
    def query_table(self, table_name):
        """查询指定表的数据"""
        conn = self.get_connection()
        if not conn:
            return None, None
        
        try:
            cursor = conn.cursor()
            query = sql.SQL("SELECT * FROM purchase_orders.{}").format(
                sql.Identifier(table_name)
            )
            cursor.execute(query)
            records = cursor.fetchall()
            
            # 获取列名
            colnames = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            return colnames, records
        except Exception as error:
            print(f"查询表 {table_name} 时出错: {error}")
            return None, None
    
    def generate_row_hash(self, row_data):
        """为行数据生成哈希值用于版本控制"""
        # 将行数据转换为字符串并生成哈希
        row_str = str(sorted(row_data.items()))
        return hashlib.md5(row_str.encode()).hexdigest()
    
    def update_row_with_version(self, table_name, pn, updates, expected_hash):
        """
        更新表中的数据（带版本控制）
        
        Args:
            table_name: 表名
            pn: 主键值
            updates: 要更新的字段字典 {column_name: new_value}
            expected_hash: 预期的行数据哈希值
            
        Returns:
            tuple: (success, message)
        """
        conn = self.get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        try:
            cursor = conn.cursor()
            
            # 确定主键字段
            primary_key_field = 'id'  # 默认使用新的自增主键
            primary_key_value = pn
            
            if table_name in ['wf_open']:
                primary_key_field = 'po_line'
            elif table_name in ['wf_closed', 'non_wf_closed']:
                # 对于这些表，我们仍然使用pn作为业务主键进行查找
                primary_key_field = 'pn'
            
            # 首先检查当前数据是否与预期的哈希值匹配
            select_query = sql.SQL("SELECT * FROM purchase_orders.{} WHERE {} = %s").format(
                sql.Identifier(table_name),
                sql.Identifier(primary_key_field)
            )
            cursor.execute(select_query, (primary_key_value,))
            current_record = cursor.fetchone()
            
            if current_record:
                # 获取列名
                colnames = [desc[0] for desc in cursor.description]
                # 构建当前行数据字典
                current_row_data = dict(zip(colnames, current_record))
                # 生成当前数据的哈希值
                current_hash = self.generate_row_hash(current_row_data)
                
                # 检查哈希值是否匹配
                if current_hash != expected_hash:
                    cursor.close()
                    conn.close()
                    return False, "数据已被其他用户修改，请刷新页面后重试"
            
            # 构建更新查询
            set_clauses = []
            values = []
            for column_name, new_value in updates.items():
                set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(column_name)))
                # 处理日期字段的特殊格式
                if column_name in ['req_date_wf', 'eta_wfsz', 'latest_departure_date', 'po_placed_date']:
                    if new_value is None or new_value == '' or new_value == 'None' or new_value == 'nan':
                        values.append(None)
                    else:
                        # 如果是日期字符串，直接使用
                        values.append(new_value)
                else:
                    # 处理其他字段的空值
                    if new_value == 'None' or new_value == 'nan':
                        values.append(None)
                    else:
                        values.append(new_value)
            
            # 添加主键值
            values.append(primary_key_value)
            
            update_query = sql.SQL("UPDATE purchase_orders.{} SET {} WHERE {} = %s").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(set_clauses),
                sql.Identifier(primary_key_field)
            )
            
            # 执行更新
            cursor.execute(update_query, values)
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                return True, f"更新成功，影响了 {affected_rows} 行"
            else:
                return False, "未找到要更新的记录或数据未发生变化"
        except Exception as error:
            if conn:
                conn.rollback()
                if cursor:
                    cursor.close()
                conn.close()
            return False, f"更新数据时出错: {error}"
    
    def delete_row_with_version(self, table_name, pn, expected_hash):
        """
        删除表中的数据（带版本控制）
        
        Args:
            table_name: 表名
            pn: 主键值
            expected_hash: 预期的行数据哈希值
            
        Returns:
            tuple: (success, message)
        """
        conn = self.get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        try:
            cursor = conn.cursor()
            
            # 确定主键字段
            primary_key_field = 'id'  # 默认使用新的自增主键
            primary_key_value = pn
            
            if table_name in ['wf_open']:
                primary_key_field = 'po_line'
            elif table_name in ['wf_closed', 'non_wf_closed']:
                # 对于这些表，我们仍然使用pn作为业务主键进行查找
                primary_key_field = 'pn'
            
            # 首先检查当前数据是否与预期的哈希值匹配
            select_query = sql.SQL("SELECT * FROM purchase_orders.{} WHERE {} = %s").format(
                sql.Identifier(table_name),
                sql.Identifier(primary_key_field)
            )
            cursor.execute(select_query, (primary_key_value,))
            current_record = cursor.fetchone()
            
            if current_record:
                # 获取列名
                colnames = [desc[0] for desc in cursor.description]
                # 构建当前行数据字典
                current_row_data = dict(zip(colnames, current_record))
                # 生成当前数据的哈希值
                current_hash = self.generate_row_hash(current_row_data)
                
                # 检查哈希值是否匹配
                if current_hash != expected_hash:
                    cursor.close()
                    conn.close()
                    return False, "数据已被其他用户修改，请刷新页面后重试"
            
            # 执行删除
            delete_query = sql.SQL("DELETE FROM purchase_orders.{} WHERE {} = %s").format(
                sql.Identifier(table_name),
                sql.Identifier(primary_key_field)
            )
            cursor.execute(delete_query, (primary_key_value,))
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                return True, f"删除成功，影响了 {affected_rows} 行"
            else:
                return False, "未找到要删除的记录"
        except Exception as error:
            if conn:
                conn.rollback()
                if cursor:
                    cursor.close()
                conn.close()
            return False, f"删除数据时出错: {error}"
    
    def insert_row(self, table_name, data):
        """
        插入新行数据
        
        Args:
            table_name: 表名
            data: 要插入的数据字典 {column_name: value}
            
        Returns:
            tuple: (success, message)
        """
        conn = self.get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        try:
            cursor = conn.cursor()
            
            # 清理数据中的特殊值
            cleaned_data = {}
            for k, v in data.items():
                if v == 'None' or v == 'nan' or v == '':
                    cleaned_data[k] = None
                else:
                    cleaned_data[k] = v
            
            # 构建插入查询
            columns = list(cleaned_data.keys())
            values = list(cleaned_data.values())
            placeholders = sql.SQL(", ").join(sql.Placeholder() * len(columns))
            
            insert_query = sql.SQL("INSERT INTO purchase_orders.{} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(sql.Identifier(col) for col in columns),
                placeholders
            )
            
            cursor.execute(insert_query, values)
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                return True, f"插入成功，影响了 {affected_rows} 行"
            else:
                return False, "插入失败"
        except Exception as error:
            if conn:
                conn.rollback()
                if cursor:
                    cursor.close()
                conn.close()
            return False, f"插入数据时出错: {error}"

# 创建全局数据库管理器实例
db_manager = DatabaseManager()