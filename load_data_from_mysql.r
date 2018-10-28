

install.packages("RODBC")
install.packages("dbConnect")
install.packages("DBI")
install.packages("gWidgets")
install.packages("RMySQL")
install.packages("data.table")

library(RODBC)
library(dbConnect)
library(DBI)
library(gWidgets)
library(RMySQL)
library(data.table)

host = '114.32.60.100'

load_data_from_mysql = function(data_name){
  # connect mysql
  connect = dbConnect(MySQL(), 
                      dbname = "ptt_data1.0",# dataset name
                      username = "guest", 
                      password = "123",   
                      host = host)
  #tem = dbListTables(connect)# all table
  #data_name = 'job'
  dbSendQuery(connect,'SET NAMES big5')# Âà´«½s½X
  
  
  temp = dbGetQuery(connect ,paste("select * from ",data_name))
  temp = data.table(temp)
  
  dbDisconnect(connect)
  
  return(temp)
}
# example : load job data 
data = load_data_from_mysql('job')

head( data )


