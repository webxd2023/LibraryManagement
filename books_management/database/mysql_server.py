import pymysql
from books_management.config import database_config

def return_coon():
    conn = pymysql.Connect(host=database_config.HOST, port=database_config.PORT, user=database_config.USER, passwd=database_config.PASSWORD, db=database_config.DB, charset='utf8')
    return conn


def get_user_info_list(sql):
    conn=return_coon()
    cur = conn.cursor()
    cur.execute(sql)
    biuids = cur.fetchall()
    # print(biuids)
    cur.close()
    conn.close()
    return biuids
def column_name(table_name):
    conn = return_coon()
    cur = conn.cursor()
    sql = f"select COLUMN_NAME from information_schema.COLUMNS where table_name = '{table_name}' order by ordinal_position asc"
    cur.execute(sql)
    data = []
    for field in cur.fetchall():
        data.append(field[0])
    cur.close()
    conn.close()
    return data
def add_user_info(sql):
    conn = return_coon()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    author_id = cur.lastrowid
    cur.close()
    conn.close()
    return author_id
def delsql(sql):
    try:
        conn=return_coon()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        num = cur.rowcount
        cur.close()
        conn.close()
        if num>0:
            return {"code":200,"msg":"删除成功"}
        else:
            return {"code": 402, "msg": "未找到数据或已经被删除"}
    except Exception as e:
        return {"code":401,"msg":f"删除失败:{e}"}

def com_up(sql):
    try:
        conn = return_coon()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        num = cur.rowcount
        if num == 0:
            return {'code': 200, 'msg': '数据未改变'}
        else:
            return {'code': 200, 'msg': '编辑成功！'}
    except Exception as e:
        return {'code': 200, 'msg': '编辑出错！%s'%e}
# get_user_info_list()
# print(column_name())