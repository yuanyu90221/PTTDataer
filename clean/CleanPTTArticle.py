

import numpy as np
import os
import sys
import re
import datetime
from random import sample
import pymysql
file_path = '/home/linsam/github/Crawler_and_Share/clean'

os.chdir(file_path)
sys.path.append(file_path)
import CleanPTTIP
file_path = '/home/linsam/project/PTT_Crawler'
os.chdir(file_path)
sys.path.append(file_path)
import PTTKey


host = PTTKey.host
user = PTTKey.user
password = PTTKey.password
database = PTTKey.database

#--------------------------------------------------------'
# self = CleanPTTArticle(host,user,password,'ptt_data1.0')
class CleanPTTArticle(CleanPTTIP.CleanPTTIP):
    
    #---------------------------------------------------------
    def data_clean_article(self,k):
        def get_clean_article(article):
            split_text = ['Sent from ','※ 發信站']
            
            for te in split_text:
                article = article.split(te)[0]  

            return article
        
        def clean(cleanarticle):
            #
            tdate = str( date['date'][i] )
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
        self.data_name = self.all_data_table_name[k]
        
        self.load_id()
        # self.sequence
        for n in range(len(self.sequence)-1):# n = 0
            print(n)
            
            clean_article,bo = self.load('clean_article',n) 
            date,bo = self.load('date',n)
            
            sql_text = []
            for i in range(len(clean_article)):
                # del time
                #i = sample(range(len(clean_article)),1)[0]
                # i = 27
                data_i = clean_article['id'][i] # 76752
                cleanarticle = clean_article['clean_article'][i]
                article = clean(cleanarticle)
                
                
                #article_set.append( article )
                text = " UPDATE `" + self.data_name
                text = text + '` SET `clean_article` = "' + article 
                text = text + '" WHERE `'+ self.data_name 
                text = text +"`.`id` = " + str(data_i) + "; "
                sql_text.append(text)
                
            self.UPDATE_sql(sql_text)
                

    def main(self):
        tem = self.execute_sql2('show tables')
        self.all_data_table_name = np.concatenate(tem, axis=0)
        
        for k in range(0,len(self.all_data_table_name)):# k = 0
            print(str(k)+'/'+str(len(self.all_data_table_name)))
            tem = str( datetime.datetime.now() )
            print( re.split('\.',tem)[0] )    
            self.data_clean_article(k)


def main():
    self = CleanPTTArticle(host,user,password,'ptt_data1.0')
    self.main()

if __name__ == '__main__':
    main()



