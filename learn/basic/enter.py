class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.connection = connect_to_database(self.db_name)  # 模拟连接
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()  # 确保连接关闭
        if exc_type is not None:
            print(f"发生异常：{exc_value}")  # 可在此处理异常

# 使用示例
with DatabaseConnection("my_db") as conn:
    conn.query("SELECT * FROM users")  # 自动管理连接的打开和关闭
