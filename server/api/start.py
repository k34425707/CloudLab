#!/bin/python3
# 載入Flask套件
from distutils import extension
from fileinput import filename
from flask import Flask, render_template,make_response, send_file,request
from flask_restful import Api
from common.JWT_handler import JWT_handler
from common.DBhandler import DBhandler
from common.mailSender import mail_sender
from flask_jwt_extended import  JWTManager,jwt_required
from werkzeug.security import generate_password_hash
from datetime import datetime
import json

'''--------------------------------------
    import api所提供的resouce file
---------------------------------------'''
from resource.User import User
from resource.Users import Users
from resource.member import  member
from resource.login_handler import login_handler
from resource.ProgrammingRequest import ProgrammingRequest
from resource.course import course
from resource.homework import homework
from resource.homeworks import homeworks
from resource.ProgrammingTest_without_hardware import ProgrammingTest_without_hardware



app = Flask(__name__)
jwt=JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'test' 
app.config['JWT_TOKEN_LOCATION']=['query_string','headers','cookies']
app.config['JWT_ACCESS_COOKIE_NAME']="access_token_cookie"
app.config['JWT_ACCESS_TOKEN_EXPIRES']=3600

'''
Api要提供的resource放在resource
'''

api = Api(app)

mail=mail_sender()
def verify_user_authorization_courses(userID):
    db=DBhandler()
    sql="SELECT authorization,course FROM `user` WHERE `userID`=\""+userID+"\""
    user_result=db.query(sql,True)
    if(len(user_result)==0):
        return None,None
    courses=user_result[0]["course"].split("/")
    return user_result[0]["authorization"],courses

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("token not authorization")
    return make_response(render_template("index.html"))


@app.route("/test")
def testUP():
    return render_template("test.html",obj=[{"test":"test"}])


##登入頁面
@app.route("/")
def index():
    return render_template("index.html")

##遠端燒錄頁面
@app.route("/remote")
@jwt_required()
def remote():
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    sql="SELECT status,datetime FROM userstatus WHERE `userID`=\""+userID+"\" && workType=0"
    status=db.query(sql,True)
    upload_datetime="上傳時間 : 紀錄不存在"
    print(len(status))
    if(len(status)==1):
        upload_datetime=datetime.strftime(status[0]["datetime"], '%Y-%m-%d %H:%M:%S')
    return render_template("remote.html",status=status,time=upload_datetime)

##使用者選課程的頁面s
@app.route("/course")
@jwt_required()
def coursechoose():
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    authorization,courses=verify_user_authorization_courses(userID)
    print(authorization)
    print(courses)
    return render_template("course.html",authorzation=authorization,courses=courses)

##使用者瀏覽某堂課程內容作業的頁面
@app.route("/course/<string:courseName>")
@jwt_required()
def homeworkbrowse(courseName):
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    authorization,courses=verify_user_authorization_courses(userID)
    if(courseName in courses):
        sql="SELECT homeworkName FROM "+courseName+"_HW "
        hw_result=db.query(sql,True)
        sql="SELECT userID,userName FROM `"+courseName+"`"
        member_result=db.query(sql,True)
        print(authorization)
        print(hw_result)
        print(member_result)
        return render_template("homeworkbrowse.html",authorzation=authorization,homeworks=hw_result,members=member_result,courseName=courseName)

##使用者看某項作業的詳細內容
@app.route("/course/<string:courseName>/<string:hwName>")
@jwt_required()
def homeworkcontent(courseName,hwName):
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    authorization,courses=verify_user_authorization_courses(userID)
    if(courseName in courses):
        sql="SELECT homeworkName,homeworkInfo,txtName,txtName2,txtName3,score,score2,score3 FROM "+courseName+"_HW  WHERE homeworkName=\""+hwName+"\""
        print(sql)
        hw_result=db.query(sql,True)
        score={
            "Scores":"沒有繳交紀錄",
            "test":"沒有成績",
            "test2":"沒有成績",
            "test3":"沒有成績"
        }
        if authorization=="0":
            sql="SELECT `"+hwName+"` FROM `"+courseName+"`  WHERE `userID`=\""+userID+"\""
            result = db.query(sql,True)
            print(result)
            # print(db.query(sql,True)[0][hwName])
            if(len(result) != 0 and result[0][hwName] != None):
                score=json.loads(result[0][hwName])
            sql="SELECT status,datetime FROM userstatus WHERE `userID`=\""+userID+"\" and `homeworkName`=\""+hwName+"\" and `className`=\""+courseName+"\" and `workType`=2 "
            status=db.query(sql,True)
        else:    
            sql="SELECT status,datetime FROM userstatus WHERE `userID`=\""+userID+"\" and `homeworkName`=\""+hwName+"\" and `className`=\""+courseName+"\" and `workType`=1 "
            status=db.query(sql,True)
        upload_datetime="上傳時間 : 還未上傳過"
        if(len(status)==1):
            upload_datetime=datetime.strftime(status[0]["datetime"], '%Y-%m-%d %H:%M:%S')
        print(authorization)
        print(status)
        print(hw_result)
        print(upload_datetime)
        print(score)
        return render_template("homeworkcontent.html",userID=userID,authorization=authorization,homework=hw_result[0],courseName=courseName,score=score,status=status,time=upload_datetime)

@app.route("/remote/getStatus")
@jwt_required()
def getStatus():
    db=DBhandler()
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    sql="SELECT status,datetime FROM userstatus WHERE `userID`=\""+userID+"\" && workType=0"
    status=db.query(sql,True)

    print(status)

    if(len(status)==1):
        upload_datetime=datetime.strftime(status[0]["datetime"], '%Y-%m-%d %H:%M:%S')
        return {
            "success":"t",
            "status":status[0]["status"],
            "time":upload_datetime,
        }
    else:
        return {
            "success":"f"
        }


@app.route("/course/<string:courseName>/<string:hwName>/getSummitStatus")
@jwt_required()
def getSummitStatus(courseName,hwName):
    db=DBhandler()
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    sql="SELECT status,datetime FROM userstatus WHERE className=\""+courseName+"\" && `homeworkName`=\""+hwName+"\"  && `userID`=\""+userID+"\" && workType=2"
    print(sql)
    status=db.query(sql,True)
    print(status)
    if(len(status)==0):
        return {
            "message":"沒有上傳紀錄"
        }
    upload_datetime=datetime.strftime(status[0]["datetime"], '%Y-%m-%d %H:%M:%S')
    score={
        "Scores":"沒有繳交紀錄",
        "test":"沒有成績",
        "test2":"沒有成績",
        "test3":"沒有成績"
    }
    sql="SELECT `"+hwName+"` FROM `"+courseName+"`  WHERE `userID`=\""+userID+"\""
    result = db.query(sql,True)
    print(sql)
    print(result)
    # print(db.query(sql,True)[0][hwName])
    if(len(result) != 0 and result[0][hwName] != None):
        score=json.loads(result[0][hwName])
    if(len(status)==1):
        return {
            "success":"t",
            "status":status[0]["status"],
            "time":upload_datetime,
            "Scores":score["Scores"],
            "test":score["test"],
            "test2":score["test2"],
            "test3":score["test3"]
        }
    else:
        return {
            "success":"f"
        }

    

    

##回傳遠端燒錄的檔案載點
@app.route("/getfile/<string:extension>")
@jwt_required()
def get_file(extension):
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    print(extension)
    print(userID)
    return send_file("../file/"+userID+"/"+userID+"."+extension, as_attachment=True)

##回傳特定作業的固定檔案的載點
@app.route("/staticFile/<string:courseName>/<string:hwName>/<string:fileName>")
@jwt_required()
def get_HWfile(courseName,hwName,fileName):
    return send_file("../file/"+courseName+"/"+hwName+"/"+fileName, as_attachment=True)

##回傳特定作業的非固定檔案的載點
@app.route("/activeFile/<string:courseName>/<string:hwName>")
@jwt_required()
def get_activeHWfile(courseName,hwName):
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    print(userID)
    sql="SELECT txtName FROM "+courseName+"_HW WHERE homeworkName=\""+hwName+"\""
    fileName=db.query(sql,True)[0]["txtName"].replace("pgv","law")
    return send_file("../file/"+courseName+"/"+hwName+"/"+userID+"/"+fileName, as_attachment=True)

@app.route("/file/pgv")
@jwt_required()
def get_pgv_teaching():
    return send_file("../file/pgv.pdf", as_attachment=True)


@app.route('/api/resetpassword', methods=['POST'])
@jwt_required()
def reset_password_mail():
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    sql="SELECT userID,userName FROM `user` WHERE `userID`=\""+userID+"\""
    user_result=db.query(sql,True)
    if len(user_result)!=0:
        token=create_reset_token(userID,user_result[0]["userName"])
        mail.send_resetPassword_mail(userID,token)
        return {
            "message":"go to check email"
        }

##信件當中連結開啟的頁面
@app.route("/resetPassword")
@jwt_required()
def reset_password():
    jwt=JWT_handler()
    db=DBhandler()
    user=jwt.readToken()
    sql="SELECT userID,userName FROM `user` WHERE `userID`=\""+user["user"]+"\""
    user=db.query(sql,True)
    if len(user)!=0:
        return render_template("resetPassword.html",user=user[0])
    
##提交新密碼後的api
@app.route("/api/do_resetPassword",methods=['POST'])
@jwt_required()
def do_resetPassword():
    jwt=JWT_handler()
    db=DBhandler()
    user=jwt.readToken()
    userID=request.form.get("userID")
    userName=request.form.get("userName")
    password=request.form.get("newPassword")
    if user["name"]==userName and user["user"]==userID:
        sql="UPDATE user SET password=\""+generate_password_hash(password)+"\" WHERE `userID` = \""+userID+"\""
        db.query(sql,False)
        return {
            "success":"t",
            "message":"更改密碼成功"
        }
        


##更改密碼認證信的token產生函式
def create_reset_token(userID,userName):
    jwt=JWT_handler()
    data={
        "name":userName,
        "user":userID
    }
    return jwt.makeToken(data)



api.add_resource(User, "/api/User")
api.add_resource(Users, "/api/Users")
api.add_resource(login_handler,"/api/login")
api.add_resource(ProgrammingRequest,"/api/ProgrammingRequest")
api.add_resource(course,"/api/course")
api.add_resource(homework,"/api/homework")
api.add_resource(homeworks,"/api/homeworks")
api.add_resource(member,"/api/member")
#api.add_resource(ProgrammingTest_without_hardware,"/api/ProgrammingRequest")

if __name__ == "__main__":
    app.run(port=8087,debug=True)