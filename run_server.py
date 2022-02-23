import mysql_sql
import server_api
import sql_models

if __name__ == '__main__':

    sql_models.db.drop_all()
    sql_models.db.create_all()

    mysql_sql.USER_INFO_insert("18811891816", "18811891816")

    # SERVICE_INFO测试表
    mysql_sql.SERVICE_INFO_insert("Service2", "trainable", "Service2 able to be trained", False, True, "XXX", "XXX")
    mysql_sql.SERVICE_INFO_insert("Service4", "trainable", "Service3 with trained model", False, True, "XXX", "XXX")

    # GLOBAL_MODEL_INFO测试表
    mysql_sql.GLOBAL_MODEL_INFO_insert("Service2", "0.0", 50, "asynchronous", "0.001", 50, 0.001)
    mysql_sql.GLOBAL_MODEL_INFO_insert("Service4", "0.0", 50, "asynchronous", "0.001", 50, 0.001)

    server_api.app.run()
