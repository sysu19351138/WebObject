import mysql_sql
import server_api
import sql_models

if __name__ == '__main__':

    sql_models.db.drop_all()
    sql_models.db.create_all()

    mysql_sql.USER_INFO_insert("18811891816", "18811891816")
    # SERVICE_INFO测试表
    mysql_sql.SERVICE_INFO_insert("service1", "a", "b" , True , False , "43fsa")
    # GLOBAL_MODEL_INFO测试表
    mysql_sql.GLOBAL_MODEL_INFO_insert("server1", "v1", "aaa", "2022-02-18 00:00:00", 1, "2022-02-19 00:00:00", "model_path")

    server_api.app.run()
