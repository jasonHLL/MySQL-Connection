import pymysql

class SQL_Control:
    def __init__(self):
        # 初始化连接
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='101.35.46.20',  # 服务器地址
                user='root',          # 数据库用户名
                password='Your0Password!',  # 数据库密码
                database='Software_Registration',  # 数据库名称
                port=3306,  # 默认 MySQL 端口号
                charset='utf8mb4'
            )
            print("数据库连接成功！")
        except Exception as e:
            print(f"数据库连接失败: {e}")
    
    def close(self):
        # 关闭数据库连接
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """
        执行查询语句（SELECT），返回结果
        :param query: SQL 查询语句
        :param params: 可选参数，用于防止 SQL 注入
        :return: 查询结果
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()  # 获取查询结果
                return result
        except Exception as e:
            print(f"查询失败: {e}")
            return None

    def execute_non_query(self, query, params=None):
        """
        执行非查询语句（INSERT、UPDATE、DELETE）
        :param query: SQL 语句
        :param params: 可选参数，用于防止 SQL 注入
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()  # 提交更改
                return "操作成功"
        except Exception as e:
            self.connection.rollback()  # 回滚更改
            return f"操作失败: {e}"

    def show_tables(self):
        """
        显示数据库中的所有表
        :return: 表名列表或 None（查询失败）
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")  # 固定的 SQL 查询语句
                result = cursor.fetchall()  # 获取查询结果
                return [row[0] for row in result]  # 提取表名，返回为列表
        except Exception as e:
            print(f"查询失败: {e}")
            return None

    def show_column(self, table_name):
        """
        获取表的列名列表（排除 auto_increment 类型的列）
        """
        try:
            with self.connection.cursor() as cursor:
                query = f"DESCRIBE `{table_name}`"  # 确保表名使用反引号包裹
                cursor.execute(query)
                result = cursor.fetchall()  # 获取查询结果

                # 提取列名，排除 auto_increment 列
                column_names = [row[0] for row in result if row[5] != 'auto_increment']
                
                print(f"Columns in {table_name}: {column_names}")
                return column_names
        except Exception as e:
            print(f"查询失败: {e}")
            return None    

    def get_primary_key(self, table_name):
        """
        获取表的主键列名
        :param table_name: 表名
        :return: 主键列名（字符串）或 None
        """
        try:
            with self.connection.cursor() as cursor:
                query = f"SHOW KEYS FROM `{table_name}` WHERE Key_name = 'PRIMARY'"
                cursor.execute(query)
                result = cursor.fetchone()  # 获取主键列信息
                if result:
                    return result[4]  # Column_name 在第5列
                return None
        except Exception as e:
            print(f"查询主键失败: {e}")
            return None

    def update_record(self, table_name, primary_key, primary_key_value, updates):
        """
        根据主键更新记录
        :param table_name: 表名
        :param primary_key: 主键列名
        :param primary_key_value: 主键值
        :param updates: 更新数据的字典 {column_name: new_value}
        """
        try:
            set_clause = ", ".join([f"`{col}` = %s" for col in updates.keys()])
            query = f"UPDATE `{table_name}` SET {set_clause} WHERE `{primary_key}` = %s"
            params = list(updates.values()) + [primary_key_value]

            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                print("Record updated successfully!")
        except Exception as e:
            print(f"更新记录失败: {e}")
            self.connection.rollback()

    def check_pk_exists(self, table_name, primary_key, primary_key_value):
        """
        检查主键值是否存在于指定表中
        :param table_name: 表名
        :param primary_key: 主键列名
        :param primary_key_value: 主键值
        :return: True 如果主键值存在，否则 False
        """
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT COUNT(*) FROM `{table_name}` WHERE `{primary_key}` = %s"
                cursor.execute(query, (primary_key_value,))
                result = cursor.fetchone()
                return result[0] > 0  # 如果 COUNT(*) > 0，返回 True
        except Exception as e:
            print(f"查询失败: {e}")
            return False

# 示例
if __name__ == "__main__":
    db = SQL_Control()
    tables = db.show_tables()
    print(f"Tables in the database: {tables}")
    
    print("1 = select all content in a table, 2 = insert a new record, 3 = update data, 4 = delete data from the table, exit = Close Connection")
    i = input("input the function you want: ")
    allow_function = ['1','2','3','4','exit']
    allow_tables = tables
    
    while i != 'exit': 
        if i == '1':
            table_name = input("input the table you select query for: ")
            if table_name in allow_tables:
                # READ 示例：查询数据
                select_query = f"SELECT * FROM {table_name}"
                results = db.execute_query(select_query)
                print("查询结果:", results)
            else:
                print("Illegal table name")


        if i == '2':
            table_name = input("Input the table you want to insert data: ")
            if table_name in allow_tables:
                # 获取列名
                columns = db.show_column(table_name)
                if columns:

                    # 动态生成插入语句
                    column_str = ", ".join(columns)
                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = f"INSERT INTO `{table_name}` ({column_str}) VALUES ({placeholders})"

                    # 动态输入数据
                    values = [input(f"Enter value for {col}: ") for col in columns]

                    # 执行插入
                    result = db.execute_non_query(insert_query, values)
                    if '操作失败' in result:
                        print(result)
                    else:
                        print("Record inserted successfully!")
                else:
                    print("No valid columns found.")
            else:
                print("Illegal table name.")



        if i == '3':
            # UPDATE 示例：更新数据
            table_name = input("Input the table you want to insert data: ")
            if table_name in allow_tables:
                # 获取列名
                columns = db.show_column(table_name)
                if columns:
                    # 获取primary key
                    primary_key = db.get_primary_key(table_name)
                    if primary_key:
                        print(f"The primary key for {table_name} is {primary_key}")
                        primary_key_value = input(f"Enter the value for {primary_key}: ")
                        if db.check_pk_exists(table_name, primary_key, primary_key_value):
                            updates = {}
                            num_updates = int(input("Enter the number of columns to update: "))
                            for _ in range(num_updates):
                                column = input("Enter column name to update: ")
                                value = input(f"Enter new value for {column}: ")
                                updates[column] = value
                            db.update_record(table_name, primary_key, primary_key_value, updates)
                        else:
                            print(f"The primary key value {primary_key_value} does not exist in {table_name}.")
                    else:
                        print(f"No primary key found for {table_name}")
                else:
                    print("No valid columns found.")
            else:
                print("Illegal table name.")


        if i == '4':
            # DELETE 示例：删除数据
            table_name = input("Input the table you want to delete data from: ")
            if table_name in allow_tables:
                primary_key = db.get_primary_key(table_name)
                PK = input("Input the primary key you want to delete: ")
                # 检查主键值是否存在
                if db.check_pk_exists(table_name, primary_key, PK):
                    delete_query = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
                    result = db.execute_non_query(delete_query, (PK,))
                    if '操作失败' in result:
                        print(result)
                    else:
                        print(f"Successfully deleted record with {primary_key} = {PK}.")
                else:
                    print(f"The primary key value {PK} does not exist in {table_name}.")
            else:
                print("Illegal table name.")


        if i == 'exit':
            # 关闭连接
            print("数据库连接已断开。") # 打印不出来
            db.close()
        
        if i not in allow_function:
            print("Illegal function selection")
        i = input("input the function you want: ")