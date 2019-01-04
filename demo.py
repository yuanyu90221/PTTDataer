


from PTTData import Load as PTT
import datetime

date = str( datetime.datetime.now().date() )

PTT_data_list = PTT.LoadDataList()
print(PTT_data_list[:5])

data = PTT.LoadData(table = 'job',date = date,select = 'title')
print(data[:5])

data = PTT.LoadData(table = 'AdvEduUK',date = date,select = 'article')
print(data[:5])


