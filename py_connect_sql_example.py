# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 01:22:35 2017
@author: linsam
"""

import pymysql
import pandas as pd
import re
import datetime

def input_data_from_SQL(data_name = 'ptt_job'):
    #---------------------------------------------------------------                         
    # 在以上指令後, 你已經會上傳 data, 那要如何下載 data 呢?
    # you can input data, then how take data from MYSQL?
    conn = ( pymysql.connect(host = 'linsam.servehttp.com',
                             port = 3306,
                             user='guest',
                             password='123',
                             database='origin_data',  
                             charset="utf8") )     
                             
    cursor = conn.cursor()                         
    # input data from article_date
    # ptt_happy
    # ptt_prozac
    # ptt_Hate
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

job_data = input_data_from_SQL(data_name = 'ptt_job')



                         
                         
                         