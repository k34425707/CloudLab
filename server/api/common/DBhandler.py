from logging import error
import logging
from pymysql import MySQLError
import pymysql.cursors

class DBhandler():
    #預設mysql帳號密碼
    def __init__(self,host='localhost', user='root',password='',db='remote_lab'):
        self.host=host
        self.user=user
        self.password=password
        self.db=db
        #connection是pivate
        self.__connection=None
        try:
            self.__connection=pymysql.connect(host=host,user=user,password=password,db=db,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        except MySQLError:
        
            print("My sql connection error")   
    
    def __del__(self):
        self.__connection.close()
        print('Destructor called, DBhandler deleted.')
        
    def query(self,sql,selected):
        try:
            #從數據庫鏈接中得到cursor的數據結構
            with self.__connection.cursor() as cursor:
                cursor.execute(sql)
                #執行到這一行指令時才是真正改變了數據庫，之前只是緩存在內存中
                if selected==True:
                    return cursor.fetchall()
                else:
                    self.__connection.commit()
                    pass
        except:
            logging.error("SQL execute failure with sql instruction {}".format(sql))

    def create_new_course_table(self,name):
        with self.__connection.cursor() as cursor:
            cursor.execute(
            "CREATE TABLE IF NOT EXISTS "+name+"( \
                userID varchar(50) NOT NULL, \
                userName varchar(3) NOT NULL, \
                total_score  int NOT NULL, \
                PRIMARY KEY (userID),\
                FOREIGN KEY (userID) REFERENCES user(userID)\
            );")
            self.__connection.commit()

            cursor.execute(
            "CREATE TABLE IF NOT EXISTS "+name+"_HW( \
                homeworkInfo text NOT NULL, \
                homeworkName varchar(20) NOT NULL, \
                txtName  varchar(64) , \
                txtName2  varchar(64) , \
                txtName3  varchar(64) , \
                PRIMARY KEY(homeworkName)\
            );")
            self.__connection.commit()