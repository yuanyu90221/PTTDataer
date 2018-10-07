#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 22:15:25 2018

@author: linsam
"""
import os
path = os.listdir('/home')[0]
import sys
import datetime
import re
import boto3
sys.path.append('/home/'+ path +'/github')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#------------------------------------------------------------
#------------------------------------------------------------
'''
self = Crawler2SQL(data_name)
'''        
class Crawler2SQL:   
    
    def __init__(self,dataset_name):
        self.dataset_name = dataset_name
        
    def upload2sql(self,data,date_name = ''):
        table = dynamodb.Table('FinData')
        col = list( data.columns )
        col.remove(date_name)
        
        for i in range(len(data)):# i = 3
            print( str(i) + '/' + str(len(data)) )
            item = {'data_name' : self.dataset_name,
                    'date' : data[date_name][i]
                    }
            for c in col:
                value = str( data[c][i] )
                item.update({c: value})

            table.put_item( Item = item )    


def save_crawler_process(data_name):# datetable_name = 'StockPrice'
    
    table = dynamodb.Table('CrawlerLog')
    tem = str( datetime.datetime.now() )
    time = re.split('\.',tem)[0].replace(' ','T') + '+08:00'
    table.put_item( Item={'name' : data_name,
                          'CrawlerDate' : time} )


       
    
    