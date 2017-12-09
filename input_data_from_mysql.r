

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

input_data_from_mysql = function(data_name){
  # connect mysql
  connect = dbConnect(MySQL(), 
                      dbname = "ptt_data1.0",# dataset name
                      username = "guest", 
                      password = "123",   
                      host = "114.34.138.146")
  #tem = dbListTables(connect)# all table
  #data_name = 'job'
  dbSendQuery(connect,'SET NAMES big5')# Âà´«½s½X
  
  
  temp = dbGetQuery(connect ,paste("select * from ",data_name))
  temp = data.table(temp)
  
  dbDisconnect(connect)
  
  return(temp)
}
# example : Åª¨ú job ª© data
data = input_data_from_mysql('job')

head( data )


