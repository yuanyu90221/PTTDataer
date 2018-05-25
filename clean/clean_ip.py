

import pymysql
import pandas as pd
import re
import numpy as np

host = '114.34.138.146'
user = 'root'
password = 'e110856234'

#--------------------------------------------------------

def execute_sql2(host,user,password,database,sql_text):
    
    conn = ( pymysql.connect(host = host,# SQL IP
                     port = 3306,
                     user = user,# 帳號
                     password = password,# 密碼
                     database = database,  # 資料庫名稱
                     charset="utf8") )   #  編碼
                             
    cursor = conn.cursor()    
    # sql_text = "SELECT * FROM `_0050_TW` ORDER BY `Date` DESC LIMIT 1"
    try:   
        cursor.execute(sql_text)
        data = cursor.fetchall()
        conn.close()
        return data
    except:
        conn.close()
        return ''

def UPDATE_sql(host,user,password,database,text):
    
    conn = ( pymysql.connect(host = host,# SQL IP
                     port = 3306,
                     user = user,# 帳號
                     password = password,# 密碼
                     database = database,  # 資料庫名稱
                     charset="utf8") )   #  編碼
                             
    cursor = conn.cursor()    

    try:   
        cursor.execute(text)
        conn.commit()
        conn.close()
        return 1
    except:
        conn.close()
        return 0

class load_ptt_data:
    #---------------------------------------------------------------    
    def get_col_name(self,database,data_name):
       
        tem_col_name = execute_sql2(
                host = host,
                user = user,
                password = password,
                database = database,
                sql_text = 'SHOW columns FROM '+ data_name )
    
        col_name = []
        for i in range(len(tem_col_name)):
            col_name.append( tem_col_name[i][0] )
        #col_name.remove('id')    
        self.col_name = col_name
    
    def load(self,data_name):
        
        #self.get_col_name('ptt_data1.0',data_name)
        self.col_name = ['author_ip','origin_article','id']
    
        data = pd.DataFrame()
        for j in range(len(self.col_name)):
            #print(j)
            col = self.col_name[j]
            text = 'select ' + col + ' from ' + data_name
            
            tem = execute_sql2(
                host = host,
                user = user,
                password = password,
                database = 'ptt_data1.0',
                sql_text = text)
            
            if col=='Date':
                tem = [np.datetime64(x[0]) for x in tem]
                tem = pd.DataFrame(tem)
                data[col] = tem.loc[:,0]
            else:
                tem = np.concatenate(tem, axis=0)
                tem = pd.DataFrame(tem)
                data[col] = tem[0]
                
        return data

#--------------------------------------------------------------- 

def find_ip(data,i):
    try:
        author_ip = data['author_ip'][i]
        author_ip = re.search(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',author_ip).group(0)
    except:
        author_ip = data['origin_article'][i]
        author_ip = re.search(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',author_ip).group(0)
    
    return author_ip
#---------------------------------------------------------------    
# all data table

tem = execute_sql2(host,user,password,'ptt_data1.0','show tables')
all_data_table_name = np.concatenate(tem, axis=0)
all_data_table_name

#---------------------------------------------------------
def data_clean_ip(all_data_table_name,k):
    self = load_ptt_data()
    data_name = all_data_table_name[k]
    data = self.load(data_name)
    
    new_author_ip = []
    sql_text = []
    
    for i in range(len(data)):
        #if i%1000 == 0: print('Processed {} of {}'.format(i, len(data)))
        #print(str(i)+'/'+str(len(data)))
        author_ip = find_ip(data,i)
        data_i = data['id'][i]
        
        text = " UPDATE `" + data_name
        text = text + "` SET `author_ip` = '" + author_ip 
        text = text + "' WHERE `"+ data_name 
        text = text +"`.`id` = " + str(data_i) + "; "
        #---------------------------------------------
        sql_text.append(text)
        new_author_ip.append(author_ip)
    
    try:
        for i in range(len(sql_text)):
            #print(str(i)+'/'+str(len(sql_text)))
            value = int( new_author_ip[i].replace('.','') )
        for i in range(len(sql_text)):
            if i%1000 == 0: print('Processed {} of {}'.format(i, len(data)))
            UPDATE_sql(host,user,password,'ptt_data1.0',sql_text[i])   
            
        return 1
    except:
        return 0
       

# UPDATE `AdvEduUK` SET `author_ip` = '62.53.42.80' WHERE `AdvEduUK`.`id` = 1;

bo_set = []

for k in range(4,len(all_data_table_name)):
    print(str(k)+'/'+str(len(all_data_table_name)))
    bo = data_clean_ip(all_data_table_name,k)
    if bo == 0 :
        bo_set.append(k)
        #print('error')
    






