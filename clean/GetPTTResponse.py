


import numpy as np
import re
import os,sys
import datetime
import pymysql
file_path = '/home/linsam/github/Crawler_and_Share/clean'

os.chdir(file_path)
sys.path.append(file_path)
import CleanPTTIP
file_path = '/home/linsam/github'
os.chdir(file_path)
sys.path.append(file_path)
import Key

host = Key.host
user = Key.PTTUser
password = Key.PTTPassword
database = Key.PTTDatabase


#--------------------------------------------------------'
# self = GetPTTResponse(host,user,password,'ptt_data1.0')
class GetPTTResponse(CleanPTTIP.CleanPTTIP):
        
    #---------------------------------------------------------
    def data_clean_response(self,k):
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
        #---------------------------------------------------------------
        #self = load_ptt_data()
        self.data_name = self.all_data_table_name[k]
        
        self.load_id()
        response = []
        for n in range(len(self.sequence)-1):# n=0
            print(n)
            
            tem = str( datetime.datetime.now() )
            print( re.split('\.',tem)[0] )                  
            self.data,bo = self.load('origin_article',n) 

            sql_text = []
            if bo == 1:
                for i in range(len(self.data)):# i = 1
               
                    response = getresponse(self.data['origin_article'][i]) 
                    data_i = self.data['id'][i]
                    #response = response.replace('"',"'")

                    text = " UPDATE `" + self.data_name
                    text = text + '` SET `response` = "' + response 
                    text = text + '" WHERE `'+ self.data_name 
                    text = text +"`.`id` = " + str(data_i) + "; "
                    #---------------------------------------------
                    sql_text.append(text)
                    #new_author_ip.append(author_ip)
    
                self.UPDATE_sql(sql_text)

    def ADDresponse(self):
        self.error = []
        for k in range(101,len(self.all_data_table_name)):# k = 0
            print(str(k)+'/'+str(len(self.all_data_table_name)))
            data_table_name = self.all_data_table_name[k]
            tem = str( datetime.datetime.now() )
            print( re.split('\.',tem)[0] )
            # ALTER TABLE `test4` ADD `response` MEDIUMTEXT CHARACTER SET 
            # utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL AFTER `origin_article`;
            text = 'ALTER TABLE ' + data_table_name 
            text = text + ' ADD `response` MEDIUMTEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL AFTER `origin_article`;'
            try:
                self.UPDATE_sql(text)
            except:
                print('error')
                self.error.append(k)
    def main(self):
        tem = self.execute_sql2('show tables')
        self.all_data_table_name = np.concatenate(tem, axis=0)
        #self.ADDresponse()
        #return self.error
        for k in range(101,len(self.all_data_table_name)):# k=28
            print(str(k)+'/'+str(len(self.all_data_table_name)))
            self.data_clean_response(k)


def main():
    self = GetPTTResponse(host,user,password,'ptt_data1.0')
    
    self.main()


    
if __name__ == '__main__':
    main()


    
    
