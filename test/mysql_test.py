#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("192.168.1.101", "root", "123456", "paper")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询

sql = "INSERT IGNORE INTO `paper_info`(`doi`) VALUES(%s)"
val = ['d', 'v']


# 使用 fetchone() 方法获取单条数据.

    # 执行sql语句
cursor.executemany(sql, val)
    # 提交到数据库执行
db.commit()


# 关闭数据库连接
db.close()