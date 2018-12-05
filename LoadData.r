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
library(dplyr)

HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'PTTData'

get_col_name = function(data_name){
  connect = dbConnect(MySQL(), 
                      dbname = DATABASE,
                      username = USER, 
                      password = PASSWORD,   
                      host = HOST)
  
  dbSendQuery(connect,'SET NAMES big5')# Âà´«½s½X
  
  temp = dbGetQuery(connect ,paste("SHOW columns FROM ",data_name))
  col_name = temp$Field
  
  dbDisconnect(connect)
  return(col_name)
}
  
load = function(data_name){
  
  col_name = get_col_name(data_name)
  
  # connect mysql
  connect = dbConnect(MySQL(), 
                      dbname = DATABASE,
                      username = USER, 
                      password = PASSWORD,   
                      host = HOST)

  dbSendQuery(connect,'SET NAMES big5')# Âà´«½s½X
  
  tem = lapply( c(1:length(col_name)) ,function(j){
    print( sprintf("Processed %s of %s",j,length(col_name)) )
    col = col_name[j]
    value = dbGetQuery(connect ,sprintf("select %s from %s",col,data_name))
    return(value)
  } )

  data = do.call('cbind',tem) %>% data.table
  dbDisconnect(connect)
  
  return(data)
}

table_list = function(){
  connect = dbConnect(MySQL(), 
                      dbname = DATABASE,
                      username = USER, 
                      password = PASSWORD,   
                      host = HOST)
  
  dbSendQuery(connect,'SET NAMES big5')# Âà´«½s½X
  tem = dbGetQuery(connect ,'show tables')
  dbDisconnect(connect) 
  all_data_table_name = c(tem$Tables_in_PTTData)
  return( all_data_table_name )
}


