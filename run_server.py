import mysql_sql
import server_api
import sql_models

if __name__ == '__main__':

    sql_models.db.drop_all()
    sql_models.db.create_all()

    mysql_sql.USER_INFO_insert("18811891816", "18811891816")
    # SERVICE_INFO测试表
    mysql_sql.SERVICE_INFO_insert("Service1", "trainable model ", "Service1 with trained model", True, False , "wuchh25")
    mysql_sql.SERVICE_INFO_insert("Service2", "trainable model ", "Service2 with trained model", False, True, "XXXXX")
    mysql_sql.SERVICE_INFO_insert("Service3", "trainable model ", "Service3 with trained model", False, False, "wuchh")
    # GLOBAL_MODEL_INFO测试表
    mysql_sql.GLOBAL_MODEL_INFO_insert("Service1", "v1", "aaa", "2022-02-18 00:00:00", 1, "2022-02-19 00:00:00",
                                       "model_path")
    mysql_sql.GLOBAL_MODEL_INFO_insert("Service2", "v2", "aaa", "2022-02-18 00:00:00", 1, "2022-02-19 00:00:00",
                                       "model_path")
    mysql_sql.GLOBAL_MODEL_INFO_insert("Service3", "v3", "aaa", "2022-02-18 00:00:00", 1, "2022-02-19 00:00:00",
                                       "model_path")

    server_api.app.run()
