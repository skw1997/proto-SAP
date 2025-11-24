import json
import psycopg2
from psycopg2 import sql
from backend.utils.config import get_db_config

class OperationLogger:
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
    
    def log_operation(self, user_email, table_name, operation, record_data):
        """
        记录用户操作
        
        Args:
            user_email: 用户邮箱
            table_name: 表名
            operation: 操作类型 ('insert', 'update', 'delete')
            record_data: 记录数据 (dict)
            
        Returns:
            bool: 是否成功记录
        """
        conn = self.get_connection()
        if not conn:
            print("无法获取数据库连接")
            return False
        
        try:
            cursor = conn.cursor()
            
            # 将记录数据转换为JSON字符串
            record_json = json.dumps(record_data, default=str)
            
            # 插入操作记录
            insert_query = """
                INSERT INTO purchase_orders.po_records 
                (user_email, table_name, operation, record_data)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_email, table_name, operation, record_json))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except Exception as error:
            print(f"记录操作时出错: {error}")
            if conn:
                try:
                    conn.rollback()
                    cursor.close()
                    conn.close()
                except:
                    pass
            return False
    
    def get_operation_logs(self, user_email=None, table_name=None, operation=None, limit=100):
        """
        获取操作日志
        
        Args:
            user_email: 用户邮箱（可选）
            table_name: 表名（可选）
            operation: 操作类型（可选）
            limit: 限制返回记录数
            
        Returns:
            list: 操作日志列表
        """
        conn = self.get_connection()
        if not conn:
            print("无法获取数据库连接")
            return []
        
        try:
            cursor = conn.cursor()
            
            # 构建查询条件
            conditions = []
            params = []
            
            if user_email:
                conditions.append("user_email = %s")
                params.append(user_email)
            
            if table_name:
                conditions.append("table_name = %s")
                params.append(table_name)
            
            if operation:
                conditions.append("operation = %s")
                params.append(operation)
            
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            # 查询操作记录
            query = f"""
                SELECT id, user_email, table_name, operation, record_data, operation_time
                FROM purchase_orders.po_records
                {where_clause}
                ORDER BY operation_time DESC
                LIMIT %s
            """
            params.append(limit)
            
            cursor.execute(query, params)
            records = cursor.fetchall()
            
            # 获取列名
            colnames = [desc[0] for desc in cursor.description]
            
            # 转换为字典列表
            result = []
            for record in records:
                row_dict = {}
                for i, colname in enumerate(colnames):
                    row_dict[colname] = record[i]
                result.append(row_dict)
            
            cursor.close()
            conn.close()
            
            return result
        except Exception as error:
            print(f"获取操作日志时出错: {error}")
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except:
                    pass
            return []

# 创建全局实例
operation_logger = OperationLogger()