
import requests
import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import datetime
import pymysql
from datetime import datetime as dtime
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
# 建立 SQL 檔案
def creat_sql_file(sql_string,dataset_name):

    conn = ( pymysql.connect(host = 'linsam.servehttp.com',# SQL IP
                             port = 3306,
                             user = user,# 帳號
                             password = password,# 密碼
                             database = database,  # 資料庫名稱
                             charset="utf8") )   #  編碼           
    c=conn.cursor()
    c.execute( sql_string )# 建立新的 SQL file
    c.execute('ALTER TABLE `'+dataset_name+'` ADD id BIGINT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY;')
    c.close() # 關閉與 SQL 的連接
    conn.close()# 關閉與 SQL 的連接
#---------------------------------------------------------------------------------    
# 爬 ptt 文章
def craw_ptt_data_fun(article_url,temp,i,index_url,sql_name,max_date_time,bo="his"):
    # bo = 'his' bo = 'new'
    # sql_name = 'ptt_Soft_Job'
    conn = ( pymysql.connect(host = 'linsam.servehttp.com',# SQL IP
                             port = 3306,
                             user = user,# 帳號
                             password = password,# 密碼
                             database = database,  # 資料庫名稱
                             charset="utf8") )#  編碼     
    cursor = conn.cursor() #创建游标
    #---------------------------------------------------------------------------
    # article_url = 'https://www.ptt.cc/bbs/Soft_Job/M.1503652456.A.526.html'
    res2 = requests.get(article_url,verify = True)  # 擷取該網站 原始碼         
    soup2 = BeautifulSoup(res2.text, "lxml")# beautiful 漂亮的呈現原始碼
    # author                
    author = temp[i].find("",{'class':'author'}).get_text() # 抓出作者
    # date
    # 抓出日期, r" [[0-9]*:[0-9]*:[0-9]]*" 為正規化擷取文字
    date = str( soup2.find(string = re.compile(r" [[0-9]*:[0-9]*:[0-9]]*")) )
    # 如果以上日期小於資料庫中最大日期, 代表該data已經抓過, 則跳過不抓同樣的data
    if(bo == 'new'):
        date_to_seconds = date_to_numeric( date ) 
        if( date_to_seconds <= max_date_time  ):
            print('data already input')
            return 'data already input'
    # title
    title = temp[i].find('a').get_text()# 抓文章 title
    print(i,title)        
    # author_ip
    # 抓發文者ip
    author_ip = soup2.find(string = re.compile(r"[[0-9]*\.[0-9]*\.[0-9]*\.[0-9]]*"))
    if( str( type(author_ip) ) == "<class 'NoneType'>" ):
        return 0
    else:
        author_ip = author_ip.replace('\n','')
    # article  
    # 抓文章   先進行暫存
    article_temp = soup2.find(id="main-container")
    if( str( type(article_temp) ) == "<class 'NoneType'>" ):
        return 0
    else:
        article_temp = str( article_temp.text ) 
    x = soup2.find_all('',{'class' : 'f2'})
    if(len(x)==0):
        return 0
    else :
        x = str( x[len(x)-1].text )[0:5]
    # 稍微清理過的 文章    
    clean_article = re.split(x,article_temp)[0]
    if( re.search('█',clean_article) ):
        clean_article.replace('█','')
        #return 0  
    # 原始文章   
    origin_article = str( soup2.find(id="main-container").text )
    
    # reply           class="push" 
    # 紀錄推文數             
    reply = soup2.find_all('',{'class' : "f1 hl push-tag"})
    #reply = soup2.find_all('',{'class' : "hl push-tag"})
    push_amount = len( soup2.find_all('',{'class' : "hl push-tag"}) )
    boo_amount = 0
    arrow_amount = 0  
    # 紀錄噓文、箭頭數
    for j in range(len(reply)):
        if( reply[j].text == '噓 ' ):
            boo_amount = boo_amount+1
        elif( reply[j].text == '→ ' ):
            arrow_amount = arrow_amount+1
    # 將以上爬到的 data, 存入MySQL
    #---------------------------------------------------------------------------        
    ( cursor.execute('insert into '+ sql_name +
    '(title,date,author,author_ip,push_amount,boo_amount,arrow_amount,article_url,clean_article,origin_article,index_url)' +
                     ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
              (title,
               date,
               author,
               author_ip,
               push_amount,
               boo_amount,
               arrow_amount,
               article_url,
               clean_article,
               origin_article,
               index_url) ) )
                          
    conn.commit()
    #以下两步把游标与数据库连接都关闭，这也是必须的！
    cursor.close()# 關閉
    conn.close()  # 關閉
#---------------------------------------------------------------------------------    
# 抓 ptt 目錄, 由目錄去抓 ptt 文章網址, 利用網址進行 craw_ptt_data_fun , 抓取data
# 注意, 八掛版會遇到 18 禁, 需要進行其他處理, 大部分的板沒有 18 禁
def main_craw_ptt(i,ptt_class_name,sql_name,bo):
    #ptt_class_name = 'Soft_Job'
    index_name = 'http://www.ptt.cc'
    index_class = '/bbs/' + ptt_class_name + '/index'
    # i=4806, i=18
    
    index_url = index_name + index_class +str(i)+'.html' # 抓第 i 個目錄
    #res = requests.get(index_url,verify = False)               
    res = requests.get(index_url,verify = True) # 讀取 html 原始碼
    soup = BeautifulSoup(res.text, "lxml")# html轉為漂亮   幫助觀察原始碼 
    
    temp = soup.find_all("",{'class':'r-ent'})
    
    for i in range( len( temp ) ): # i=0 len( temp )
        #print(i)
        temp2 = temp[i].find('a')
        if( str( temp2 ) == 'None' ):# 如果該網址是空   則 return error, 因為有可能對方已刪文
            print('error')
        elif( str( temp2 ) != 'None' ):# 非空才執行爬蟲
            #print(i)
            article_url = temp[i].find('a')['href']# 抓文章網址
            article_url = index_name+article_url# 與 index 合併
            title = temp[i].find('a').get_text()# 抓 title
            # article_url = 'https://www.ptt.cc/bbs/Soft_Job/M.1503652456.A.526.html'
            response = requests.session().get( article_url )#response, 網站狀態, 200代表成功
            if( response.status_code == 404 ):
                print(404)
            elif( re.search('[公告]',title) ):# 不抓公告
                print('[公告]')
            elif( response.status_code == 200  ):# 200才抓文章
                if(bo == 'new'):# 更新data, 每日抓新文章, 
                    # max date time 比對, 小於sql中的 max time, 代表是舊文章, 不抓
                    date_time = catch_ptt_history_date_time(ptt_class_name,sql_name)
                    max_date_time = date_time
                elif(bo == 'his'):# 抓歷史文章, 由於文章數過多, 需要慢慢抓
                    max_date_time = 0
                tem = craw_ptt_data_fun(article_url,temp,i,index_url,sql_name,max_date_time,bo)
        else:
            print('other')
#---------------------------------------------------------------------------------  
# 修正爬取 data, 由於可能在抓到目錄 index=100 時, 第5篇時出現error, 則由第6篇重新抓取
def fix_data(i,ptt_class_name,sql_name,bo,j):
    #ptt_class_name = 'Soft_Job'
    index_name = 'http://www.ptt.cc'
    index_class = '/bbs/' + ptt_class_name + '/index'
    # i=4806, i=18
    
    index_url = index_name + index_class +str(i)+'.html'
    #res = requests.get(index_url,verify = False)     
    # index_url = 'http://www.ruten.com.tw/'    
    res = requests.get(index_url,verify = True)
    soup = BeautifulSoup(res.text, "lxml")
    
    temp = soup.find_all("",{'class':'r-ent'})
    
    for i in range( j,len( temp ) ): # i=12 len( temp )
        #print(i)
        temp2 = temp[i].find('a')
        if( str( temp2 ) == 'None' ):
            print('error')
        elif( str( temp2 ) != 'None' ):
            #print(i)
            article_url = temp[i].find('a')['href']
            article_url = index_name+article_url
            title = temp[i].find('a').get_text()
            # article_url = 'https://www.ptt.cc/bbs/Soft_Job/M.1503652456.A.526.html'
            response = requests.session().get( article_url )
            if( response.status_code == 404 ):
                print(404)
            elif( re.search('[公告]',title) ):
                print('[公告]')
            elif( response.status_code == 200  ):
                if(bo == 'new'):
                    date_time = catch_ptt_history_date_time(ptt_class_name,sql_name)
                    max_date_time = max(date_time)
                elif(bo == 'his'):
                    max_date_time = 0
                tem = craw_ptt_data_fun(article_url,temp,i,index_url,sql_name,max_date_time,bo)
        else:
            print('other')
#---------------------------------------------------------------------------------              
# 日期轉數字, 用於比較大小
def date_to_numeric(date):
    
    #date = '07/06/2017 07:46:39'
    #date = 'Wed Nov  4 12:04:28 2011'
    #date = '※ 轉錄者: smallwo (71.212.4.14), 11/30/2016 14:40:18'
    temp = re.split(' ',date)
    if( len( temp[len(temp)-1] )!=4 or date == 'None' ):
        return 0
    if( re.search('※',date) ):
        #print(date)
        # r"[0-9]*/[0-9]*/[0-9]* [[0-9]*:[0-9]*:[0-9]*]*" 為正規化擷取文字
        date = str( re.findall( r"[0-9]*/[0-9]*/[0-9]* [[0-9]*:[0-9]*:[0-9]*]*" , date ) )        
        date = date.replace("['",'')
        date = date.replace("']",'')
        date = dtime.strptime(date,'%m/%d/%Y %H:%M:%S')
    else:
        date = date.replace('  ',' ')
        # 正規化 抓取月分與星期
        regex = re.compile('(?P<week>[a-zA-Z]+)\s+(?P<month>[a-zA-Z]+)')
        m = regex.search(date)
        month = m.group('month')
        week  = m.group('week')
        date = str( re.findall( r" [0-9]* [[0-9]*:[0-9]*:[0-9]* [0-9]*]*" , date ) )
        date = date.replace("['",'')
        date = date.replace("']",'')
        date = week + ' '+ month + date
        if( month == 'July' ):# 月份的簡寫, 在July比較特別, 需要額外處理
            # %a 是星期, %B是月份(非縮寫),  %d 是day, %H是小時, %M是分鐘, %S 是秒, %Y是年
            date = dtime.strptime(date,'%a %B %d %H:%M:%S %Y')
        else:# %b 是月份縮寫
            date = dtime.strptime(date,'%a %b %d %H:%M:%S %Y')
    
    # change to numeric by seconds
    value = ( date - dtime(1970,1,1) ).total_seconds()# 所有日期轉成秒, 便於比較
    return value
#---------------------------------------------------------------------------------  
def catch_ptt_max_index(ptt_class_name,sql_name):
    conn = ( pymysql.connect(host = 'linsam.servehttp.com',
                             port = 3306,
                             user = user,
                             password = password,
                             database = database,  
                             charset="utf8") )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `'+ sql_name +'` ORDER BY id DESC LIMIT 1;')
    data = cursor.fetchone()       


    index = data[10]
    index = index.replace('http://www.ptt.cc/bbs/'+ ptt_class_name +'/index','')
    index = index.replace('.html','')
    index = int(index)

    cursor.close()
    conn.close()    
    
    return index
#---------------------------------------------------------------------------------  
#---------------------------------------------------------------------------------  
# 抓 SQL 中 data 的時間, 新data時間不能小於 SQL 中 max data time
def catch_ptt_history_date_time(ptt_class_name,sql_name):
    conn = ( pymysql.connect(host = 'linsam.servehttp.com',
                             port = 3306,
                             user = user,
                             password = password,
                             database = database,  
                             charset="utf8") )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `'+ sql_name +'` ORDER BY id DESC LIMIT 1;')
    data = cursor.fetchone()     
        
    date_time  = date_to_numeric( data[1] )

    cursor.close()
    conn.close()    
    
    return date_time  
#---------------------------------------------------------------------------------            
# 抓最近目錄的 index, index 有上一頁的連結, 由此連結去抓最近的 index
def craw_last_index(ptt_class_name):   
    #ptt_class_name = 'Soft_Job'
    index_url = 'https://www.ptt.cc/bbs/' + ptt_class_name + '/index.html'
    res = requests.get(index_url,verify = True)
    soup3 = BeautifulSoup(res.text, "lxml")   
    
    x = soup3('',{'class':"btn wide"},text = re.compile('上頁'))
    last_index = x[0]['href']
    last_index = last_index.replace('/bbs/' + ptt_class_name + '/index','')
    last_index = int( last_index.replace('.html','') )+1
    
    return last_index
#--------------------------------------------------------------------------------- 
# 使用 ubuntu - crontab-e, 設定排程, 每日自動抓最新 data 
# 由於 PTT 文章過多, 會自動刪除文章, 影響目錄編號, 
# 因此每天更新DATA, 採用抓取 index 前一頁的方式, 去抓去一定量的 data,
# 並比較時間, 如果時間小於
def auto_craw_new_ptt_data(amount,ptt_class_name,sql_name):    
    #ptt_class_name = 'Soft_Job'
    last_index = craw_last_index(ptt_class_name)    
    #his_index = catch_ptt_max_index(ptt_class_name,sql_name)
    #max_index = (his_index)
    #max_date_time = max(date_time)
    
    for i in range(last_index-amount,last_index+1,1):
        print(i,'================================================')
        main_craw_ptt(i,ptt_class_name,sql_name,bo='new')
    
#---------------------------------------------------------------------------------
# 使用 ubuntu - crontab-e, 設定排程, 每小時自動抓歷史 data,
def auto_craw_history_ptt_data(amount,ptt_class_name,sql_name):

    #amount = 10
    index = catch_ptt_max_index(ptt_class_name,sql_name)
    min_index = (index)
         
    for i in range(min_index+1,min_index+amount,1):# i =3452
        print(i,'================================================')
        main_craw_ptt(i,ptt_class_name,sql_name,bo='his') 
#---------------------------------------------------------------------------------  
# 建立基本的 data, 有基礎才能抓 history data 與 更新 data
def create_based_ptt_data(ptt_class_name,sql_name):
         
    for i in range(0,3,1):
        print(i,'================================================')
        main_craw_ptt(i,ptt_class_name,sql_name,bo='his')    
        
#------------------------------------------------------------------------
# 建立新的 ptt dataset, 格式基本上是用 text, 
# 由於 article 可能過長, clean_article & origin_article 使用 median text, 長一點的型態
def create_ptt_dataset(dataset_name):  
    #dataset_name = 'ptt_Soft_Job'       
    sql_string = ( 'create table ' + dataset_name + '( title text(100), date text(100),'+
    ' author text(30), author_ip text(100),'+
    ' push_amount text(10), boo_amount text(10), arrow_amount text(10),' + 
    ' article_url text(100), clean_article text(1000000),origin_article text(1000000),'+
    ' index_url text(100))' )
    
    creat_sql_file(sql_string,dataset_name)         
#------------------------------------------------------------------------
#------------------------------------------------------------------------
# main         
user='guest'# 帳號
password='123'# 密碼
database='guest_dataset'  # 資料庫名稱
#------------------------------------------------------------------------
#  create dataset

ptt_class_name = 'cookclub' # 測試, 爬取 PTT 料理板
sql_name = 'test4'         # 先創建自己的 data table, 測試用

create_ptt_dataset(sql_name)# 建立 data table
create_based_ptt_data(ptt_class_name,sql_name)# 建立基礎的 data

# 自動爬取, 
# ubuntu 可用 crontab -e 設定
# 例如 0 0-23 * * * python3 /xxx/xxx/xxx/auto_craw_his_ptt_data.py
# 以上 ubuntu 排程, 會每小時爬取一次 data, 我預設一次爬取 40 個目錄, 時間大約在 40~50 minute
# 一個目錄約有 15 篇文章, 因此一小時約可爬取 600 篇文章, 一天約 14000 筆
for i in range(20):
    print('i = ',i)
    auto_craw_history_ptt_data(4,ptt_class_name,sql_name)
    time.sleep(60*10)# 休息, 爬蟲可以看成 Docs 攻擊, 我選擇休息一段時間的做法
    
# 以下記錄目前爬取位置, 由於 ubuntu 進行排程, 無法得知目前狀況, 
# 因此採取建立文件的做法, 文件命名為 sql_name + index , 可以得知目前 sql_name 和 index
test=[]
test.append(1)
test = {'test':test}
test = pd.DataFrame(test)
os.chdir('d:/text_mining/')
index = catch_ptt_max_index(ptt_class_name,sql_name)
test.to_csv(sql_name + index + '.csv')


# windows 比較可能出現 connect 錯誤的問題, 因此使用以下 code 進行修補
# fix_data(381,ptt_class_name,sql_name,bo = 'his',j=4)
# 如果中途掛掉, 例如在目錄(index) 100 中的第 5 篇文章出現 error, 
# 就從第 6 篇開始抓, 不然會遺漏
# fix_data(3968,ptt_class_name,sql_name,bo = 'his',j=6)




