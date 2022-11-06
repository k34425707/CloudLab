from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
from common.JWT_handler import JWT_handler
from flask_jwt_extended import jwt_required

class homework(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db=DBhandler()
        self.jwt=JWT_handler()


    @jwt_required()
    def get(self):
        user=self.jwt.readToken()
        userID=user['userID']
        parser = reqparse.RequestParser()
        parser.add_argument('courseName')
        parser.add_argument('homeworkName')
        arg=parser.parse_args()
        print("arg['homeworkName']=="+arg["homeworkName"])
        if(arg["homeworkName"]==""):
            return {
                "message":"名稱不能為空白"
            }
        self.sql="SELECT course FROM user where `userID` = \""+userID+"\"" 
        result=self.db.query(self.sql,True)
        result=result.split("/")
        if(arg["courseName"] in result):
            self.sql="SELECT homeworkInfo FROM "+arg["courseName"]+"_HW where homeworkName="+arg["homeworkName"] 
            info=self.db.query(self.sql,True)
            self.sql="SELECT "+arg["homeworkName+"]+" FROM "+arg["courseName"]
            score=self.db.query(self.sql,True)
            return{
                "info":info[0]["homeworkInfo"],
                "score":score[0][arg["homeworkName"]]
            }
        else:
            return{
                "message":"you dont have authorization"
            }

    @jwt_required()
    def post(self):
        user=self.jwt.readToken()
        parser = reqparse.RequestParser()
        parser.add_argument('homeworkInfo')
        parser.add_argument('homeworkName')
        parser.add_argument("courseName")
        arg=parser.parse_args()
        if(arg["homeworkName"]==""):
            return {
                "message":"名稱不能為空白"
            }
        self.sql="SELECT authorization,course FROM user where `userID` = \""+user['userID']+"\""
        user=self.db.query(self.sql,True)
        course_result=user[0]["course"].split("/")
        if user[0]["authorization"]=="1" and len(course_result)!=0 and (arg["courseName"] in user[0]["course"].split("/")):
            sql="SELECT * FROM "+arg["courseName"]+"_HW where `homeworkName` = \""+arg['homeworkName']+"\""
            HW_result=self.db.query(sql,True)
            if(len(HW_result)==1):
                return {
                    "success":"f",
                    "message":"name has been used"
                }
            sql="INSERT INTO "+arg["courseName"]+"_HW (`homeworkInfo`,`homeworkName`) VALUES (\"{}\",\"{}\")".format(arg['homeworkInfo'],arg['homeworkName'])
            self.db.query(sql,False)
            sql="ALTER TABLE `"+arg["courseName"]+"` ADD `"+arg["homeworkName"]+"` JSON;"
            print(sql)
            self.db.query(sql,False)
            return {
                "success":"t"
            }
        else:
            return {
                "success":"f",
                "message":"you can't do this"
            }


    @jwt_required()
    def put(self):
        user=self.jwt.readToken()
        parser = reqparse.RequestParser()
        parser.add_argument('homeworkName')
        parser.add_argument('oldhomeworkName')
        parser.add_argument("courseName")
        parser.add_argument("homeworkInfo")
        parser.add_argument("score1")
        parser.add_argument("score2")
        parser.add_argument("score3")
        arg=parser.parse_args()
        self.sql="SELECT authorization,course FROM user where `userID` = \""+user['userID']+"\""
        user=self.db.query(self.sql,True)
        course_result=user[0]["course"].split("/")
        if user[0]["authorization"]=="1" and len(course_result)!=0 and (arg["courseName"] in user[0]["course"].split("/")):
            print(arg["homeworkName"])
            print(arg["oldhomeworkName"])
            print(arg["courseName"])
            print(arg["homeworkInfo"])
            print(arg["score1"])
            print(arg["score2"])
            print(arg["score3"])
            sql="UPDATE "+arg["courseName"]+"_HW SET homeworkInfo=\""+arg["homeworkInfo"]+"\", homeworkName=\""+arg["homeworkName"]+"\", score="+arg["score1"]+",score2="+arg["score2"]+", score3="+arg["score3"]+" WHERE homeworkName=\""+arg["oldhomeworkName"]+"\""
            print(sql)
            self.db.query(sql,False)
            sql="ALTER TABLE "+arg["courseName"]+" CHANGE `"+arg["oldhomeworkName"]+"` `"+arg["homeworkName"]+"` JSON"
            self.db.query(sql,False) 
            return {
                "message":"更新成功"
            }


    
    @jwt_required()
    def delete(self):
        user=self.jwt.readToken()
        parser = reqparse.RequestParser()
        parser.add_argument("courseName")
        parser.add_argument("homeworkName")
        arg=parser.parse_args()
        self.sql="SELECT authorization,course FROM user where userID = \""+user['userID']+"\""
        user=self.db.query(self.sql,True)
        if user[0]["authorization"]=="1"  and (arg["courseName"] in user[0]["course"].split("/")):
            sql="DELETE FROM "+arg["courseName"]+"_HW WHERE `homeworkName` =\""+arg["homeworkName"]+"\""
            self.db.query(sql,False)
            return {
                "success":"t",
                "message":"刪除成功"
            }