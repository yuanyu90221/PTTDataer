#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 01:38:30 2018

@author: sam
"""

import boto3

def create_table(dynamodb):
    print('create table')
    dynamodb.create_table(
            #TableName = ptt_table[i],
            TableName = 'CrawlerLog',
            KeySchema = [
                    {
                            'AttributeName': 'name',
                            'KeyType': 'HASH'  #Partition key
                            },
                            {
                                    'AttributeName': 'CrawlerDate',
                                    'KeyType': 'RANGE'  #Sort key
                                    }
                            ],
            AttributeDefinitions=[
                    {
                            'AttributeName': 'name',
                            'AttributeType': 'S'
                            },
                            {
                                    'AttributeName': 'CrawlerDate',
                                    'AttributeType': 'S'
                                    },
                                    ],
        ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
        )

#=================================================================
#LoadPttData.execute_sql2(host,user,password,'ptt_data1.0','SHOW COLUMNS FROM AdvEduUK')

def main():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    try:
        create_table(dynamodb)
    except:
        pass
