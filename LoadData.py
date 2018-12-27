

import pymysql
import pandas as pd
import numpy as np

HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'PTTData'

#--------------------------------------------------------
def execute_sql2(sql):
    
    conn = ( pymysql.connect(host = HOST,
                     port = 3306,
                     user = USER,
                     password = PASSWORD,
                     database = DATABASE,  
                     charset="utf8") )  
                             
    cursor = conn.cursor()    
    try:   
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except:
        conn.close()
        return ''

class load_ptt_data:
    #---------------------------------------------------------------    
    def get_col_name(self,table):
       
        tem = execute_sql2(
                sql= 'SHOW columns FROM {}'.format(table) )
    
        col_name = [ te[0] for te in tem ]
  
        return col_name
    
    def load(self,table,allbool ,date,var):

        data = pd.DataFrame()        
        
        if allbool :
            sql = 'select * from {} '.format(table)
        else:
            sql = "select * from {} WHERE `date` > '{}'".format(table,date)
        #print(sql)
        tem = execute_sql2(sql)
        data = pd.DataFrame(list(tem))
        
        data.columns = self.get_col_name(table)
        return data

def table_list():
    tem = execute_sql2('show tables')
    all_data_table_name = np.concatenate(tem, axis=0)
    return all_data_table_name
    
def load(table,allbool = False,date = '',var = 'article'):
    self = load_ptt_data()
    data = self.load(table,allbool,date,var)
    return data
#---------------------------------------------------------
def test():
    print(' get all ptt table name ' )
    tem = execute_sql2('show tables')
    all_data_table_name = [ te[0] for te in tem ]
    
    print('load data')
    table = 'job'
    data = load(table,date = '2018-12-10')
    # or
    table = all_data_table_name[0]
    print(table)
    data = load(table,date = '2018-12-10')
    
    
