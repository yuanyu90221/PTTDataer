
import requests
import sys,os
path = os.listdir('/home')[0]
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import pymysql
from datetime import datetime as dtime
import boto3
from boto3.dynamodb.conditions import Key
sys.path.append('/home/'+ path +'/github')
from PTTOpenData import LoadDataFromAWS

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_aws_table(sql_string,dataset_name):

    print('create table')
    dynamodb.create_table(
            #TableName = ptt_table[i],
            TableName = 'PTT',
            KeySchema = [
                    {
                            'AttributeName': 'ptt_name',
                            'KeyType': 'HASH'  #Partition key
                            },
                            {
                                    'AttributeName': 'date',
                                    'KeyType': 'RANGE'  #Sort key
                                    }
                            ],
            AttributeDefinitions=[
                    {
                            'AttributeName': 'ptt_name',
                            'AttributeType': 'S'
                            },
                            {
                                    'AttributeName': 'date',
                                    'AttributeType': 'S'
                                    },
                                    ],
        ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
        )

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
    
    #author_ip = data['author_ip'][i]
    author_ip = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',author_ip)
    if len(author_ip) == 1:
        author_ip = author_ip[0]
        return author_ip
    #-------------------------------------------
    #author_ip = origin_article
    
    author_ip = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',origin_article)
    if len(author_ip) == 1:
        author_ip = author_ip[0]
        return author_ip
    return ''   
    
def craw_ptt_data_fun(article_url,temp,i,index_url,sql_name,max_date_time,bo,ptt_class_name,bool_18):
    # bo = 'his' bo = 'new'
    # sql_name = 'ptt_Soft_Job'
    #------------------------------------------------------
    def getresponse(origin_article):
        tem = origin_article.split('\n')
        response = ''
        for res in tem:# res = tem[1]
            #re.search('[推,噓,→]*+[ ]*+[a-zA-Z0-9]*+[ ]*+[:]',res)
            tem2 = re.search('[推,噓,→, ]+[a-zA-Z0-9]+[:, ]+',res)
            if str(type(tem2)) == "<class 'NoneType'>":
                123
            elif '推' in tem2.group(0) or '噓' in tem2.group(0) or '→' in tem2.group(0) :
                #response.append(res)
                response = response + '\n' + res
            try:
                ip = re.search('[[0-9]+.[0-9]+.[0-9]+.[0-9]+]*',response).group(0)
                response = response.replace(ip,'')
            except:
                123
        #response.split('\n')
        response = pymysql.escape_string(response)
        return response
    #------------------------------------------------------
    def get_clean_article(article):
        split_text = ['Sent from ','※ 發信站']
        
        for te in split_text:
            article = article.split(te)[0]  

        return article
    
    def clean(cleanarticle,date):
        #
        tdate = str( date )
        year = tdate[:4]
        tdate = re.search(r"[[0-9]*:[0-9]*:[0-9]*]*",tdate).group(0)
        tdate = tdate + ' ' + year
        
        tem = cleanarticle.split(tdate)
        if len(tem) > 1: 
            tem2 = tem[1]
        else:
            tem2 = tem[0]
        # del 'Sent from ','※ 發信站'
        tem = tem2.split('\n')
        article = ''
        for te in tem:
            if ': ' not in te:
                if '※ 引述' not in te:
                    if len(te) >1:
                        #print(te)
                        article = article + '\n' + te
                        
        article = get_clean_article(article)  
        article = article.replace('"',"'")
        article = pymysql.escape_string(article)
        return article      
    #------------------------------------------------------        
    if( bool_18 == 1 ):
    #-----------------------------------------------------
        rs = requests.session()
        #res = rs.post('https://www.ptt.cc/ask/over18',verify = False, data = payload)
        
        res2 = rs.get(article_url,verify = True)  # 擷取該網站 原始碼         
        soup2 = BeautifulSoup(res2.text, "lxml")# beautiful 漂亮的呈現原始碼
        #temp = soup.find_all("",{'class':'r-ent'})
    #---------------------------------------------------------------------------
    # article_url = 'https://www.ptt.cc/bbs/NBA/M.1526380904.A.17A.html'
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
    clean_article = clean(clean_article,date)
    # 原始文章   
    origin_article = str( soup2.find(id="main-container").text )
    # author_ip
    # 抓發文者ip
    author_ip = soup2.find(string = re.compile(r"[[0-9]*\.[0-9]*\.[0-9]*\.[0-9]]*"))
    author_ip = find_ip(author_ip,origin_article)
    if( str( type(author_ip) ) == "<class 'NoneType'>" ):
        #return 0
        author_ip = ''
    else:
        author_ip = author_ip.replace('\n','')
    
    response = getresponse(origin_article)
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
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('PTT')
    date = str(date).replace(' ','T') + '+08:00'
    #---------------------------------------------------------------------------  
    table.put_item(
            Item={
                    'ptt_name' : ptt_class_name,
                    'title' : title,
                    'date' : date,
                    'author': author,
                    'author_ip': author_ip,
                    'push_amount': push_amount,
                    'boo_amount': boo_amount,
                    'arrow_amount': arrow_amount,
                    'article_url': article_url,
                    'clean_article': clean_article,
                    'response': response,
                    }
                    )
    
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
    # ptt_class_name = 'job'
    # sql_name = 'job'
    index_name = 'https://www.ptt.cc'
    index_class = '/bbs/' + ptt_class_name + '/index'

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
    
    for i in range( len( temp ) ): # i=3 len( temp )
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
                    max_date_time = catch_ptt_history_date_time(ptt_class_name)
                elif(bo == 'his'):# 抓歷史文章, 由於文章數過多, 需要慢慢抓
                    max_date_time = 0#bo = 'his'
                craw_ptt_data_fun(article_url,temp,i,index_url,
                                  sql_name,max_date_time,bo,
                                  ptt_class_name,bool_18)
        else:
            print('other')

#------------------------------------------------------------------------------------------
def date_to_numeric(date):
    #date = '07/06/2017 07:46:39'
    #date = 'Su Sep 18 10:31:26 201'
    #date = '※ 轉錄者: smallwo (71.212.4.14), 11/30/2016 14:40:18'
    # date = data[1]
    try:
        date = dtime.strptime(date,'%Y-%m-%d %H:%M:%S')
        value = ( date - dtime(1970,1,1) ).total_seconds()
    except:
        try:
            temp = re.split(' ',date)
            if( len( temp[len(temp)-1] )!=4 or date == 'None' ):
                print(0)
                return 0      
            if( re.search('※',date) ):
                #print(date)
                date = str( re.findall( r"[0-9]*/[0-9]*/[0-9]* [[0-9]*:[0-9]*:[0-9]*]*" , date ) )        
                date = date.replace("['",'')
                date = date.replace("']",'')
                date = dtime.strptime(date,'%m/%d/%Y %H:%M:%S')
            else:
                date = date.replace('  ',' ')
             
                regex = re.compile('(?P<week>[a-zA-Z]+)\s+(?P<month>[a-zA-Z]+)')
                m = regex.search(date)
                month = m.group('month')
                #week  = m.group('week')
                date = str( re.findall( r" [0-9]* [[0-9]*:[0-9]*:[0-9]* [0-9]*]*" , date ) )
                date = date.replace("['",'')
                date = date.replace("']",'')
                date = month + date
                if( month == 'July' ):
                    date = dtime.strptime(date,'%B %d %H:%M:%S %Y')
                else:
                    date = dtime.strptime(date,'%b %d %H:%M:%S %Y')
            
            # change to numeric by seconds
            value = ( date - dtime(1970,1,1) ).total_seconds()
        except:
            #print(1)
            date = dtime.strptime(date,'%Y-%m-%d %H:%M:%S')
            value = ( date - dtime(1970,1,1) ).total_seconds()
    return value


def catch_ptt_history_date_time(ptt_class_name):

    table = dynamodb.Table('PTT')# ptt_class_name = 'AdvEduUK'
    query = Key('ptt_name').eq(ptt_class_name)
    
    response = table.query(
        KeyConditionExpression = query,
        Limit = 1,
        ScanIndexForward = False
        )
    data = pd.DataFrame.from_dict(response['Items']) # len(data)   
    date_time = data['date'][0].split('+')[0]
    date_time = datetime.datetime.strptime(date_time,'%Y-%m-%dT%H:%M:%S')
         
    date_time  = ( date_time- dtime(1970,1,1) ).total_seconds()   
 
    
    return date_time            

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
    
def auto_craw_new_ptt_data(amount,ptt_class_name):    
    # ptt_class_name = 'job'
    # sql_name = 'job'
    # amount = 3
    tem = catch_new_ptt_bo(ptt_class_name)
    if(tem != 'end'):
        return 0
    bo = 1
    while( bo ):
        try:
            last_index = craw_last_index(ptt_class_name)  
            bo=0
        except:
            print('last index error')
        
    #his_index = catch_ptt_max_index(ptt_class_name,sql_name)
    #max_index = (his_index)
    #max_date_time = max(date_time)
    #data = pd.DataFrame()
    for i in range(last_index-amount,last_index+1,1):# i = 147
        k=0
        print(i,'================================================')
        # connect wrong
        while(k==0):
            try:
                main_craw_ptt(i,ptt_class_name,bo='new') 
                k=1
                print('ok')
            except:
                123
    save_new_craw_process(ptt_class_name,i)

#------------------------------------------------------------------------
def save_new_craw_process(ptt_class_name,index):
    
    table = dynamodb.Table('CrawlerLog')
    tem = str( datetime.datetime.now() )
    time = re.split('\.',tem)[0].replace(' ','T') + '+08:00'
    table.put_item(
            Item={
                    'name' : 'PTT_' + ptt_class_name,
                    #'ptt_name' : 'PTT_' + ptt_class_name,
                    'CrawlerDate' : time,
                    'index' : index
                    }
                    )

#------------------------------------------------------------------------
def catch_new_ptt_bo(ptt_class_name):
    
    data = LoadDataFromAWS.main(dynamodb_name = 'ptt_history_ok',
                               pkey_name = 'bool', 
                               pkey_value = 'end')
    new_bo = []
    if ptt_class_name in list( data['ptt_name'] ):
        new_bo = 'end'
    
    return new_bo
#------------------------------------------------------------------------
# main         
#tem = catch_new_ptt_bo('job')
#tem    
#------------------------------------------------------------------------

# craw new data

ptt_class_name_set = ['job','Soft_Job','Tech_Job','Oversea_Job','TaiwanJobs',
                      'part-time','HomeTeach','movie','Stock','Japan_Travel',
                      'WomenTalk','e-shopping','Finance','toberich','prozac',
                      'Lifeismoney','MacShop','HardwareSale','happy','Hate',
                      'car','Food','PC_Shopping','cookclub','MenTalk',
                      'talk','home-sale','Gossiping','MobileComm','BabyMother',
                      'Sad','Self-Healing','SorryPub','SayLove','love',
                      'Lonely','Lucky','Marginalman','Broken-heart','couple',
                      'Boy-Girl','NBA','Baseball','StupidClown','BuyTogether',
                      'creditcard','GetMarry','SportLottery','StupidClown','mobilesales',
                      'Salary','HelpBuy','Wanted','forsale','CarShop',
                      'BabyProducts','DC_SALE','AdvEduUK','studyabroad','EngTalk',
                      'joke','love-vegetal','baking','Aquarius','Aries',
                      'Cancer','Capricornus','Gemini','Libra','Leo',
                      'Pisces','Sagittarius','Scorpio','Taurus','Zastrology',
                      'Virgo','MakeUp','marvel','Kaohsiung','Tainan','TaichungBun',
                      'Hsinchu','biker','Aviation','give','Loan','HatePolitics',
                      'CATCH','Diary','DistantLove','Dreamland','EuropeTravel',
                      'Hiking','hotspring','Ind-travel','isLandTravel','Korea_Travel',
                      'Tour-Agency','VISA','travelbooks','travel','WorkanTravel',
                      'IELTS','JapanStudy','TOEFL_iBT','Anti-Cancer','Bread',
                      'chocolate','Coffee','sex'
                      ]

amount_set = [3,3,3,3,3,
              8,3,5,5,8,
              10,3,3,3,3,
              3,13,10,3,20,
              5,5,3,3,3,
              3,3,200,5,8,
              3,3,3,3,3,
              3,3,3,3,3,
              3,5,15,3,8,
              3,3,3,3,12,
              3,23,40,40,3,
              13,5,3,3,3,
              5,3,3,3,3,
              3,3,3,3,3,
              3,3,3,3,3,
              3,3,3,5,10,
              10,5,3,3,3,
              8,3,5,3,3,
              3,3,3,3,3,
              3,3,3,3,3,
              3,3,3,3,3,
              3,3,3,3,3,
              3,3,3,3,3,
              5
              ]

if __name__ == '__main__':
    
    for i in range(len(ptt_class_name_set)):# i = 0
        #print(i)
        ptt_class_name = ptt_class_name_set[i]
        amount = amount_set[i]
        auto_craw_new_ptt_data(amount,ptt_class_name)#craw data~~~
        #time.sleep(60*3)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    table = dynamodb.Table('CrawlerLog')
    tem = str( datetime.datetime.now() )
    time = re.split('\.',tem)[0].replace(' ','T') + '+08:00'
    table.put_item(
            Item={
                    'name' : 'PTT',
                    'CrawlerDate' : time,
                    'index' : today
                    }
                    )
    
    
    
    