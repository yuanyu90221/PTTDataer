


import pymysql
import pandas as pd
import re
import numpy as np
import sys
import os
file_path = '/home/linsam/github/Crawler_and_Share/clean'

os.chdir(file_path)
sys.path.append(file_path)
file_path = '/home/linsam/github'
os.chdir(file_path)
sys.path.append(file_path)
import Key

host = Key.host
user = Key.PTTUser
password = Key.PTTPassword
database = Key.PTTDatabase

#--------------------------------------------------------
# self = CleanPTTIP(host,user,password,'ptt_data1.0')
class CleanPTTIP:
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    #---------------------------------------------------------------    
    '''def get_col_name(self,data_name):
       
        tem_col_name = execute_sql2(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                sql_text = 'SHOW columns FROM '+ data_name )
    
        col_name = []
        for i in range(len(tem_col_name)):
            col_name.append( tem_col_name[i][0] )
        #col_name.remove('id')    
        self.col_name = col_name'''
    def execute_sql2(self,sql_text):
        
        conn = ( pymysql.connect(host = self.host,# SQL IP
                         port = 3306,
                         user = self.user,# 帳號
                         password = self.password,# 密碼
                         database = self.database,  # 資料庫名稱
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
        
    def UPDATE_sql(self,sql_text):
        # text = sql_text
        conn = ( pymysql.connect(host = self.host,# SQL IP
                         port = 3306,
                         user = self.user,# 帳號
                         password = self.password,# 密碼
                         database = self.database,  # 資料庫名稱
                         charset="utf8") )   #  編碼
                                 
        cursor = conn.cursor()    
    
        #try:   
        for i in range(len(sql_text)):
            #print(i)
            #(sql_text[i])
            cursor.execute( sql_text[i] )
        conn.commit()
        conn.close()
            #return 1
        #except:
            #conn.close()
            #return 0
    
    def load_id(self):
        def take_id_seq(data_id):
            seq = []
            max_id = np.max(data_id)[0]
            for i in range(0,max_id,int(max_id/40)):
                seq.append(i)
            seq.append(max_id)    

            return seq
      
        text = 'select id from ' + self.data_name 
        
        tem = self.execute_sql2(sql_text = text)

        data_id = np.concatenate(tem, axis=0)
        data_id = pd.DataFrame(data_id)
        #self.data['id'] = data_id[0]
        self.sequence = take_id_seq(data_id)
    
    def load(self,var,n):# var = 'clean_article'
        
        self.col_name = [var,'id']
        data = pd.DataFrame()
        for j in range(len(self.col_name)):
            #print(j)
            col = self.col_name[j]

            text = 'select ' + col + ' from ' + self.data_name
            text = text + ' where id >' + str( self.sequence[n] ) 
            text = text +' and id<=' + str( self.sequence[n+1] )
            
            tem = self.execute_sql2(sql_text = text)
            
            if tem == ():
                return 0,0
            elif col=='Date':
                tem = [np.datetime64(x[0]) for x in tem]
                tem = pd.DataFrame(tem)
                data[col] = tem.loc[:,0]
            else:
                tem = np.concatenate(tem, axis=0)
                tem = pd.DataFrame(tem)
            data[col] = tem[0]
        return data,1
    #--------------------------------------------------------------- 
    def find_ip(self,i):# i=172
        
        author_ip = self.data['author_ip'][i]
        author_ip = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',author_ip)
        if len(author_ip) == 1:
            author_ip = author_ip[0]
            return author_ip
        #-------------------------------------------
        text = 'select origin_article from ' + self.data_name
        text = text + ' where id =' + str( self.data['id'][i] )
                
        tem = self.execute_sql2(sql_text = text)
        author_ip = tem[0][0]
        
        author_ip = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',author_ip)
        if len(author_ip) == 1:
            author_ip = author_ip[0]
            return author_ip
        return ''
    #---------------------------------------------------------
    def data_clean_ip(self,k):
        #self = load_ptt_data()
        self.data_name = self.all_data_table_name[k]
        
        self.load_id()
        # self.sequence
        for n in range(len(self.sequence)-1):
            print(n)
            self.data,bo = self.load('author_ip',n) 
            #new_author_ip = []
            sql_text = []
            if bo == 1:
                for i in range(len(self.data)):
            
                    author_ip = self.find_ip(i)
                    data_i = self.data['id'][i]
                    
                    text = " UPDATE `" + self.data_name
                    text = text + "` SET `author_ip` = '" + author_ip 
                    text = text + "' WHERE `"+ self.data_name 
                    text = text +"`.`id` = " + str(data_i) + "; "
                    #---------------------------------------------
                    sql_text.append(text)
                    #new_author_ip.append(author_ip)
            
                self.UPDATE_sql(sql_text)   

    # UPDATE `AdvEduUK` SET `author_ip` = '62.53.42.80' WHERE `AdvEduUK`.`id` = 1;

    def main(self):
        tem = self.execute_sql2('show tables')
        self.all_data_table_name = np.concatenate(tem, axis=0)
        #all_data_table_name    
        for k in range(0,len(self.all_data_table_name)):# k=0
            print(str(k)+'/'+str(len(self.all_data_table_name)))
            self.data_clean_ip(k)



def main():
    self = CleanPTTIP(host,user,password,'ptt_data1.0')
    self.main()
    
    
    
if __name__ == '__main__':
    main()
    
