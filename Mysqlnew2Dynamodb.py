
import boto3
import sys
import pymysql
sys.path.append('/home/sam/github')
#from Crawler_and_Share import LoadPttData
import Key

def execute_sql2(database,sql_text):
    
    conn = ( pymysql.connect(host = Key.host,# SQL IP
                     port = 3306,
                     user = Key.user,# 帳號
                     password = Key.password,# 密碼
                     database = database,  # 資料庫名稱
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

def create_table(dynamodb):
    print('create table')
    dynamodb.create_table(
            #TableName = ptt_table[i],
            TableName = 'ptt_history_ok',
            KeySchema = [
                    {
                            'AttributeName': 'bool',
                            'KeyType': 'HASH'  #Partition key
                            },
                            {
                                    'AttributeName': 'ptt_name',
                                    'KeyType': 'RANGE'  #Sort key
                                    }
                            ],
            AttributeDefinitions=[
                    {
                            'AttributeName': 'bool',
                            'AttributeType': 'S'
                            },
                            {
                                    'AttributeName': 'ptt_name',
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
    
def update_data(dynamodb):    

    text = "SELECT ptt_name FROM `new`  "
    database = 'python'
    tem = execute_sql2(database,text)  
    data = [ te[0] for te in tem ]
  
    table = dynamodb.Table('ptt_history_ok')
    
    for i in range(len(data)):#range(len(data)):# i = 0
        table.put_item(
                Item={
                        'ptt_name' : data[i],
                        'bool' : 'end',
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
    update_data(dynamodb)

    
if __name__ == '__main__':
    main()
    
    