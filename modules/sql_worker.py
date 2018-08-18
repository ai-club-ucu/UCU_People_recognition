import pymysql

def creat_local_connection():
    connection = pymysql.connect(host="localhost",
                                 user="root",
                                 password="",
                                 db="dvd_collection",
                                 charset="utf8mb4",
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_table(table_name, connection):
    cursor = connection.cursor()
    sql_statement = "CREATE TABLE {}(id int, x DECIMAL(25, 10), y DECIMAL(25, 10))".format(table_name)
    cursor.execute(sql_statement)

def drop_table(table_name, connection):
    cursor = connection.cursor()
    sql_statement = "DROP TABLE IF EXISTS {}".format(table_name)
    cursor.execute(sql_statement)

