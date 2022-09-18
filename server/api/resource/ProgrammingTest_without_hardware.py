from ast import Try
from asyncio.subprocess import PIPE
from pickle import TRUE
from tokenize import Double
from flask import Flask, request
from flask_restful import Resource, Api
from subprocess import PIPE
import sys
import subprocess
import time
import os
import shutil
import threading
# 處理import DBhandler
sys.path.insert(1, 'C:\\git-repos\\ours\\CloudLab\\server')

from api.common.JWT_handler import JWT_handler
from flask_jwt_extended import jwt_required
from api.common.DBhandler import DBhandler
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import datetime

sem = threading.Semaphore()
ALLOWED_EXTENSIONS = {'sof', 'pgv'}

class ProgrammingTest_without_hardware(Resource):
    def get(self):
        return {'Msg': 'This is GET method!'}

    @jwt_required()
    def post(self):
        jwt = JWT_handler()
        user = jwt.readToken()
        # print("Enter post!\nuser:")
        # print(user)
        app = Flask(__name__)
        userID = user['userID']
        print("userID: " + userID)
        #做什麼燒錄動作    例: 0:單純燒錄    1:助教作業上傳    2:學生繳交作業
        try:
            workType = int(request.form.get('workType',-1))
        except Exception:
            print("workType must be int!!")
            workType = -1
        #課程名稱
        className = request.form.get('className','')
        #作業名稱
        homeworkName = request.form.get('homeworkName','')
        #設定資料夾路徑
        # UPLOAD_FOLDER = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + userID
        # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        LAFlag = 0
        succFlag = 0
        uploadFlag = 0
        statusCode = 400
        returnMsg = "Can't program the board!!"
        emailMsg = ""
        #txt files
        file1=""
        file2=""
        file3=""
        differences = []
        judgeResults = []
        hwScores = []
        totalScore = 0
        batPath = "C:\\git-repos\\ours\\CloudLab\\server\\api\\common\\"
        pgvName = ""
        pgvName1 = ""
        pgvName2 = ""
        pgvName3 = ""
        i = 0
        mailText = ""
        judgeFlag = 0
        judgeFlag2 = 0
        judgeFlag3 = 0


        #做檔案的副檔名檢查
        def allowed_file(filename):
            return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        #上傳檔案
        def upload_file(fileKey,type):
            file = request.files[fileKey]
            if file and allowed_file(file.filename):        #檢查副檔名
                # filename = secure_filename(file.filename)    #避免Directory traversal attack
                if(file.filename[-3:] == "pgv" and type != 1):
                    filename = userID + ".pgv"
                elif(file.filename[-3:] == "sof" and type != 1):
                    filename = userID + ".sof"
                else:
                    filename = secure_filename(file.filename)    #避免Directory traversal attack
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   #存檔
                return filename
        #創建資料夾
        def make_dir():
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            #檢查資料夾存不存在，if not then create the folder
            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            else:
                shutil.rmtree(UPLOAD_FOLDER)
                os.mkdir(UPLOAD_FOLDER)

        def make_dirs():
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            #檢查資料夾存不存在，if not then create the folder
            if not os.path.isdir(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            else:
                shutil.rmtree(UPLOAD_FOLDER)
                os.makedirs(UPLOAD_FOLDER)
        #取得pgv檔的波型總時間
        def getWaveTime(pgvPath):
            with open(pgvPath + "\\" + pgvName,'r') as f:
                data = f.read()

                data = data.strip()
                # print(data)
                tmp = data.splitlines()

                timeUnit = tmp[3]
                timeUnit = timeUnit.strip()[5] #取得時間單位
                # print(tmp)

                #取得輸出波型需要幾秒
                if(len(tmp[-1]) == 1):
                    wtime = tmp[-2]
                else:
                    wtime = tmp[-1]
                wtime = wtime[:wtime.rfind('>')].strip()
                # print("wtime:")
                # print(wtime)

                #算出需要多少ms輸出波型
                if timeUnit == 'N' or timeUnit == 'n':
                    wave_Time = float(wtime) * pow(10,-6)
                if timeUnit == 'U' or timeUnit == 'u':
                    wave_Time = float(wtime) * pow(10,-3)
                if timeUnit == 'M' or timeUnit == 'm':
                    wave_Time = float(wtime)

                print("Time is {}ms".format(str(wave_Time)))
                return wave_Time
        #作業txt檔的比對
        def judgeHomework(comparedpgvFile,i = 0):
            compareFile = UPLOAD_FOLDER + "\\" + comparedpgvFile
            answerFile = homeworkPath + "\\" + comparedpgvFile
            recordFile = UPLOAD_FOLDER + "\\diff" + str(i) + ".txt"
            diff = 0
            x = 0

            try:
                with open(compareFile,'r',encoding='utf-8') as fp1,open(answerFile,'r',encoding='utf-8') as fp2,open(recordFile,'w',encoding='utf-8') as fp3:
                    for line,line2 in zip(fp1,fp2):
                        x += 1
                        line = line.strip()
                        line2 = line2.strip()
                        if(line != line2):
                            diff += 1
                            fp3.write("diff at " + str(x) + " :" + line + " "+  line2 + "\n")
                #比對完之後，看跟解答誤差多少，之後拿來判斷是否錯誤
                differences.append(diff)
                return True
            except Exception as err:
                print("Homework judge error:")
                print(err)
                return False

        def randomJudge():
            x = random.random()
            
            if(x >= 0.5):
                return True
            else:
                return False
        
        def writeStatusIntoSql(type,status):
            db = DBhandler('localhost','root','','remote_lab')
            cName = "NULL"
            hName = "NULL"

            if(type == 0):
                sqlStatement = "SELECT * FROM userStatus WHERE userID = '" + userID + "' and workType = '0';"
            elif(type == 1):
                cName = className
                hName = homeworkName
                sqlStatement = "SELECT * FROM userStatus WHERE userID = '" + userID + "' and workType = '1' and className = '" + className + "' and homeworkName = '" + homeworkName + "';"
            else:
                cName = className
                hName = homeworkName
                sqlStatement = "SELECT * FROM userStatus WHERE userID = '" + userID + "' and workType = '2' and className = '" + className + "' and homeworkName = '" + homeworkName + "';"

            result = db.query(sqlStatement,True)
            # print("result:" + str(result))
            #取得目前時間
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if(len(result) == 0):
                if(type == 0):
                    sqlStatement = "INSERT INTO userStatus VALUES('" + str(userID) + "','" + str(status) + "','0',NULL,NULL,'" + dt + "');"
                elif(type == 1):
                    sqlStatement = "INSERT INTO userStatus VALUES('" + str(userID) + "','" + str(status) + "','1','" + cName + "','" + hName + "','" + dt + "');"
                else:
                    sqlStatement = "INSERT INTO userStatus VALUES('" + str(userID) + "','" + str(status) + "','2','" + cName + "','" + hName + "','" + dt + "');"
            else:
                if(type == 0):
                    sqlStatement = "UPDATE userStatus SET `status` = '{}', `datetime` = '{}' WHERE userID = '{}' and workType = '0';".format(status,dt,userID)
                elif(type == 1):
                    sqlStatement = "UPDATE userStatus SET `status` = '{}', `datetime` = '{}' WHERE userID = '{}' and workType = '1' and className = '{}' and homeworkName = '{}';".format(status,dt,userID,cName,hName)
                else:
                    sqlStatement = "UPDATE userStatus SET `status` = '{}', `datetime` = '{}' WHERE userID = '{}' and workType = '2' and className = '{}' and homeworkName = '{}';".format(status,dt,userID,cName,hName)

            # print("The sqlStatement:" + sqlStatement)
            db.query(sqlStatement,False)
                    # db.query("INSERT INTO `orderQueue` VALUES('','0','" + userID + "')",False)
            del db
            


        writeStatusIntoSql(workType,0)
        # 設定上傳檔案的路徑
        if(workType == 0):     # 0:單純燒錄
            # i用來決定要燒幾次
            i = 1
            UPLOAD_FOLDER = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + userID
            if (userID == ''):
                returnMsg = "userID is empty!!"
            else:
                try:
                    make_dir()
                    sofName = upload_file("sofFile",0)
                    pgvName = upload_file("pgvFile",0)
                    uploadFlag = 1
                except Exception as er:
                    returnMsg = "Upload the files failed!!" + str(er)
                    print("Error:")
                    print(str(er))
            
        elif(workType == 1):                    # 1:助教作業上傳
            i = 3
            UPLOAD_FOLDER = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + homeworkName
            if(className == ''):
                returnMsg = "className is empty!!"
            elif(homeworkName == ''):
                returnMsg = "homeworkName is empty!!"
            else:
                try:
                    make_dirs()
                    #上傳sof,pgv檔到files
                    sofName = upload_file("sofFile",1)
                    pgvName1 = upload_file("pgvFile",1)
                    pgvName2 = upload_file("pgvFile2",1)
                    pgvName3 = upload_file("pgvFile3",1)
                    homeworkPath = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + homeworkName
                    uploadFlag = 1
                except Exception as er:
                    returnMsg = "Upload the files failed!! " + str(er)
                    print("Error:")
                    print(str(er))
        elif(workType == 2):                    # 2:學生繳交作業
            i = 3
            UPLOAD_FOLDER = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + homeworkName + "\\" + userID
            if(className == ''):
                returnMsg = "Class's name is empty!!"
            elif(homeworkName == ''):
                returnMsg = "Homework's name is empty!!"
            else:
                try:
                    make_dir()
                    sofName = upload_file("sofFile",2)
                    homeworkPath = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + homeworkName
                    ###去資料庫抓作業PGV檔的檔名
                    db = DBhandler('localhost','root','','remote_lab')
                    # #取得courseID
                    # sqlStatement = "SELECT courseID FROM courses WHERE `courseName` = '" + className + "';"
                    # result = db.query(sqlStatement,True)
                    # # print("The result:")
                    # # print(result[0]['courseID'])
                    tableName = className + "_HW"
                    #get the pgv files name
                    sqlStatement = "SELECT txtName,txtName2,txtName3 FROM " + tableName + " WHERE homeworkName = '" + homeworkName + "';"
                    result = db.query(sqlStatement,True)
                    # print("The result:")
                    # print(result)
                    pgvName1 = result[0]['txtName']
                    file1 = pgvName1[:-4] + ".txt"
                    pgvName2 = result[0]['txtName2']
                    file2 = pgvName2[:-4] + ".txt"
                    pgvName3 = result[0]['txtName3']
                    file3 = pgvName3[:-4] + ".txt"
                    # print("pgvName:")
                    # print(pgvName1)
                    # print(pgvName2)
                    # print(pgvName3)
                    ###

                    # ###讀取每個測資的分數
                    # sqlStatement = "SELECT score,score2,score3 FROM " + tableName + " WHERE homeworkName = '" + homeworkName + "';"
                    # result = db.query(sqlStatement,True)
                    # hwScores.append(result[0]['score'])
                    # hwScores.append(result[0]['score2'])
                    # hwScores.append(result[0]['score3'])
                    # ###

                    del db   #釋放db資源
                    uploadFlag = 1
                except Exception as er:
                    returnMsg = "Upload the files failed!!" + str(er)
                    print("Error:")
                    print(str(er))

        # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        # try:
        #     #檢查資料夾存不存在，if not then create the folder
        #     if not os.path.isdir(UPLOAD_FOLDER):
        #         os.mkdir(UPLOAD_FOLDER)
        #     else:
        #         shutil.rmtree(UPLOAD_FOLDER)
        #         os.mkdir(UPLOAD_FOLDER)

        #     #上傳sof,pgv檔到files
        #     sofName = upload_file("sofFile")
        #     pgvName = upload_file("pgvFile")
        #     print("folder route: " + UPLOAD_FOLDER)
        #     print("\npgvName: " + pgvName)
        #     print("\nupload finished!")
        #     uploadFlag = 1
        # except Exception as er:
        #     print("Error:")
        #     print(str(er))

        if(uploadFlag):
            #燒錄程式開始，使用semaphore來管理同步
            sem.acquire()
            print("enter sem!")
            ### write Quartus programming bat file
            with open(batPath + "Programming_run.bat",'w') as fileWrite:
                fileWrite.write("cd " + UPLOAD_FOLDER)
                fileWrite.write("\nC:\\altera\\13.0\\quartus\\bin64\\quartus_pgm.exe -m JTAG -o p;{}".format(sofName))
            ###

            #因為作業上傳和作業評測都用同一個sof檔，所以只要燒一次就好
            try:
                #依照workType會決定做幾次燒錄動作
                for j in range(i):
                # try:
                    #燒錄程式開始，使用semaphore來管理同步
                    # sem.acquire()
                    # print(pgvDataPath['codePath'])

                    # batPath = "..\\common\\PG_run.bat"
                    #根據workType的不同，內容也會跟著不同
                    if(workType == 0):
                        
                        waveTime = getWaveTime(UPLOAD_FOLDER)
                        ###write PG_run bat file
                        with open(batPath + "PG_run.bat",'w') as fileWrite:
                            fileWrite.write("cd " + UPLOAD_FOLDER)
                            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\PG_run\\bin\\x86\\Debug\\PG_1.exe {} {}".format(pgvName,str(waveTime)))
                        ###

                        ### write Quartus programming bat file
                        # with open(batPath + "Programming_run.bat",'w') as fileWrite:
                        #     fileWrite.write("cd " + UPLOAD_FOLDER)
                        #     fileWrite.write("\nC:\\altera\\13.0\\quartus\\bin64\\quartus_pgm.exe -m JTAG -o p;{}".format(sofName))
                        ###

                        ### write LA bat file
                        with open(batPath + "LA_run.bat",'w') as fileWrite:
                            fileWrite.write("cd " + UPLOAD_FOLDER)
                            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\LA_run\\bin\\Debug\\C_Sharp.exe {}".format(userID))
                        ###
                        time.sleep(3)
                       
                    elif(workType == 1):
                        if(j == 0):
                            pgvName = pgvName1
                        elif(j == 1):
                            pgvName = pgvName2
                        elif(j == 2):
                            pgvName = pgvName3
                        
                        print("the pgvName:" + pgvName)
                        #取得波型長度
                        waveTime = getWaveTime(UPLOAD_FOLDER)

                        #write PG bat file
                        with open(batPath + "PG_run.bat",'w') as fileWrite:
                            fileWrite.write("cd " + UPLOAD_FOLDER)
                            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\PG_run\\bin\\x86\\Debug\\PG_1.exe {} {}".format(pgvName,str(waveTime)))

                        ### write LA bat file
                        with open(batPath + "LA_run.bat",'w') as fileWrite:
                            fileWrite.write("cd " + UPLOAD_FOLDER)
                            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\LA_run_0\\bin\\Debug\\C_Sharp.exe {} {} {}".format(homeworkPath,pgvName[:-4],"0"))
                        ###

                        time.sleep(3)
                        
                    elif(workType == 2):
                        if(j == 0):
                            pgvName = pgvName1
                        elif(j == 1):
                            pgvName = pgvName2
                        elif(j == 2):
                            pgvName = pgvName3
                        
                        waveTime = getWaveTime(homeworkPath)

                        #write PG bat file
                        with open(batPath + "PG_run.bat",'w') as fileWrite:
                            fileWrite.write("cd " + homeworkPath)
                            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\PG_run\\bin\\x86\\Debug\\PG_1.exe {} {}".format(pgvName,str(waveTime)))

                        ### write LA bat file
                        with open(batPath + "LA_run.bat",'w') as fileWrite:
                            fileWrite.write("cd " + UPLOAD_FOLDER)
                            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\LA_run_0\\bin\\Debug\\C_Sharp.exe {} {} {}".format(UPLOAD_FOLDER,pgvName[:-4],"1"))
                        ###

                        time.sleep(3)
                    
                    time.sleep(1) #sleep for LA
                    # sem.release()

                    # db = DBhandler('localhost','root','','remote_lab')

                    # result = db.query("SELECT COUNT(*) FROM orderQueue",True)

                    # # print(result[0]['COUNT(*)'])
                    # print("DB rowcount:" + str(result[0]['COUNT(*)']) + "\n")

                    # #table is empty
                    # if(result[0]['COUNT(*)'] == 0):
                    #     #重設order順序 = 1
                    #     db.query("ALTER TABLE orderQueue AUTO_INCREMENT = 1",False) 

                    # db.query("INSERT INTO `orderQueue` VALUES('','0','" + userID + "')",False)

                    #系統沒再燒錄程式
                    # if(result != 0):
                    #     print("table is empty")
                    #     subprocess.Popen(["python3","RunProgramming.py"])
                #程式燒錄成功
                succFlag = 1

                ###把測資的檔名寫進資料庫
                if(succFlag and workType == 1):
                    #create database conn
                    db = DBhandler('localhost','root','','remote_lab')

                    tableName = className + "_HW"

                    sqlStatement = "UPDATE " + tableName + " SET `txtName` = '" + pgvName1 + "', `txtName2` = '" + pgvName2 + "', `txtName3` = '" + pgvName3 + "' WHERE `homeworkName` = '" + homeworkName + "';"
                    db.query(sqlStatement,False)
                    print("the sqlStatement:")
                    print(sqlStatement)

                ###比對txt檔案來看對不對
                if(succFlag and workType == 2):
                    judgeFlag = True
                    judgeFlag2 = True
                    judgeFlag3 = True

                    
                    db = DBhandler('localhost','root','','remote_lab')

                    ###讀取每個測資的分數
                    sqlStatement = "SELECT score,score2,score3 FROM " + tableName + " WHERE homeworkName = '" + homeworkName + "';"
                    result = db.query(sqlStatement,True)
                    hwScores.append(result[0]['score'])
                    hwScores.append(result[0]['score2'])
                    hwScores.append(result[0]['score3'])
                    ###

                    ###把作業結果寫進資料庫
                        #先檢查這一欄創好了沒
                    sqlStatement = "SHOW COLUMNS FROM `" + tableName[0:-3]  + "` LIKE '" + homeworkName  + "';"
                    result = db.query(sqlStatement,True)
                    # print("column result:")
                    # print(len(result))
                        #如果沒創，就創這欄位
                    if(len(result) == 0):
                        sqlStatement = "ALTER TABLE `" + tableName[0:-3] + "` ADD " + homeworkName + " JSON;"
                        db.query(sqlStatement,False)

                    for k in range(3):
                        #誤差設0.1%，超過就算錯
                        if(randomJudge()):
                            totalScore += float(hwScores[k])
                            judgeResults.append("Correct")
                        else:
                            judgeResults.append("Wrong")

                    sqlStatement = "UPDATE `" + tableName[:-3] + "` SET `" + homeworkName + "` = '{\"Scores\" : \"" + str(totalScore) + "\", \"test\" : \"" + judgeResults[0] + "\", \"test2\" : \"" + judgeResults[1] + "\", \"test3\" : \"" + judgeResults[2] + "\"}' WHERE userID = '" + userID + "';"
                    db.query(sqlStatement,False)
                    print("the sqlStatement:")
                    print(sqlStatement)

                    del db #釋放db資源
                                                
                    ###        
                ###

                ###programming successful -> email letter to notice the user
                # content = MIMEMultipart()  #建立MIMEMultipart物件
                # content["subject"] = "遠端實驗室程式燒錄"  #郵件標題
                # content["from"] = "oceanremotelab@gmail.com"  #寄件者
                # content["to"] = userID + "@mail.ntou.edu.tw" #收件者
                # content.attach(MIMEText("您的程式燒錄成功!!"))  #郵件內容
                #ckystilkvgqxnodh

                # with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
                #     try:
                #         smtp.ehlo()  # 驗證SMTP伺服器
                #         smtp.starttls()  # 建立加密傳輸
                #         smtp.login("oceanremotelab@gmail.com", "ckystilkvgqxnodh")  # 登入寄件者gmail
                #         smtp.send_message(content)  # 寄送郵件
                #         print("Email complete!")
                #     except Exception as e:
                #         emailMsg = "But email failed!"
                #         print("Email Error message: ", e)    
                ###
            except Exception as err:
                succFlag = 0
                print("Error: " + str(err))
                # if(LAFlag and LA_process.poll() is None):
                #     print("kill the LA_process!")
                #     LA_process.kill()
                    # sem.release()
            sem.release()
            # print("out of sem!")
            # print("The floder: " + UPLOAD_FOLDER)

        # if(LAFlag and LA_process.poll() is None):
        #     print("kill the LA_process!")
        #     LA_process.kill()
        
        # time.sleep(15)
        # sem.release()
        print("out of sem!")
        writeStatusIntoSql(workType,1)
        # print("The floder: " + UPLOAD_FOLDER)

        
        ###programming successful -> email letter to notice the user
        # content = MIMEMultipart()  #建立MIMEMultipart物件
        # content["subject"] = "遠端實驗室程式燒錄"  #郵件標題
        # content["from"] = "oceanremotelab@gmail.com"  #寄件者
        # content["to"] = userID + "@mail.ntou.edu.tw" #收件者
        # if(succFlag):
        #     if(workType == 0):
        #         content.attach(MIMEText("您的程式燒錄成功!!"))  #郵件內容
        #     elif(workType == 1):
        #         content.attach(MIMEText("您的作業創建成功!!"))  #郵件內容
        #     elif(workType == 2):
        #         if(judgeFlag and judgeFlag2 and judgeFlag3):
        #             content.attach(MIMEText("您的作業上傳成功!!"))  #郵件內容
        #         else:
        #             content.attach(MIMEText("您的作業上傳失敗!!\n請再重新上傳一次"))  #郵件內容
        # else:
        #     if(workType == 0):
        #         content.attach(MIMEText("您的程式燒錄失敗!!\n請再重新上傳一次"))  #郵件內容
        #     elif(workType == 1):
        #         content.attach(MIMEText("您的作業創建失敗!!\n請再重新上傳一次"))  #郵件內容
        #     elif(workType == 2):
        #         content.attach(MIMEText("您的作業上傳失敗!!\n請再重新上傳一次"))  #郵件內容
        # # ckystilkvgqxnodh

        # with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        #     try:
        #         smtp.ehlo()  # 驗證SMTP伺服器
        #         smtp.starttls()  # 建立加密傳輸
        #         smtp.login("oceanremotelab@gmail.com", "ckystilkvgqxnodh")  # 登入寄件者gmail
        #         smtp.send_message(content)  # 寄送郵件
        #         print("Email complete!")
        #     except Exception as e:
        #         emailMsg = "But email failed!"
        #         print("Email Error message: ", e)    
        # ###

        # print("\ngo to the program end!!\n")
        if(succFlag):
            if(workType == 0):
                return {"success": "True",'Message': 'Program the board successful!' + emailMsg},201
            elif(workType == 1):
                return {"success": "True",'Message': 'Create the homework successful!' + emailMsg},201
            elif(workType == 2):
                if(judgeFlag and judgeFlag2 and judgeFlag3):
                    return {"success": "True",'Message': 'Homework judge successful!' + emailMsg},200
                else:
                    return {"success": "False",'Message': 'Homework judge Failed!' + emailMsg},200
        else:
            return {"success": "False",'Message': returnMsg},400


# api.add_resource(ProgrammingRequest, '/api/ProgrammingRequest')

# if __name__ == '__main__':
#     app.run(debug=True)     #如果寫完要記得把debug模式刪掉