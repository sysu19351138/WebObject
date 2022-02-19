import mysql_sql
import server_api
import sql_models

if __name__ == '__main__':

    sql_models.db.drop_all()
    sql_models.db.create_all()

    mysql_sql.USER_INFO_insert("18811891816", "18811891816")
    # SERVICE_INFO测试表
    mysql_sql.SERVICE_INFO_insert("sad", "a", "b",True,False, "43fsa")

    server_api.app.run()