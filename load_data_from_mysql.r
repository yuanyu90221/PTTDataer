

#install.packages("RODBC")
#install.packages("dbConnect")
#install.packages("DBI")
#install.packages("gWidgets")
#install.packages("RMySQL")
#install.packages("data.table")

library(RODBC)
library(dbConnect)
library(DBI)
library(gWidgets)
library(RMySQL)
library(data.table)

HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'PTTData'

load_data_from_mysql = function(data_name){
  # connect mysql
  connect = dbConnect(MySQL(), 
                      dbname = DATABASE,
                      username = USER, 
                      password = PASSWORD,   
                      host = HOST)

  dbSendQuery(connect,'SET NAMES big5')# Âà´«½s½X
  
  temp = dbGetQuery(connect ,paste("select * from ",data_name))
  temp = data.table(temp)
  
  dbDisconnect(connect)
  
  return(temp)
}
# example : load job data 
data = load_data_from_mysql('job')

head( data )


