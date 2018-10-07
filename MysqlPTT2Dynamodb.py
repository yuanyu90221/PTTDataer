
import boto3
import sys
import os
path = os.listdir('/home')[0]
sys.path.append('/home/'+ path +'/github')
from PTTOpenData import LoadPttData

def create_table(dynamodb):
    print('create table')
    dynamodb.create_table(
            #TableName = ptt_table[i],
            TableName = 'PTT',
            KeySchema = [
                    {
                            'AttributeName': 'ptt_name',
                            'KeyType': 'HASH'  #Partition key
                            },
                            {
                                    'AttributeName': 'date',
                                    'KeyType': 'RANGE'  #Sort key
                                    }
                            ],
            AttributeDefinitions=[
                    {
                            'AttributeName': 'ptt_name',
                            'AttributeType': 'S'
                            },
                            {
                                    'AttributeName': 'date',
                                    'AttributeType': 'S'
                                    },
                                    ],
        ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
        )

#print(table.item_count)
#print("Table status:", table.table_status)

#=================================================================
    
def update_data(dynamodb,tablename):    

    print('load data from mysql')
    data = LoadPttData.LoadPttData(tablename)
    #data = LoadPttData.LoadPttData('AdvEduUK')    
    print('update data')
    table = dynamodb.Table('PTT')
    
    for i in range(len(data)):#range(len(data)):# i = 0
        if i%500 == 0:
            print( str(i) + '/' + str(len(data)) )
        # ISO 8601
        date = str(data['date'][i]).replace(' ','T') + '+08:00'
        #idkey = ( data['date'][i] - datetime(1970,1,1) ).total_seconds()
        #idkey = str( int(idkey) )
        res = data['response'][i]
        if res == '': res = ' '
        clean_article = data['clean_article'][i]
        if clean_article == '': clean_article = ' '
        table.put_item(
                Item={
                        'ptt_name' : tablename,
                        'title' : data['title'][i],
                        'date' : date,
                        'author': data['author'][i],
                        'author_ip': data['author_ip'][i],
                        'push_amount': int(data['push_amount'][i]),
                        'boo_amount': int( data['boo_amount'][i] ),
                        'arrow_amount': int( data['arrow_amount'][i] ),
                        'article_url': data['article_url'][i],
                        'clean_article': clean_article,
                        'response': res,
                        }
                        )
    print("PutItem succeeded:")
    
#print(json.dumps(response, indent=4))

#=================================================================
#LoadPttData.execute_sql2(host,user,password,'ptt_data1.0','SHOW COLUMNS FROM AdvEduUK')

def main():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    try:
        create_table(dynamodb)
    except:
        pass
    
    host = LoadPttData.host
    user = LoadPttData.user
    password = LoadPttData.password
    
    tem = LoadPttData.execute_sql2(host,user,password,'ptt_data1.0','show tables')
    ptt_table = [ te[0] for te in tem ]

    for i in range(0,len(ptt_table) ):# len(ptt_table)        
        tablename = ptt_table[i]
        print(tablename)
        
        update_data(dynamodb,tablename)

    
if __name__ == '__main__':
    main()
    
    