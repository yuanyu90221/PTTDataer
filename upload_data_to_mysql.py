
# 2017/10/5 測試可執行

# 該程式提供可上傳 data 的帳號，在各位進行 data clean 後，一個上傳/分享的管道，
# 這樣就不需要每個人都進行 data clean，合作的概念。程式中提供一個 建立 data file 和上傳 data 的範例。
# 註：clean data 另外儲存在 clean_data 資料庫中
# upload_user 帳號提供對於 clean_data 資料庫上傳、新增、修改的權限，並能建立自己的 data table
import pymysql

host = '114.32.89.248'

# 建立 SQL 檔案
def creat_sql_file(sql_string,dataset_name):
    conn = ( pymysql.connect(host = host,# SQL IP
                             port = 3306,
                             user='guest',# 帳號
                             password='123',# 密碼
                             database='guest_dataset',  # 資料庫名稱
                             charset="utf8") )   #  編碼           
    c=conn.cursor()
    c.execute( sql_string )# 建立新的 SQL file
    # 加 PRIMARY KEY 
    c.execute('ALTER TABLE `'+dataset_name+'` ADD id BIGINT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY;')
    c.close() # 關閉與 SQL 的連接
    conn.close()# 關閉與 SQL 的連接
    
def create_ptt_dataset(dataset_name='test'):    
    sql_string = ( 'create table ' + dataset_name + '( i text(100),date text(100) )' )
    creat_sql_file(sql_string,dataset_name)     

#------------------------------------------------------------
# 建立 data file    
create_ptt_dataset('test')

conn = ( pymysql.connect(host = host,# SQL IP
                         port = 3306,
                         user='guest',# 帳號
                         password='123',# 密碼
                         database='guest_dataset',  # 資料庫名稱
                         charset="utf8") )   #  編碼   


# 將 data 匯入 test file 中, test file 是由 create_ptt_dataset 建立, 作為範例使用
for i in range(1,4,1):
    print(i)
    id = str( i )
    date = '2017-03-0' + str(i)
    
    ( conn.cursor().execute(    'insert into ' + 
                                'test' + '(i,date)'
                                ' values(%s,%s)',
                                ( id,date ) ) )

conn.commit()
# this command is stop connect, you must run it
# 關閉 connect, 否則將無法結束上傳的動作
conn.close()




