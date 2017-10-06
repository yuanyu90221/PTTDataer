# -*- coding: utf-8 -*-

# 開程式，可自由取得 SQL 中的 data，並將格式轉為 dataframe ，利於分析


import pymysql
import pandas as pd
import re
import datetime

def input_data_from_SQL(data_name = 'ptt_job'):
    #---------------------------------------------------------------                         
    # 連接 MySQL
    conn = ( pymysql.connect(host = '114.34.138.146',
                             port = 3306,
                             user='guest',
                             password='123',
                             database='origin_data',  
                             charset="utf8") )     
                             
    cursor = conn.cursor()                         
    cursor.execute('select * from ' + data_name)
    # 抓所有的 data
    sql_data = cursor.fetchall()
    # close connect
    conn.close()
    #---------------------------------------------------------------                         
    # 從 MYSQL 抓下來的型態為 tuple, 不利於分析, 
    # 一般是使用 dataframe, 因此進行轉換
    # type of data is tuple, we can change to dataframe
    
    title = []
    date = []
    author = []
    ip = []
    push = []
    boo = []
    arrow = []
    article_url = []
    clean_article = []
    origin_article = []
    for d in sql_data:
        title.append( d[0] )
        date.append(  d[1] )
        author.append(  d[2] )
        ip.append(  d[3] )
        push.append(  d[4] )
        boo.append(  d[5] )
        arrow.append(  d[6] )
        article_url.append(  d[7] )
        clean_article.append(  d[8] )
        origin_article.append(  d[9] )
        
        
    data = {
        'title' : title,
        'date' : date,
        'author' : author,
        'ip' : ip,
        'push' : push,
        'boo' : boo,
        'arrow' : arrow,
        'article_url' : article_url,
        'clean_article' : clean_article,
        'origin_article' : origin_article}
    
    data = pd.DataFrame(data)
    # 轉換成功
    return data
#--------------------------------------------------------------- 
#---------------------------------------------------------
# 如想取得其他 data，可更改 data_name，data_name 可以參考
# https://github.com/f496328mm/Crawler_and_Share 下的 SQL name
# 傳輸 data 可能會花一段時間(一分內) ，麻煩請稍等
job_data = input_data_from_SQL(data_name = 'ptt_job')



                         
                         
                         
