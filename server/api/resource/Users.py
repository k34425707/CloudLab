'''
更改全部User的resource
及提供的function
我假設他匯入學號檔案csv寫在這
'''
from flask import jsonify
from flask_restful import Resource
from common.DBhandler import DBhandler
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
    
           
    def get(self):
        results=self.db_handler.query("SELECT * FROM `user`",True)
        '''
        我不確定多個json資料可不可以放在陣列
        感覺合法
        但有點奇怪
        return jsonify(results)
        '''
        #有多筆資料
        items={}
        for i in range(0,len(results)):
            items.update({i:results[i]})
        return jsonify(items)

            
        
        
    
    '''
    給路徑檔名csv
    輸入到資料庫
    '''
    def post(self,path="../file/user.csv"):
        with open(path, mode='r',newline='') as csvfile:
        
            # 讀取 CSV 檔案內容
            rows = csv.reader(csvfile)
            '''
            這裡要取決修課名單的格式
            '''
            # 以迴圈輸出每一列
            for row in rows:
                sql="INSERT INTO `user`(`uId`,`uPassword`,`uName`,`uPrivilege`) VALUES (%s,%s,%s,%s)"
                self.db_handler.query("INSERT INTO `user`(`uId`={},`uPassword`={},`uName`={},`uPrivilege`={}".format(row[0],'a'+row[0],row[1],'0'))

    def put(self):
        pass
    def delete(self):
        global users
        users = [item for item in users if item['name'] != name]
        return {
            'message': 'Delete done!'
        }