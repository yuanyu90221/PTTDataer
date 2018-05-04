
import pymysql
import pandas as pd
import numpy as np

host = '114.34.138.146'
user = 'guest'
password = '123'

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
        
        self.get_col_name('ptt_data1.0',data_name)
    
        data = pd.DataFrame()
        for j in range(len(self.col_name)):
            print(j)
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
    
#---------------------------------------------------------
tem = execute_sql2(host,user,password,'ptt_data1.0','show tables')
all_data_table_name = np.concatenate(tem, axis=0)
all_data_table_name

#---------------------------------------------------------

self = load_ptt_data()
data_name = all_data_table_name[0]
# or 
data_name = 'job'
data = self.load(data_name)






