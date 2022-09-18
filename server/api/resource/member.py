
import csv

from flask import jsonify
from flask_restful import Resource,request
from common.DBhandler import DBhandler
from flask_jwt_extended import  jwt_required
from common.JWT_handler import JWT_handler
from werkzeug.security import generate_password_hash

class member(Resource):

    def __init__(self) -> None:
        super().__init__()  
        self.db_handler=DBhandler()
        self.jwt_handler=JWT_handler()

    

        
    
           
    @jwt_required()
    def post(self):
        courseName=request.form.get("courseName")
        path="../file/user.csv"
        userID=self.jwt_handler.readToken()["userID"]
        sql="SELECT authorization,course FROM `user` WHERE `userID`=\"{}\"".format(userID)
        result=self.db_handler.query(sql,True)
        print(sql)
        if( len(result)==0 or result[0]["authorization"]!="1" or (courseName not in result[0]["course"].split("/")) ):
            return {
                "message":"you can't do this"
        }
        file=request.files["file"]
        file.save("../file/user.csv")
        with open(path, mode='r',newline='',encoding='utf-8') as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.DictReader(csvfile)
            # 以迴圈輸出每一列
            for row in rows:
                sql="SELECT * FROM `user` WHERE `userID`={}".format(row["userID"])
                if(len(self.db_handler.query(sql,True))==0):
                    sql="INSERT INTO `user`(`userID`,`password`,`userName`,`course`,`authorization`) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\'{}\')".format(row['userID'],generate_password_hash(password=row["userID"]),row['userName'],courseName,"0")
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
            return {
                "success":"t",
                "message":"成功新增"
        }
    
    @jwt_required()
    def delete(self):
        accesser=self.jwt_handler.readToken()
        courseName=request.form.get("courseName")
        userID=request.form.get("userID")
        sql="SELECT authorization,course FROM `user` WHERE `userID`={}".format(accesser["userID"])
        result=self.db_handler.query(sql,True)
        if( len(result)==0 or result[0]["authorization"]!="1" or (courseName not in result[0]["course"].split("/")) ):
            return {
                "success":"f",
                "message":"you can't do this"
        }
        sql="SELECT authorization FROM `user` WHERE `userID`={}".format(userID)
        if( self.db_handler.query(sql,True)[0]["authorization"]=="1"):
            return {
                "meesage":"he or she is a administrator"
            }
        sql="DELETE FROM "+courseName+" WHERE `userID`= \""+userID+"\""
        self.db_handler.query(sql,False)
        self.sql="SELECT course FROM user WHERE `userID` =\""+userID+"\""
        print(self.sql)
        member_courses=self.db_handler.query(self.sql,True)[0]["course"].split("/")
        print(member_courses)
        member_courses.remove(courseName)
        if(len(member_courses)!=0):
            self.sql="UPDATE user SET course=\""+"/".join(member_courses)+"\" WHERE `userID` = \""+userID+"\""
        else:
            self.sql="DELETE FROM user WHERE `userID` = \""+userID+"\""
        self.db_handler.query(self.sql,False)
        return {
            "success":"t",
            "message":"成功剔除該學生"
        }


'''
刪除成員{
    type:"delete",
    url:"/api/member",
    data:{
        courseName,
        userID  (要刪除的那個)
    }
}
'''