import pymysql
import logging

# 打开数据库连接
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME

db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)


# 关闭数据库连接

# try:
#     cursor.execute(sql, (arg1, arg2))
#     connection.commit()
# except:
#     print(cursor._last_executed)
#     raise


def insert_manny(val):
    logging.info("待插入的数据")
    logging.info(val)
    sql = "INSERT IGNORE INTO `paper_info`(`doi`,`site_type`) VALUES(%s,%s)"
    cursor.executemany(sql, val)
    logging.info("正在执行的sql:\t%s" % cursor._last_executed)
    db.commit()

    return cursor.rowcount


def update_bib_one(val):
    logging.info("待更新的数据")
    logging.info(val)

    sql = "update `paper_info` set bib_flag=%s,bib_info=%s, title =%s where doi =%s"
    cursor.execute(sql, val)
    logging.info("正在执行的sql:\t%s" % cursor._last_executed)
    db.commit()

    return cursor.rowcount
def update_fail(val):
    logging.info("待更新的数据")
    logging.info(val)

    sql = "update `paper_info` set remark=%s  where doi =%s"
    cursor.execute(sql, val)
    logging.info("正在执行的sql:\t%s" % cursor._last_executed)
    db.commit()

    return cursor.rowcount


def update_pdf_one(val):
    logging.info("待更新的数据")
    logging.info(val)
    sql = "update `paper_info` set pdf_flag=%s where doi= %s"
    cursor.execute(sql, val)
    logging.info("正在执行的sql:\t%s" % cursor._last_executed)
    db.commit()

    return cursor.rowcount


def insert_manny_dict(val_dict):
    a = val_dict[0]
    cols = ", ".join('`{}`'.format(k) for k in a.keys())

    val_cols = ', '.join('%({})s'.format(k) for k in a.keys())
    sql = "REPLACE INTO `paper_info`(%s) VALUES(%s)"

    res_sql = sql % (cols, val_cols)
    cursor.executemany(res_sql, val_dict)

    db.commit()

    return cursor.rowcount


def get_all_without_bib():
    sql = "select * from paper_info where bib_flag=0"
    cursor.execute(sql)
    logging.info("正在执行的sql:\t%s" % cursor._last_executed)
    return cursor.execute(sql), cursor.fetchall()


def get_all_without_pdf():
    sql = "select * from paper_info where remark is null and pdf_flag=0 and title is not null"
    cursor.execute(sql)
    logging.info("正在执行的sql:\t%s" % cursor._last_executed)
    return cursor.execute(sql), cursor.fetchall()


def close_db():
    return db.close()


# def escape_name(s):
#     """Escape name to avoid SQL injection and keyword clashes.
#
#     Doubles embedded backticks, surrounds the whole in backticks.
#
#     Note: not security hardened, caveat emptor.
#
#     """
#     return '`{}`'.format(s.replace('`', '``'))
#
# names = list(dict_of_params)
# cols = ', '.join(map(escape_name, names))  # assumes the keys are *valid column names*.
# placeholders = ', '.join(['%({})s'.format(name) for name in names])
#
# query = 'INSERT INTO TABLENAME ({}) VALUES ({})'.format(cols, placeholders)
# cursor.execute(query, dict_of_params)

if __name__ == '__main__':
    # val =[{'doi': '10.1119/CIFEr.2012.63y27783','site_type':'IEEE'},{'doi': '10.11y9/CIFEr.2012.63y27783','site_type':'IEEE'}]
    # logging.info(insert_manny_dict(val))
    # update_bib_one((True,'1','1',"10.1109/CIFEr.2012.6327783"))
    print(get_all_without_pdf())
