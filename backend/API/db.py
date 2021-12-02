import mysql.connector as database

connection = database.connect(
    user="root",
    password="admin",
    host='127.0.0.1',
    database="innovatieplatform")
cur = connection.cursor()
