import pymysql

connection = pymysql.connect(host='localhost',user='root',password='',charset='utf8mb4')

try:
    cursor = connection.cursor()

    cursor.execute("DROP DATABASE IF EXISTS remote_lab;")

    cursor.execute("CREATE DATABASE IF NOT EXISTS remote_lab;")

    connection.select_db("remote_lab")

    cursor.execute("DROP TABLE IF EXISTS courses;")
    connection.commit()

    cursor.execute("DROP TABLE IF EXISTS orderQueue;")
    connection.commit()

    cursor.execute("DROP TABLE IF EXISTS user;")
    connection.commit()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user( \
            userID varchar(50) NOT NULL, \
            userName  varchar(30) NOT NULL, \
            password varchar(70) NOT NULL, \
            email varchar(50) NOT NULL, \
            PRIMARY KEY (userID) \
        );")
    connection.commit()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS orderQueue( \
            workOrder int(10) NOT NULL AUTO_INCREMENT, \
            workType varchar(3) NOT NULL, \
            workText  varchar(25) NOT NULL, \
            PRIMARY KEY (workOrder) \
        );")
    connection.commit()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS courses( \
            courseID int(10) NOT NULL, \
            courseName varchar(300), \
            PRIMARY KEY (courseID) \
        );")
    connection.commit()

    print("Create the database!")
except Exception as err:
    print("Error: " + err)
finally:
    cursor.close()
    connection.close()
    print("Close the connection!")