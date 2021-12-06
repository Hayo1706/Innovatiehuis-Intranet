import mysql.connector as database
from mysql.connector import pooling
from mysql.connector import Error

try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="innovatiepool",
        pool_size=5,
        pool_reset_session=True,
        host='127.0.0.1',
        database='innovatieplatform',
        user='root',
        password='admin')

except Error as e:
    print("Error while connecting to MySQL using Connection pool ", e)