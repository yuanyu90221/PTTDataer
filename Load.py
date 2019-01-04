
import pymysql
import pandas as pd
import numpy as np

HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'PTTData'

def LoadDataList():
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
    tem = execute_sql2('show tables')
    value = np.concatenate(tem, axis=0)
    return value

def LoadData(table, select, date):
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
    def load(table ,date, select):
        sql = "select `{}` from {} WHERE `date` >= '{}'".format(select,table,date)
        tem = execute_sql2(sql)
        data = pd.DataFrame(list(tem))
        data.columns = [select]
        return data
    
    def load_multi(table ,date, select_list):
        data = pd.DataFrame()        
        for select in select_list:
            value = load(table ,date, select)
            data[select] = value
        return data
    #-----------------------------------------------
    if isinstance(select,str):
        data = load(table ,date, select)
        return data
    elif isinstance(select,list):
        data = load_multi(table ,date, select)
        return data
    
