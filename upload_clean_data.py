

import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import pymysql

# 建立 SQL 檔案
def creat_sql_file(sql_string):
    conn = ( pymysql.connect(host = 'linsam.servehttp.com',# SQL IP
                             port = 3306,
                             user='upload_user',# 帳號
                             password='f496328mm',# 密碼
                             database='clean_data',  # 資料庫名稱
                             charset="utf8") )   #  編碼           
    c=conn.cursor()
    c.execute( sql_string )# 建立新的 SQL file
    c.close() # 關閉與 SQL 的連接
    conn.close()# 關閉與 SQL 的連接
    
def create_ptt_dataset(dataset_name='test'):    
    sql_string = ( 'create table ' + dataset_name + '( id text(100),date text(100) )' )
    creat_sql_file(sql_string)     

#------------------------------------------------------------
# 建立 data file    
create_ptt_dataset('test')

conn = ( pymysql.connect(host = 'linsam.servehttp.com',# SQL IP
                         port = 3306,
                         user='upload_user',# 帳號
                         password='f496328mm',# 密碼
                         database='clean_data',  # 資料庫名稱
                         charset="utf8") )   #  編碼   


# 將 data 匯入 test file 中
for i in range(1,4,1):
    print(i)
    id = str( i )
    date = '2017-03-0' + str(i)
    
    ( conn.cursor().execute(    'insert into ' + 
                                'test' + 
                                ' values(%s,%s)',
                                ( id,date ) ) )

conn.commit()
# this command is stop connect, you must run it
# 關閉 connect, 否則將無法結束上傳的動作
conn.close()




