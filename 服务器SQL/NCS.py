import pymysql
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import random


app = Flask(__name__)

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
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
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
                
                # 打印结果以检查格式
                print("Tables result:", result)
                
                # 提取表名
                table_names = [list(row.values())[0] for row in result]  # 适配字典格式
                return table_names
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



db = SQL_Control()



@app.route('/', methods=['GET'])
def get_tables():
    tables = db.show_tables()
    if tables:
        return jsonify({"tables": tables})
    return jsonify({"error": "Failed to fetch tables"}), 500


@app.route('/data/<table_name>/', methods=['GET'])
def get_table_data(table_name):
    results = db.execute_query(f"SELECT * FROM {table_name}")
    if results:
        return jsonify({"data": results})
    return jsonify({"error": "Failed to fetch data"}), 500


@app.route('/data/User/', methods=['POST'])
def insert_data():
    # 验证 Content-Type
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Must be application/json"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is empty or invalid JSON"}), 400

    columns = ["RegistrationID", "Username", "Image", "Introduction", "Login_Time", "Special_Status", "State"]
    default_data = {
        "RegistrationID": random.randint(0, 5),
        "Username": "test_user",
        "Image": "/path/to/image",
        "Introduction": "Default Introduction",
        "Login_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Special_Status": "null", 
        "State": "在线"
    }
    values = [data.get(col, default_data[col]) for col in columns]
    column_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO `User` ({column_str}) VALUES ({placeholders})"
    
    result = db.execute_non_query(query, values)
    if "操作失败" in result:
        return jsonify({"error": result}), 500
    return jsonify({"message": "Record inserted successfully!"})



@app.route('/data/User/', methods=['PUT'])
def update_data():
    # 验证 Content-Type
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Must be application/json"}), 415

    # 获取请求数据
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is empty or invalid JSON"}), 400

    updates = []
    values = []

    # 固定 Login_Time 为当前时间
    updates.append("`Login_Time` = %s")
    values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 遍历请求数据构建其他更新字段
    for key, value in data.items():
        if key != "Login_Time":  # 避免重复处理 Login_Time
            updates.append(f"`{key}` = %s")
            values.append(value)

    if not updates:
        return jsonify({"error": "No fields to update"}), 400

    # 拼接 SQL 更新语句
    update_clause = ", ".join(updates)
    query = f"UPDATE `User` SET {update_clause} WHERE `Userid` = %s"

    # 将主键值固定为 1
    values.append(1)

    # 执行 SQL 语句
    try:
        print("执行的 SQL:", query)
        print("参数:", values)
        result = db.execute_non_query(query, values)

        if result != "操作成功":
            return jsonify({"error": result}), 500

        return jsonify({"message": "Record updated successfully!"})
    except Exception as e:
        print(f"SQL 执行失败: {str(e)}")
        return jsonify({"error": f"操作失败: {str(e)}"}), 500





@app.route('/data/User/', methods=['DELETE'])
def delete():
    # 查询表中最后一行的主键值
    query_select = "SELECT `UserID` FROM `User` ORDER BY `UserID` DESC LIMIT 1"
    result = db.execute_query(query_select)

    if not result:
        return jsonify({"error": "No rows found in the table"}), 404

    # 获取最后一行的主键值
    last_row_id = result[0]["UserID"]

    # 删除最后一行
    query_delete = "DELETE FROM `User` WHERE `UserID` = %s"
    try:
        db.execute_non_query(query_delete, (last_row_id,))
        return jsonify({"message": f"Record with UserID = {last_row_id} deleted successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to delete record: {str(e)}"}), 500



# 示例
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True, threaded = True)
    CORS(app)
