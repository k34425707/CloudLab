from asyncio.subprocess import PIPE
from flask import Flask, request
from flask_restful import Resource, Api
from subprocess import PIPE
import subprocess
import time
import os
import shutil
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'sof', 'pgv'}
app = Flask(__name__)
api = Api(app)

class HomeworkJudge(Resource):
    '''
    利用form-data傳資料
    上傳完SOF檔之後，先拿作業的pgv檔做燒路，順便把波型檔輸出成txt檔案，和學生的sof檔一起存在資料夾內，然後拿這個txt檔案去跟助教燒出來的做比對，如果對回傳true，否則false
    Inputs:
        className:哪個課程
        homeworkName:課程的哪個作業           我的想法:/files/課程名稱/課程作業
        userID:學生的帳號
        sofFile:sof檔案    <input type=file name=sofFile>
        pgvFile:pgv檔案
        pgvFile2:pgv檔案
        pgvFile3:pgv檔案
    Outputs:
        json:{"score": ?
              "openResult" : "true or false"}
        True or False
    '''
    def get(self):
        return {'Msg': 'This is GET method!'}
    def post(self):
        #設定資料夾路徑
        
        LAFlag = 0
        succFlag = 0
        className = request.form["className"]
        homeworkName = request.form["homeworkName"]
        UPLOAD_FOLDER = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + homeworkName
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        # JWT = JWT_handler()
        # JWT.readToken()

        #做檔案的副檔名檢查
        def allowed_file(filename):
            return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
        def upload_file(fileKey):
            file = request.files[fileKey]
            if file and allowed_file(file.filename):        #檢查副檔名
                filename = secure_filename(file.filename)    #避免Directory traversal attack
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   #存檔
                return filename

        # pgvDataPath = request.get_json()
        try:
            print("debug1")
            #檢查資料夾存不存在，if not then create the folder
            if not os.path.isdir(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            else:
                shutil.rmtree(UPLOAD_FOLDER)
                os.makedirs(UPLOAD_FOLDER)
            print("debug2")
            #上傳sof,pgv檔到files
            sofName = upload_file("sofFile")
            pgvName1 = upload_file("pgvFile")
            pgvName2 = upload_file("pgvFile2")
            pgvName3 = upload_file("pgvFile3")
            print("debug3")

            # print(pgvDataPath['codePath'])
            batPath = "C:\\git-repos\\ours\\CloudLab\\server\\api\\common\\"

            # batPath = "..\\common\\PG_run.bat"

            homeworkPath = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + homeworkName

            ### write Quartus programming bat file
            with open(batPath + "Programming_run.bat",'w') as fileWrite:
                fileWrite.write("cd " + UPLOAD_FOLDER)
                fileWrite.write("\nC:\\altera\\13.0\\quartus\\bin64\\quartus_pgm.exe -m JTAG -o p;{}".format(sofName))
            ###
            ### programming the DE0 board
            print("programming process\n")
            programming_process = subprocess.Popen([batPath + "Programming_run.bat"],stdout = PIPE) # run Programming_run.bat
            programming_out = programming_process.communicate()    #取得stdout 來判斷執行結果是否正確
            print("out of programming process")
            time.sleep(5)
            # print(type(programming_out)).

            # print(str(programming_out[0]).split('\\r\\n')[-2].strip())
            if(str(programming_out[0]).split('\\r\\n')[-2].strip()[:5] == "Error"):   #can't program the DE0 board
                raise Exception("Error0!Can't program the board!")
            # print(type(programming_out[1]))
            ###

            for i in range(3):
                if(i == 0):
                    pgvName = pgvName1
                elif(i == 1):
                    pgvName = pgvName2
                elif(i == 2):
                    pgvName = pgvName3
            ###write PG_run bat file
                with open(UPLOAD_FOLDER + "\\" + pgvName,'r') as f:
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

                    #算出需要多少ms輸出波型
                    if timeUnit == 'N' or timeUnit == 'n':
                        waveTime = float(wtime) * pow(10,-6)
                    if timeUnit == 'U' or timeUnit == 'u':
                        waveTime = float(wtime) * pow(10,-3)
                    if timeUnit == 'M' or timeUnit == 'm':
                        waveTime = float(wtime)

                    print("Time is {}ms".format(str(waveTime)))


                with open(batPath + "PG_run.bat",'w') as fileWrite:
                    fileWrite.write("cd " + UPLOAD_FOLDER)
                    fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\PG_run\\bin\\x86\\Debug\\PG_1.exe {} {}".format(pgvName,str(waveTime)))
                ###

                ### write LA bat file
                with open(batPath + "LA_run.bat",'w') as fileWrite:
                    fileWrite.write("cd " + UPLOAD_FOLDER)
                    fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\LA_run_0\\bin\\Debug\\C_Sharp.exe {} {} {}".format(homeworkPath,pgvName[:-4],i))
                ###

                ###Run the logic analysis(LA)
                print("LA process\n")
                LAFlag = 1
                LA_process = subprocess.Popen([batPath + "LA_run.bat"])
                time.sleep(20)
                ###

                ### Run the pattern generator(PG)
                print("PG process")
                PG_process = subprocess.Popen([batPath + "PG_run.bat"],stdout = PIPE)  #run PG_run.bat
                PG_out = PG_process.communicate()    #取得stdout and stderr 來判斷執行結果是否正確
                print(str(PG_out[0]).split('\\r\\n'))
                # print(str(PG_out[0]).split('\\r\\n')[-3][:5].strip())
                if(str(PG_out[0]).split('\\r\\n')[-3][:5].strip() == "Error"):
                    raise Exception("Error1!Can't generate pattern to board!")
                ###

                time.sleep(30) #sleep for LA
            succFlag = 1
        except Exception as err:
            succFlag = 0
            # state = int(str(err)[5])
            print(str(err))

        if(LAFlag and LA_process.poll() is None):
            print("kill the LA_process!")
            LA_process.kill()

        

        print("go to the program end!!\n")
        if(succFlag):
            return {'Msg': 'Running the program!'}
        else:
            return {'Msg': 'Error occurred!'}

api.add_resource(HomeworkJudge, '/api/HomeworkJudge')

if __name__ == '__main__':
    app.run(debug=True)     #如果寫完要記得把debug模式刪掉