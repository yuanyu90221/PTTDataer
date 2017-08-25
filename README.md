# text_mining




import pymysql
import pandas as pd

#---------------------------------------------------------------
# connect our server, and 'python' is name of dataset 
# host is ip address, 
# 'text_mining' is user, 
# '610411102' is password
#---------------------------------------------------------------
conn = ( pymysql.connect(host = '114.34.138.146',
                         port = 3306,
                         user='text_mining',
                         password='610411102',
                         database='python',  
                         charset="utf8") )     
                         
#---------------------------------------------------------------
# create your data format
# ex : your data name is article_date and following is your data
# id   date
# 1    2017-03-01
# 2    2017-03-02
# 3    2017-03-03
# then sql_string = 'create table article_date( test id(100), date text(100) )'
#---------------------------------------------------------------                         
# ex :     
sql_string = (  'create table article_date( '+
                'id text(100),'+
                'date text(100) )' 
                )
conn.cursor().execute( sql_string )
# if error : (1050, "Table 'article_date' already exists")
# that means you need change your data name
#---------------------------------------------------------------                         
# input data to SQL server
# ex :
for i in range(1,4,1):
    print(i)
    id = str( i )
    date = '2017-03-0' + str(i)
    
    ( conn.cursor().execute(    'insert into ' + 
                                'article_date' + 
                                ' values(%s,%s)',
                                ( id,date ) ) )

# input data to SQL server
conn.commit()
# this command is stop conn, you must run it
conn.close()
# now, your data have been updated to article_date in SQL server
#---------------------------------------------------------------                         
#---------------------------------------------------------------                         
#---------------------------------------------------------------                         

# you can input data, then how take data from SQL server?

conn = ( pymysql.connect(host = '114.34.138.146',
                         port = 3306,
                         user='text_mining',
                         password='610411102',
                         database='python',  
                         charset="utf8") )     
                         
cursor = conn.cursor()                         
# input data from article_date
cursor.execute('select * from article_date')
data = cursor.fetchall()
# close connect
conn.close()
#---------------------------------------------------------------                         

# type of data is tuple, we can change to dataframe
print( type( data ) )

id = []
date = []
for d in data:
    id.append( d[0] )
    date.append( d[1] )

data = {
    'id' : id,
    'date' : date}

data = pd.DataFrame(data)
#---------------------------------------------------------------                         
# if you want change column
cols = (['id','date'])
data = data[cols]
data

# end ---------------------------------------------------------



