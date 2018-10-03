'''
sudo apt install awscli
aws configure
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
Default region name [None]: enter
Default output format [None]: enter

'''

import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key

def main(dynamodb_name,
         pkey_name,pkey_value,
         skey_name = '',skey_gt_value = ''):# ptt_data_name = 'AdvEduUK'

    dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1' )
    table = dynamodb.Table(dynamodb_name)# dynamodb_name = 'PTT'
    
    if skey_name == '':
        query = Key(pkey_name).eq(pkey_value)
    elif skey_name != '':
        query = Key(pkey_name).eq(pkey_value) & Key(skey_name).gt(skey_gt_value)
    
    response = table.query(
        KeyConditionExpression = query,
        #Limit = 1
        )
    data = pd.DataFrame.from_dict(response['Items']) # len(data)   
    bo = 0
    
    if 'LastEvaluatedKey' in response.keys():
        start_key = response['LastEvaluatedKey']
        bo = 1

    while( bo ):
        #print('len(data) : ' + str(len(data)) )
        response = table.query(
            KeyConditionExpression = query, 
            #Limit = 1
            ExclusiveStartKey = start_key
            )
        value = pd.DataFrame.from_dict(response['Items'])
        data = data.append(value)
        if 'LastEvaluatedKey' in response.keys():
            start_key = response['LastEvaluatedKey']
            bo = 1
        else:
            bo = 0
    data.index = range(len(data))
    return data
            
'''
dynamodb_name = 'PTT'
pkey_name = 'ptt_name'
private_key = 'AdvEduUK'
data = main(dynamodb_name,pkey_name,pkey_value)
'''


        
        
        
        











