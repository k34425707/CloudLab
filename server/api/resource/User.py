'''
更改一個User的resource
及提供的function
'''
from flask import jsonify,request
from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
from werkzeug.security import generate_password_hash

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
class User(Resource):
    
    
    '''
    要登陸才能執行
    把所有資料庫的user讀出出來
    '''
    def __init__(self) -> None:
        #繼承上層Resource的init
        super().__init__()  
        self.db_handler=DBhandler()
    
    def get(self):
        id="test"
        results=self.db_handler.query("SELECT * FROM `user` WHERE `userID`={}".format(id),True)
        return jsonify(results[0])
        
        
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uId', required=True)
        parser.add_argument('uName', required=True)
        arg=parser.parse_args()

        sql="INSERT INTO `user`(`userID`,`password`,`userName`,`course`,`authorization`) VALUES (\"{}\",\"{}\",\"{}\",\'{}\',\"{}\")".format(arg['uId'],generate_password_hash(arg["uId"]),arg['uName'],"","1")
        self.db_handler.query(sql,False)

        

    def put(self):
        pass

