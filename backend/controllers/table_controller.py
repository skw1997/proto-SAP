from backend.models.database import DatabaseManager

class TableController:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_table_data(self, table_name):
        """获取表数据"""
        try:
            # query_table 返回的是记录列表，而不是 (colnames, records) 元组
            records = self.db_manager.query_table(table_name)
            if records is not None:
                # 如果 records 不是空列表，说明查询成功
                return {
                    'success': True,
                    'data': records
                }
            else:
                # 检查是否是连接问题
                conn = self.db_manager.get_connection()
                if not conn:
                    return {
                        'success': False,
                        'error': '数据库连接失败，请检查数据库配置和PostgreSQL服务状态'
                    }
                else:
                    if conn:
                        conn.close()
                    return {
                        'success': False,
                        'error': '无法加载表数据，请检查表是否存在'
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_duplicates(self, table_name, data_list):
        """检查数据列表中是否存在主键冲突"""
        try:
            duplicates = self.db_manager.check_duplicates(table_name, data_list)
            return {
                'success': True,
                'duplicates': duplicates
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_row(self, table_name, pn, updates, user_email=None):
        """更新行数据"""
        try:
            # 检查是否有更新数据
            if not updates or not isinstance(updates, dict):
                return {
                    'success': False,
                    'message': '没有提供更新数据'
                }
            
            # 检查更新数据是否为空
            if len(updates) == 0:
                return {
                    'success': True,
                    'message': '没有更改需要保存'
                }
            
            success, message = self.db_manager.update_row(table_name, pn, updates, user_email)
            return {
                'success': success,
                'message': message
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_row(self, table_name, key, user_email=None, key_field='pn'):
        """删除行数据"""
        try:
            success, message = self.db_manager.delete_row(table_name, key, user_email, key_field)
            return {
                'success': success,
                'message': message
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def insert_row(self, table_name, data, user_email=None):
        """插入新行"""
        try:
            success, message = self.db_manager.insert_row(table_name, data, user_email)
            return {
                'success': success,
                'message': message
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }