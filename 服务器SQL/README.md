# Flask 版本NCS markdown文档

## 项目概述
本项目基于 pymysql 和 Flask 框架开发，用于与 MySQL 数据库交互，支持用户数据的增删改查操作。

## 项目结构
SQL控制代码 + Flask 框架对于User table 的增删改查

## 数据相关
host='101.35.46.20'
user='root'
password='Your0Password!'
database='Software_Registration'

## API 使用详情
获取数据库中的所有表：http://127.0.0.1:5000/ method: GET
获取User table中的数据：http://127.0.0.1:5000/data/User/ method: GET
插入new row到User table：http://127.0.0.1:5000/data/User/ method: POST
{
    "RegistrationID": 1,
    "Username": "test_user",
    "Image": "/path/to/image",
    "Introduction": "This is a test",
    "Login_Time": "2024-12-30 10:00:00",
    "Special_Status": "VIP",
    "State": "在线"
}

更新User table中userID为1的login time：http://127.0.0.1:5000/data/User/ method: PUT
{
    "Login_Time": "2024-12-31 12:00:00"
}


删除User table中最后的记录：http://127.0.0.1:5000/data/User/ method: DELETE