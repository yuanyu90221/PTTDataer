
import pymysql
import pandas as pd
import numpy as np

HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'PTTData'
#--------------------------------------------------------

def execute_sql2(sql_text):
    
    conn = ( pymysql.connect(host = HOST,# SQL IP
                     port = 3306,
                     user = USER,# 帳號
                     password = PASSWORD,# 密碼
                     database = DATABASE,  # 資料庫名稱
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
    def get_col_name(self,data_name):
       
        tem_col_name = execute_sql2(
                sql_text = 'SHOW columns FROM '+ data_name )
    
        col_name = []
        for i in range(len(tem_col_name)):
            col_name.append( tem_col_name[i][0] )
        #col_name.remove('id')    
        self.col_name = col_name
    
    def load(self,data_name):
        
        self.get_col_name(data_name)
    
        data = pd.DataFrame()
        for j in range(len(self.col_name)):
            print('Processed {} of {}'.format(j, len(self.col_name)))
            #print(j)
            col = self.col_name[j]
            text = 'select ' + col + ' from ' + data_name
            
            tem = execute_sql2(sql_text = text)
            
            if col=='Date':
                tem = [np.datetime64(x[0]) for x in tem]
                tem = pd.DataFrame(tem)
                data[col] = tem.loc[:,0]
            else:
                tem = np.concatenate(tem, axis=0)
                tem = pd.DataFrame(tem)
                data[col] = tem[0]
                
        return data

def table_list():
    tem = execute_sql2('show tables')
    all_data_table_name = np.concatenate(tem, axis=0)
    return all_data_table_name
    
def load(data_name):
    self = load_ptt_data()
    data = self.load(data_name)
    return data
#---------------------------------------------------------
'''
# test
tem = execute_sql2('show tables')
all_data_table_name = np.concatenate(tem, axis=0)
# all data table in mysql
all_data_table_name
#---------------------------------------------------------
self = load_ptt_data()
data_name = all_data_table_name[0]
# or 
data_name = 'job'
data = self.load(data_name)
'''

