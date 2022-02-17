import pymysql
# 数据库配置在此修改
Password = "wch011005"
Database = "USER_INFO"

def match(username: str, password: str):
    # 打开数据库连接
    # 这里运行的话需要改 密码 与 数据库 名
    flag = False
    db = pymysql.connect(host="localhost", user="root", password=Password, database=Database)
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    select_sql = "select * from USER_INFO where username=%s" % (username)

    try:
        cursor.execute(select_sql)
        data = cursor.fetchall()
        # 可以有长度判断

        output = data[0][1]
        if (output == password):
            flag = True
        else:
            flag = False

    except:
        print("查询出错")
        flag = False

    db.close()
    return str(flag)

def find(username: str):
    # 打开数据库连接
    flag = False
    db = pymysql.connect(host="localhost", user="root", password=Password, database=Database)
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    select_sql = "select * from USER_INFO where name=%s" % (username)

    try:
        cursor.execute(select_sql)
        data = cursor.fetchall()
        flag = True
    except:
        print("查询出错")
        flag = False

    db.close()
    return str(flag)


def insert(phone: str, password: str):
    # 打开数据库连接
    flag = False
    db = pymysql.connect(host="localhost", user="root", password=Password, database=Database)
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    insert_sql = "insert into USER_INFO(username, password) values(%s, %s)" % (phone, password)

    try:
        # 执行sql语句
        cursor.execute(insert_sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库连接
        flag = True

    except:
        print("数据插入失败,请查检try语句里的代码")
        # raise
        flag = False

    db.close()
    return str(flag)


def update(phone: str, password: str):
    flag = False
    db = pymysql.connect(host="localhost", user="root", password=Password, database=Database)
    cursor = db.cursor()
    updata_sql = "update USER_INFO set password=%s where name=%s" % (phone, password)

    try:
        # 执行sql语句
        cursor.execute(updata_sql)
        # 提交到数据库执行
        db.commit()
        flag = True

    except:
        # 如果发生错误则回滚
        db.rollback()
        db.close()
        flag = False

    db.close()
    return str(flag)


def delete(phone: str):
    flag = False
    db = pymysql.connect(host="localhost", user="root", password=Password, database=Database)
    cursor = db.cursor()
    del_sql = "delete from USER_INFO where name='%s'" % (phone)

    try:
        cursor.execute(del_sql)
        db.commit()
        flag = True

    except:
        # 如果发生错误则回滚
        db.rollback()
        flag = False

    db.close()
    return str(flag)


if __name__ == "__main__":
    # select("'admin'")
    insert("18811891816", "18811891816")
    # select("18811891816","18811891816")
    # delete("18811891816")