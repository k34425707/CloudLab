from enum import unique
from math import fabs
from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
from common.JWT_handler import JWT_handler
from flask_jwt_extended import jwt_required

class course(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db=DBhandler()
        self.jwt=JWT_handler()
    
    @jwt_required()
    def post(self):
        user=self.jwt.readToken()
        self.sql="SELECT authorization,course,userID,userName FROM user where `userID` = \""+user['userID']+"\""
        user=self.db.query(self.sql,True)
        if user[0]["authorization"]=="1":
            parser = reqparse.RequestParser()
            parser.add_argument('courseName')
            arg=parser.parse_args()
            self.sql="SELECT * FROM courses where `courseName` = \""+arg['courseName']+"\""
            result=self.db.query(self.sql,True)
            if(len(result)==1):
                    return {
                        "success":"f",
                        "message":"the course name has been used"
                    }
            self.sql="INSERT INTO `courses`(`courseName`) VALUES (\"{}\")".format(arg['courseName'])
            self.db.query(self.sql,False)
            self.db.create_new_course_table(arg['courseName'])
            courses=user[0]["course"].split("/")
            courses.append(arg["courseName"])
            courses.remove("")
            sql="UPDATE user SET course=\""+"/".join(courses)+"\" WHERE userID=\""+user[0]["userID"]+"\""
            self.db.query(sql,False)
            self.sql="INSERT INTO "+arg['courseName']+ " (`userID`,`userName`) VALUES (\"{}\",\"{}\")".format(user[0]["userID"],user[0]["userName"])
            self.db.query(self.sql,False)
            return {
                "success":"t",
                "message":"success!"
            }
        else:
            return {
                "success":"f",
                "message":"don't hava authorization"
            }
    @jwt_required()
    def delete(self):
        user=self.jwt.readToken()
        parser = reqparse.RequestParser()
        parser.add_argument('courseName')
        arg=parser.parse_args()
        self.sql="SELECT authorization,course,userID,userName FROM user where `userID` = \""+user['userID']+"\""
        user=self.db.query(self.sql,True)
        courses=user[0]["course"].split("/")
        if user[0]["authorization"]=="1" and arg["courseName"] in courses:
            self.sql="SELECT userID FROM "+arg["courseName"]
            course_member=self.db.query(self.sql,True)
            for member in course_member:
                self.sql="SELECT course FROM user WHERE `userID` =\""+member["userID"]+"\""
                print(self.db.query(self.sql,True)[0]["course"].split("/"))
                member_courses=self.db.query(self.sql,True)[0]["course"].split("/")
                member_courses.remove(arg['courseName'])
                print(member_courses)
                self.sql="UPDATE user SET course=\""+"/".join(member_courses)+"\" WHERE `userID` = \""+member["userID"]+"\""
                self.db.query(self.sql,False)
            self.sql="DROP TABLE `"+arg["courseName"]+"`"
            self.db.query(self.sql,False)
            self.sql="DROP TABLE `"+arg["courseName"]+"_HW`"
            self.db.query(self.sql,False)
            self.sql="DELETE FROM courses WHERE `courseName` = \""+arg["courseName"]+"\""
            self.db.query(self.sql,False)
            return {
                "success":"t",
                "message":"刪除成功"
            }

'''
刪除課程{
    type:"delete",
    url:"api/course",
    data (JSON.sringify) : {
        courseName
    }
}
'''