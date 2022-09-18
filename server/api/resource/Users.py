'''
更改全部User的resource
及提供的function
我假設他匯入學號檔案csv寫在這
'''
import csv

from flask import jsonify
from flask_restful import Resource,request
from common.DBhandler import DBhandler
from flask_jwt_extended import  jwt_required
from common.JWT_handler import JWT_handler
'''
我參考的命名規則
==========  =====================  ==================================
HTTP 方法   行为                   示例
==========  =====================  ==================================
GET         获取资源的信息         http://example.com/api/orders
GET         获取某个特定资源的信息 http://example.com/api/orders/123
POST        创建新资源             http://example.com/api/orders
PUT         更新资源               http://example.com/api/orders/123
DELETE      删除资源               http://example.com/api/orders/123
==========  ====================== ==================================
'''
class Users(Resource):
    
    
    '''
    把所有資料庫的user讀出出來
    '''
    def __init__(self) -> None:
        #繼承上層Resource的init
        super().__init__()  
        self.db_handler=DBhandler()
        self.jwt_handler=JWT_handler()
    
           
 
    

    @jwt_required()
    def post(self):
        path="../file/user.csv"
        userID=self.jwt_handler.readToken()["userID"]
        sql="SELECT authorization FROM `user` WHERE `userID`={}".format(userID)
        result=self.db_handler(sql,True)
        if( len(result)==0 or result[0]["authorization"]!="1" ):
            return {
                "message":"you can't do this"
            }
        courseName=request.form.get("courseName")
        file=request.files["file"]
        file.save("../file/user.csv")
        with open(path, mode='r',newline='',encoding='utf-8') as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.DictReader(csvfile)
            # 以迴圈輸出每一列
            for row in rows:
                sql="SELECT * FROM `user` WHERE `userID`={}".format(row["userID"])
                if(len(self.db_handler.query(sql,True))==0):
                    sql="INSERT INTO `user`(`userID`,`password`,`userName`,`course`,`authorization`) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\'{}\')".format(row['userID'],"a"+row['userID'],row['userName'],courseName,"0")
                    self.db_handler.query(sql,False)
                else:
                    sql="SELECT course FROM `user` WHERE `userID`={}".format(row["userID"])
                    result=self.db_handler.query(sql,True)
                    courses=result[0]["course"].split('/')
                    if(courseName not in courses):
                        courses.append(courseName)
                        courses="/".join(courses)
                        sql="UPDATE user SET course=\""+courses+"\" WHERE userID=\""+row["userID"]+"\""
                        self.db_handler.query(sql,False)
                sql="INSERT INTO`"+ courseName+"`(`userID`,`userName`) VALUES (\"{}\",\"{}\")".format(row['userID'],row['userName'])
                self.db_handler.query(sql,False)
