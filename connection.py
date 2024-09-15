import pymysql

# 连接数据库
connection = pymysql.connect(
    host= '101.35.46.20',  # 服务器地址
    user= 'root',          # 数据库用户名
    password='Your0Password!',  # 数据库密码
    database = 'Software_Registration',  # 数据库名称
    port= 3306  # 默认 MySQL 端口号
)

# 创建游标对象
cursor = connection.cursor()

def update_table(table,ID, state_name):
    with connection.cursor() as cursor:
        new_state = input("State for update: ")
        # 更新命令
        sql = f"UPDATE {table} SET {state_name} = {new_state} WHERE RegistrationID = {ID}"
        cursor.execute(sql, (new_state, ID))
        # 提交更改
    connection.commit()
    
def delete(ID):
    with connection.cursor() as cursor:
        # 删除记录
        sql = f"DELETE FROM Registration WHERE `UserID` = {ID}"
        cursor.execute(sql, (ID,))
        # 提交更改
    connection.commit()

print("1 = select all content in a table, 2 = Customized query search command, 3 = update table, 4 = delete a user from the databse, exit = Close Connection")
i = input("input the function you want: ")

while i != 'exit':
    if i == '1':
        Table_Name = input("input the table name: ")
        # 执行SQL完整表查询
        query = f"SELECT * FROM {Table_Name}" 
        cursor.execute(query)

    if i == "2":
        # 执行SQL查询
        query = input("Please input MySQL command for query: ")
        cursor.execute(query)
    
    if i == "3":
        # 执行表更新
        table = input("Which table you want to update: ")
        ID = input("Enter the RegistrationID: ")
        state_name = input("Which state you want to update: ")
        update_table(table,ID, state_name)
    
    if i == "4":
        # 执行删除用户
        ID = input("Enter the RegistrationID that want to delete: ")
        delete(ID,table)
    
    # 获取查询结果
    result = cursor.fetchall()

    # 打印结果
    for row in result:
        print(row)

    print("\n\n")
    print("1 = select all content in a table, 2 = Customized query search command, 3 = Ppdate table, 4 = Delete a user from the databse, exit = Close Connection")
    i = input("input the function you want: ")
    
# 关闭游标和连接
cursor.close()
connection.close()
print("Connection Close")