
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

    conn = ( pymysql.connect(host = host,# SQL IP
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
def build_date_time(date):#i=1
    x = date
    try:
        if( re.search('編輯',x) ):
            hour_min = re.findall(r'[[0-9]*:[0-9]*:[0-9]*]*',x)[0]
            day_month_year = re.findall(r'[[0-9]*/[0-9]*/[0-9]*]*',x)[0]
            tem = day_month_year + ' ' + hour_min
            
            date = dtime.strptime(tem,'%m/%d/%Y %H:%M:%S')# tem = '07/29/2017 12:37:01'
        else:
            regex = re.compile('(?P<week>[a-zA-Z]+)\s+(?P<month>[a-zA-Z]+)')
            m = regex.search(x)
            month = m.group('month')
            year = re.findall(r'[0-9]{4,4}',x)[0]
            day = re.findall(r'[ ]{1,2}[0-9]*[ ]{1,2}',x)[0]
    
            day = day.replace(' ','')
            hour_min = re.findall(r'[[0-9]*:[0-9]*:[0-9]*]*',x)[0]
            tem = year+'-'+month+'-'+day + ' ' + hour_min
            #return tem
            date = dtime.strptime(tem,'%Y-%b-%d %H:%M:%S')
    except:
        print('error')
        date = datetime.datetime(1900,1,1,1,1,1)
    
    return date
# 爬 ptt 文章
    
def find_ip(author_ip,origin_article):# i=172
    
    author_ip = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',author_ip)
    if len(author_ip) == 1:
        author_ip = author_ip[0]
        return author_ip
    #-------------------------------------------

    author_ip = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',origin_article)
    if len(author_ip) == 1:
        author_ip = author_ip[0]
        return author_ip
    return ''    
    

def craw_ptt_data_fun(article_url,
                      temp,
                      i,
                      index_url,
                      sql_name,
                      max_date_time,
                      bo,
                      ptt_class_name,
                      bool_18,
                      cursor):
    # bo = 'his' bo = 'new'
    # sql_name = 'ptt_Soft_Job'

    
    if( bool_18 == 1 ):
    #-----------------------------------------------------
        index_name = 'https://www.ptt.cc'
        rs = requests.session()
        payload = {
        'from':'/bbs/'+ptt_class_name+'/index.html',
        'yes':'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18',verify = False, data = payload)
        
        res2 = rs.get(article_url,verify = True)  # 擷取該網站 原始碼         
        soup2 = BeautifulSoup(res2.text, "lxml")# beautiful 漂亮的呈現原始碼
        #temp = soup.find_all("",{'class':'r-ent'})
    #---------------------------------------------------------------------------
    # article_url = 'https://www.ptt.cc/bbs/Soft_Job/M.1503652456.A.526.html'
    else:
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
    date = build_date_time(date)
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
        clean_article = clean_article.replace('█','')
    elif( re.search('▌',clean_article) ):
        clean_article = clean_article.replace('▌','')
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
    # data clean            
            
    author_ip = find_ip(author_ip,origin_article)
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
    
def ptt_18(ptt_class_name,i):
    index_name = 'https://www.ptt.cc'
    index_class = '/bbs/' + ptt_class_name + '/index'
    rs = requests.session()
    
    payload = {
    'from':'/bbs/'+ptt_class_name+'/index.html',
    'yes':'yes'
    }
    index_url = index_name + index_class +str(i)+'.html'
    res = rs.post('https://www.ptt.cc/ask/over18',verify = False, data = payload)
    
    res = rs.get(index_url,verify = False)                
    soup = BeautifulSoup(res.text, "lxml")
    temp = soup.find_all("",{'class':'r-ent'})
    
    return temp
#---------------------------------------------------------------------------------    
# 抓 ptt 目錄, 由目錄去抓 ptt 文章網址, 利用網址進行 craw_ptt_data_fun , 抓取data
# 注意, 八掛版會遇到 18 禁, 需要進行其他處理, 大部分的板沒有 18 禁
def main_craw_ptt(i,ptt_class_name,sql_name,bo):
    # ptt_class_name = 'Gossiping'
    # sql_name = 'ptt_Gossiping'
    conn = ( pymysql.connect(host = host,# SQL IP
                             port = 3306,
                             user = user,# 帳號
                             password = password,# 密碼
                             database = database,  # 資料庫名稱
                             charset="utf8") )#  編碼     
    cursor = conn.cursor() #创建游标
    
    index_name = 'https://www.ptt.cc'
    index_class = '/bbs/' + ptt_class_name + '/index'
    # i=1, i=2845
    
    index_url = index_name + index_class +str(i)+'.html' # 抓第 i 個目錄
    #res = requests.get(index_url,verify = False)               
    res = requests.get(index_url,verify = True) # 讀取 html 原始碼
    soup = BeautifulSoup(res.text, "lxml")# html轉為漂亮   幫助觀察原始碼     
    if( re.search('進入之看板內容需滿十八歲方可瀏覽',str(soup)) ):
        temp = ptt_18(ptt_class_name,i)
        bool_18 = 1
    else:
        temp = soup.find_all("",{'class':'r-ent'})
        bool_18 = 0
    #-----------------------------------------------------
    
    for i in range( len( temp ) ): # i=0 len( temp )
        #print(i)
        temp2 = temp[i].find('a')
        if( str( temp2 ) == 'None' ):# 如果該網址是空   則 return error, 因為有可能對方已刪文
            print('error')
        elif( str( temp2 ) != 'None' ):# 非空才執行爬蟲
            
            article_url = temp[i].find('a')['href']# 抓文章網址
            article_url = index_name+article_url# 與 index 合併
            title = temp[i].find('a').get_text()# 抓 title
            #print(i,title)
            # article_url = 'https://www.ptt.cc/bbs/Soft_Job/M.1503652456.A.526.html'
            response = requests.session().get( article_url )#response, 網站狀態, 200代表成功
            if( response.status_code == 404 ):
                print(404)
            elif( re.search('公告',title) ):# 不抓公告
                print('[公告]')
            elif( response.status_code == 200  ):# 200才抓文章
                if(bo == 'new'):# 更新data, 每日抓新文章, 
                    # max date time 比對, 小於sql中的 max time, 代表是舊文章, 不抓
                    date_time = catch_ptt_history_date_time(ptt_class_name,sql_name)
                    max_date_time = date_time
                elif(bo == 'his'):# 抓歷史文章, 由於文章數過多, 需要慢慢抓
                    max_date_time = 0#bo = 'his'
                tem = craw_ptt_data_fun(article_url,
                                        temp,
                                        i,
                                        index_url,
                                        sql_name,
                                        max_date_time,
                                        bo,
                                        ptt_class_name,
                                        bool_18,
                                        cursor)
        else:
            print('other')
            
    conn.commit()
    cursor.close()# 關閉
    conn.close()  # 關閉
    
# 修正爬取 data, 由於可能在抓到目錄 index=100 時, 第5篇時出現error, 則由第6篇重新抓取
def fix_data(i,ptt_class_name,sql_name,bo,j):
    #ptt_class_name = 'Soft_Job'
    index_name = 'http://www.ptt.cc'
    index_class = '/bbs/' + ptt_class_name + '/index'
    # i=2845, i=18
    
    index_url = index_name + index_class +str(i)+'.html'
    #res = requests.get(index_url,verify = False)     
    # index_url = 'http://www.ruten.com.tw/'    
    res = requests.get(index_url,verify = True)
    soup = BeautifulSoup(res.text, "lxml")
    
    temp = soup.find_all("",{'class':'r-ent'})
    
    for i in range( j,len( temp ) ): # i=10 len( temp )
        #print(i)
        temp2 = temp[i].find('a')
        if( str( temp2 ) == 'None' ):
            print('error')
        elif( str( temp2 ) != 'None' ):
            #print(i)
            article_url = temp[i].find('a')['href']
            article_url = index_name+article_url
            title = temp[i].find('a').get_text()
            #print(i,title)
            # article_url = 'https://www.ptt.cc/bbs/Soft_Job/M.1503652456.A.526.html'
            response = requests.session().get( article_url )
            if( response.status_code == 404 ):
                print(404)
            elif( response.status_code == 200  ):
                if(bo == 'new'):
                    date_time = catch_ptt_history_date_time(ptt_class_name,sql_name)
                    max_date_time = max(date_time)
                elif(bo == 'his'):
                    max_date_time = 0
                tem = craw_ptt_data_fun(article_url,temp,i,index_url,sql_name,max_date_time,bo,ptt_class_name,0)
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
    conn = ( pymysql.connect(host = '114.34.138.146',
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
    index = index.replace('https://www.ptt.cc/bbs/'+ ptt_class_name +'/index','')
    index = index.replace('.html','')
    index = int(index)

    cursor.close()
    conn.close()    
    
    return index
#---------------------------------------------------------------------------------  
#---------------------------------------------------------------------------------  
# 抓 SQL 中 data 的時間, 新data時間不能小於 SQL 中 max data time
def catch_ptt_history_date_time(ptt_class_name,sql_name):
    conn = ( pymysql.connect(host = host,
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
    
    if( re.search('進入之看板內容需滿十八歲方可瀏覽',str(soup3)) ):
        index_name = 'https://www.ptt.cc'
        index_class = '/bbs/' + ptt_class_name + '/index'
        rs = requests.session()
        
        payload = {
        'from':'/bbs/'+ptt_class_name+'/index.html',
        'yes':'yes'
        }
        index_url = index_name + index_class +'.html'
        res = rs.post('https://www.ptt.cc/ask/over18',verify = False, data = payload)
        
        res = rs.get(index_url,verify = False)                
        soup3 = BeautifulSoup(res.text, "lxml")
    else:
        123

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

    #amount = 2
    index = catch_ptt_max_index(ptt_class_name,sql_name)
    min_index = (index)
         
    for i in range(min_index+1,min_index+amount,1):# i =3452
        print(i,'================================================')
        main_craw_ptt(i,ptt_class_name,sql_name,bo='his') 
#---------------------------------------------------------------------------------  
# 建立基本的 data, 有基礎才能抓 history data 與 更新 data
def create_based_ptt_data(ptt_class_name,line):
    #ptt_class_name = 'e_shopping'
    #line = 1
    sql_name = ptt_class_name
    if(line==1):
        sql_name = sql_name.replace('_','-')
    for i in range(1,2,1):
        print(i,'================================================')
        main_craw_ptt(i,sql_name,ptt_class_name,bo='his')    
        
#------------------------------------------------------------------------
# 建立新的 ptt dataset, 格式基本上是用 text, 
# 由於 article 可能過長, clean_article & origin_article 使用 median text, 長一點的型態
def create_ptt_dataset(dataset_name,line):  
    #dataset_name = 'ptt_Soft_Job'       
    sql_string = ( 'create table ' + dataset_name + '( title text(100), date text(100),'+
    ' author text(30), author_ip text(100),'+
    ' push_amount int(10), boo_amount int(10), arrow_amount int(10),' + 
    ' article_url text(100), clean_article text(1000000),origin_article text(1000000),'+
    ' index_url text(100))' )
    
    creat_sql_file(sql_string,dataset_name)      
    create_based_ptt_data(dataset_name,line)# 建立基礎的 data
#------------------------------------------------------------------------
def compare_index(ptt_class_name,sql_name):
    # ptt_class_name = 'Gossiping'
    # sql_name = 'ptt_Gossiping'
    # n = 150

    our_index = catch_ptt_max_index(ptt_class_name,sql_name)
    ptt_index = craw_last_index(ptt_class_name)
    
    if( abs(our_index - ptt_index) < 1):

        conn = ( pymysql.connect(host = host,# SQL IP
                                 port = 3306,
                                 user = user,# 帳號
                                 password = password,# 密碼
                                 database = 'python',  # 資料庫名稱
                                 charset="utf8") )#  編碼     
        cursor = conn.cursor() #创建游标
        #---------------------------------------------------------------------------        
        ( cursor.execute('insert into '+ 'new(ptt_name,bool)'  +
                         ' values(%s,%s)', 
                  (sql_name,'end') ) )
                              
        conn.commit()
        #以下两步把游标与数据库连接都关闭，这也是必须的！
        cursor.close()# 關閉
        conn.close()  # 關閉

#------------------------------------------------------------------------        
#------------------------------------------------------------------------  
def catch_new_ptt_bo(ptt_class_name,sql_name):
    
    conn = ( pymysql.connect(host = host,
                             port = 3306,
                             user = user,
                             password = password,
                             database='python',  
                             charset="utf8") )     
    cursor = conn.cursor()                         
    cursor.execute('select * from ' + 'new')
    # 抓所有的 data
    data = cursor.fetchall()
    #ptt_name = []
    #bo = []
    new_bo = []
    for d in data:
        #print(d[0])
        if( d[0] == sql_name ):
            new_bo = d[1]

    # close connect
    conn.close()
    
    return new_bo
#------------------------------------------------------------------------     
def print_ptt_index_csv(ptt_class_name,sql_name):
    test=[]
    test.append(1)
    test = {'test':test}
    test = pd.DataFrame(test)
    os.chdir('/home/linsam/text_mining')
    index = catch_ptt_max_index(ptt_class_name,sql_name)
    test.to_csv(ptt_class_name+'_' + str(index) + '.csv')        
        
#------------------------------------------------------------------------     
def save_craw_process(ptt_class_name,sql_name):
    #test=[]
    #test.append(1)
    #test = {'test':test}
    #test = pd.DataFrame(test)
    #os.chdir('/home/linsam/text_mining')
    index = catch_ptt_max_index(ptt_class_name,sql_name)
    #test.to_csv(ptt_class_name+'_' + str(index) + '.csv')   
    
    conn = ( pymysql.connect(host = host,# SQL IP
                             port = 3306,
                             user = user,# 帳號
                             password = password,# 密碼
                             database = 'python',  # 資料庫名稱
                             charset="utf8") )#  編碼     
    cursor = conn.cursor() #创建游标
    tem = str( datetime.datetime.now() )
    time = re.split('\.',tem)[0]
    #---------------------------------------------------------------------------        
    ( cursor.execute('insert into '+ 'process(ptt_name,page_index,time)'  +
                     ' values(%s,%s,%s)', 
              (ptt_class_name,index,time) ) )
                          
    conn.commit()
    #以下两步把游标与数据库连接都关闭，这也是必须的！
    cursor.close()# 關閉
    conn.close()  # 關閉
    
    
#------------------------------------------------------------------------
def auto_change_ptt_class(ptt_class_name,sql_name):#n=3


    tem = catch_new_ptt_bo(ptt_class_name,sql_name)
    if(tem == 'end'):
        return 1
        
    compare_index(ptt_class_name,sql_name)
    # bo = 0 means craw ptt article doesn't end
    #s = datetime.datetime.now()
    auto_craw_history_ptt_data(60,ptt_class_name,sql_name)
    #t = datetime.datetime.now()-s
    #print(t)# 50s
    save_craw_process(ptt_class_name,sql_name)
    #print_ptt_index_csv(ptt_class_name,sql_name)
        
    return 0
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------    
# main         
host = '114.34.138.146'
user='text_mining'# 帳號
password='610411102'# 密碼
#database='guest_dataset'  # 資料庫名稱
database='ptt_data1.0'  # 資料庫名稱
#ptt_class_name = 'PC_Shopping' # 測試, 爬取 PTT 料理板
#sql_name = 'ptt_PC_Shopping'         # 先創建自己的 data table, 測試用
#------------------------------------------------------------------------
#  create dataset

# 自動爬取, 
# ubuntu 可用 crontab -e 設定
# 例如 0 0-23 * * * python3 /xxx/xxx/xxx/auto_craw_his_ptt_data.py
# 以上 ubuntu 排程, 會每小時爬取一次 data, 我預設一次爬取 40 個目錄, 時間大約在 40~50 minute
# 一個目錄約有 15 篇文章, 因此一小時約可爬取 600 篇文章, 一天約 14000 筆


ptt_class_name_set = ['Food',
                      'car',# 3824
                      'Sad',# 1307
                      'Self-Healing',# 680
                      'SorryPub',# 918
                      'SayLove',# 720
                      'love',# 978
                      'Lonely',# 1023
                      'Lucky',# 967
                      'Marginalman',# 5887 
                      'Broken-heart', # 1167
                      'couple',
                      'Japan_Travel',
                      'e-shopping',
                      'Finance',
                      'NBA',
                      'Baseball',
                      'StupidClown',
                      'Aquarius',
                      'Aries',
                      'Cancer',
                      'Bread',
                      'chocolate',
                      'Coffee'
                      ]
sql_name_set = ['Food',
                'car',# 3824
                'Sad',# 1307
                'Self_Healing',# 680
                'SorryPub',# 918
                'SayLove',# 720
                'love',# 978
                'Lonely',# 1023
                'Lucky',# 967
                'Marginalman',# 5887 
                'Broken_heart', # 1167
                'couple',
                'Japan_Travel',
                'e_shopping',
                'Finance',
                'NBA',
                'Baseball',
                'StupidClown',
                'Aquarius',
                'Aries',
                'Cancer',
                'Bread',
                'chocolate',
                'Coffee'
                ]
                
'''     
create_ptt_dataset('Bread',0)     
create_ptt_dataset('chocolate',0)        
create_ptt_dataset('Coffee',0)        
create_ptt_dataset('cookclud',0)  
'''                      
#Bread
#chocolate
#coffee
#cookclud

while(1):
    while_bool = 1
    i=0
    try:
        while(while_bool == 1):
            ptt_class_name = ptt_class_name_set[i]
            sql_name = sql_name_set[i]
            print('i=' + str(i)+'  '+str(ptt_class_name))
            # catch_new_ptt_bo(ptt_class_name,sql_name)
            bo = auto_change_ptt_class(ptt_class_name,sql_name) 
            i=i+1
            if(bo==0 or i>=len(ptt_class_name_set)): 
                print('break')
                while_bool = 0
    except:
        123        



# windows 比較可能出現 connect 錯誤的問題, 因此使用以下 code 進行修補
# fix_data(381,ptt_class_name,sql_name,bo = 'his',j=4)
# 如果中途掛掉, 例如在目錄(index) 100 中的第 5 篇文章出現 error, 
# 就從第 6 篇開始抓, 不然會遺漏
# fix_data(2354,ptt_class_name,sql_name,bo = 'his',j=19)









