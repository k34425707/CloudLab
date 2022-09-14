from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
from common.JWT_handler import JWT_handler

class login_handler(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db=DBhandler()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uId')
        parser.add_argument('uPassword')
        arg=parser.parse_args()
        self.sql="SELECT * FROM user where `userID` = \""+arg['uId']+"\""
        result=self.db.query(self.sql,True)
        if(len(result)==1):
            #暫時先不加密處理，之後再改
            if(arg['uPassword']==result[0]['password']):
                jwt=JWT_handler()
                return {
                    "jwt_token":jwt.makeToken(result[0]),
                    "success":"t",
                    "message":"login success"
                }
        
        return {
            "success":"f",
            "message":"username or password wrong!"
        }
'''
login{
    method:post
    url:/api/login
    data:{
        uId:,
        uPassword
    }
}

login-response

1.登入失敗:
{
    "success":"f",
    "message":"username or password wrong!"
}

2.登入成功:
{
    "jwt_token":token,(儲存在某個地方)
    "success":"t",
    "message":"login success"
}
'''