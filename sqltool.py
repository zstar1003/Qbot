import pymysql

# 数据库用户名和密码
user = "root"
password = "自己的密码"

# 初始化：每个用户给予三次文字机会
def init_user():
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    sql_order = 'UPDATE `group` SET TextChance = 3'
    cur.execute(sql_order)
    conn.commit()
    cur.close()
    conn.close()


# 插入新用户
def insert_user(qq_no, message):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    sql_order = 'INSERT INTO `group` (qq_no, TextChance, PicChance, Message) VALUES ("%s", 3, 3, "%s")' % (qq_no, message)
    cur.execute(sql_order)
    conn.commit()
    cur.close()
    conn.close()


# 用户信息更新
def update_user(qq_no, message):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    # 文字次数减1
    sql_order = 'UPDATE `group` SET TextChance = TextChance - 1 WHERE qq_no = %s' % qq_no
    cur.execute(sql_order)
    conn.commit()
    # 信息内容拼接
    sql_order = 'UPDATE `group` SET Message = CONCAT(Message,";%s") WHERE qq_no = %s' % (message, qq_no)
    cur.execute(sql_order)
    conn.commit()
    cur.close()
    conn.close()


# 用户信息更新(图片信息)
def update_user_pic(qq_no):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    # 图片次数减1
    sql_order = 'UPDATE `group` SET PicChance = PicChance - 1 WHERE qq_no = %s' % qq_no
    cur.execute(sql_order)
    conn.commit()
    cur.close()
    conn.close()


# 用户文字次数查询
def select_TextChance(qq_no):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    sql_order = 'select TextChance from `group` WHERE qq_no = %s' % qq_no
    cur.execute(sql_order)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]

# 用户图片次数查询
def select_PicChance(qq_no):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    sql_order = 'select PicChance from `group` WHERE qq_no = %s' % qq_no
    cur.execute(sql_order)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]


# 清空用户的次数
def clear_user(qq_no):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    sql_order = 'UPDATE `group` SET TextChance = 0 WHERE qq_no = %s' % qq_no
    cur.execute(sql_order)
    conn.commit()
    sql_order = 'UPDATE `group` SET PicChance = 0 WHERE qq_no = %s' % qq_no
    cur.execute(sql_order)
    conn.commit()
    cur.close()
    conn.close()


# 查询当前用户是否已经存在
def user_isexist(qq_no):
    conn = pymysql.connect(host="localhost", port=3306, user=user, password=password, database="qbot")
    cur = conn.cursor()
    sql_order = 'select * from `group` where qq_no = "%s"' % qq_no
    result = cur.execute(sql_order)
    conn.commit()
    cur.close()
    conn.close()
    if result == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    insert_user('123456', '测试一下')
    num_TextChance = select_TextChance('123456')
    print(num_TextChance)