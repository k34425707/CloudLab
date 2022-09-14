import pymysql.cursors
import csv


'''
加一筆資料到sql
'''
def add_user(uId,uName):
    #連線資料庫
    connection=pymysql.connect(host='localhost',user='root',password='',db='lab',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    
    try:
        #從數據庫鏈接中得到cursor的數據結構
        with connection.cursor() as cursor:
            #在之前建立的user表格基礎上，插入新數據，這裡使用了一個預編譯的小技巧，避免每次都要重複寫sql的語句
            sql="INSERT INTO `user`(`uId`,`uPassword`,`uName`,`uPrivilege`) VALUES (%s,%s,%s,%s)"
            #uPassword:預設a加學號
            cursor.execute(sql,(uId,'a'+uId,uName,int()))
            #執行到這一行指令時才是真正改變了數據庫，之前只是緩存在內存中
    finally:
        connection.commit()
'''
匯入csv檔
到sql
'''
def import_user(file_name):
    
    
    # 開啟 CSV 檔案
    with open(file_name, mode='r',newline='') as csvfile:
        
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        # 以迴圈輸出每一列
        for row in rows:
            
            add_user(row[0],row[1])
            
            
            
            
if __name__=='__main__':
    import_user("user.csv")