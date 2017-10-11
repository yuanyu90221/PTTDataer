# -*- coding: utf-8 -*-

# 該程式為測試用
# 連接 SQL 下載 DATA 範例請參考 py_connect_sql_example.py
# 連接 SQL 上傳 DATA 範例請參考 upload_clean_data.py

import pymysql
import pandas as pd

#---------------------------------------------------------------
# 連接 server, host 是 ip 位置, 
# 'text_mining' 是帳號, 密碼部分請 email 詢問我
# connect our server, and 'origin_data' is name of dataset 
# host is ip address, 
# 'text_mining' is user, 
# if your wnat password, please email to me
#---------------------------------------------------------------
conn = ( pymysql.connect(host = '114.34.138.146',
                         port = 3306,
                         user='text_mining',
                         password='password',
                         database='ptt_data1.0',  
                         charset="utf8") )     
                         
#---------------------------------------------------------------
# 建立你需要 data 的格式, 
# 例如 id date 需要文字型態, 其他型態請自行 google
# create your data format
# ex : your data name is article_date and following is your data
# id   date
# 1    2017-03-01
# 2    2017-03-02
# 3    2017-03-03
# then sql_string = 'create table article_date( test id(100), date text(100) )'
#---------------------------------------------------------------                         
# ex :     
# 建立 table, 舉例來說, 
# 你的 data 希望命名為 article_date 
# id, date 格式是 text, 長度為 100 
sql_string = (  'create table article_date( '+
                'id text(100),'+
                'date text(100) )' 
                )
# 將以上 SQL 指令丟到 MYSQL 去初始化你的 data 
conn.cursor().execute( sql_string )
# 如果出現以下 error, 代表名稱重複
# if error : (1050, "Table 'article_date' already exists")
# that means you need change your data name
#---------------------------------------------------------------                         
# update data to MYSQL
# 將資料 update 到 MYSQL, 以上面的 data 為例
# id   date
# 1    2017-03-01
# 2    2017-03-02
# 3    2017-03-03
# ex : 
for i in range(1,4,1):
    print(i)
    id = str( i )
    date = '2017-03-0' + str(i)
    
    ( conn.cursor().execute(    'insert into ' + 
                                'article_date' + 
                                ' values(%s,%s)',
                                ( id,date ) ) )

# update data to MYSQL
conn.commit()
# this command is stop connect, you must run it
# 關閉 connect, 否則將無法結束上傳的動作
conn.close()
# 現在, 你的 data 已經成功上傳到 server 上, 
# 可以開 http://114.34.138.146/phpmyadmin/index.php 進行查看
# now, your data have been updated to article_date in MYSQL
#---------------------------------------------------------------                         
#---------------------------------------------------------------                         
#---------------------------------------------------------------                         
# 在以上指令後, 你已經會上傳 data, 那要如何下載 data 呢?
# you can input data, then how take data from MYSQL?
conn = ( pymysql.connect(host = '114.34.138.146',
                         port = 3306,
                         user='text_mining',
                         password='password',
                         database='ptt_data1.0',  
                         charset="utf8") )     
                         
cursor = conn.cursor()                         
# input data from article_date
cursor.execute('select * from article_date')
# 抓所有的 data
data = cursor.fetchall()
# close connect
conn.close()
#---------------------------------------------------------------                         
# 從 MYSQL 抓下來的型態為 tuple, 不利於分析, 
# 一般是使用 dataframe, 因此進行轉換
# type of data is tuple, we can change to dataframe
print( type( data ) )

id = []
date = []
for d in data:
    id.append( d[0] )
    date.append( d[1] )

data = {
    'id' : id,
    'date' : date}

data = pd.DataFrame(data)
# 轉換成功
#--------------------------------------------------------------- 
# col 預測按照 a-z 進行排序, 如果不喜歡, 可以進行以下調整                        
# if you want change column
cols = (['id','date'])
data = data[cols]
data

# end ---------------------------------------------------------








                         
                         

                         
                         
                         
                         
                         
                         
