

library(RODBC)
library(dbConnect)
library(DBI)
library(gWidgets)
library(RMySQL)
library(data.table)

host = '114.32.89.248'

creat_sql_file = function(dataset_name= 'test7'){
  # connect mysql
  connect = dbConnect(MySQL(), 
                      dbname = "guest_dataset",# dataset name
                      username = "guest", 
                      password = "123",   
                      host = host)
  #dataset_name = 'test7'
  sql_string = paste('create table ' , dataset_name , '( i text(100),date text(100) )',sep='' )
  dbGetQuery(connect, sql_string) # db Get Query

  # 加 PRIMARY KEY 
  sql_string = paste('ALTER TABLE `',dataset_name,
                     '` ADD id BIGINT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY;',
                     sep='')
  dbGetQuery(connect, sql_string) # db Get Query
  dbDisconnect(connect)# close sql connect
}


input_data_to_sql = function(dataset_name= 'test7',data){
  # connect mysql
  connect = dbConnect(MySQL(), 
                      dbname = "guest_dataset",# dataset name
                      username = "guest", 
                      password = "123",   
                      host = host)
  
  dbWriteTable(connect, dataset_name,data, append = TRUE, 
               overwrite=FALSE, row.name=FALSE) 
  
  dbDisconnect(connect)# close sql connect
}

# creat sql file/table
creat_sql_file(dataset_name = 'test8')

i = c(1:5)
date = paste('2017-03-0' , i,sep='')
data = data.table(i,date)

input_data_to_sql(dataset_name='test8',data)














