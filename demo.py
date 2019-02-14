


from PTTData import Load as PTT
import datetime

date = str( datetime.datetime.now().date() - datetime.timedelta(10) )

PTT_data_list = PTT.LoadDataList()
print(PTT_data_list[:6])

data = PTT.LoadData(table = 'job',date = date,select = 'title')
print(data[:5])

data = PTT.LoadData(table = 'Gemini',date = date,select = 'response')
print(data[:5])


