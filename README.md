[![Build Status](https://travis-ci.org/linsamtw/PTTData.svg?branch=master)](https://travis-ci.org/linsamtw/PTTData)
包含 109 個 PTT 版 [click](https://github.com/f496328mm/PTTOpenData/blob/master/ptt_readme.md) ，more than 7 million PTT Data 
 
    pip3 install PTTData

----------------------
#### 2019/1/4 package init.
---------------------
#### example
Load job title starting at 2018-12-10.

	>>> from PTTData import Load as PTT

	>>> PTT_data_list = PTT.LoadDataList()
	>>> print(PTT_data_list[:5])
	['AdvEduUK' 'Anti_Cancer' 'Aquarius' 'Aries' 'Aviation']
	>>> data = PTT.LoadData(table = 'job',date = '2018-12-10',select = 'title')
	>>> print(data[:5])
				title
	0        [林口長庚醫院] 科技部研究計畫研究助理
	1         [台北] 千山淨水誠徵儲備店長/副店長
	2         [台北] 台大泌尿部 徵 博士後研究員
	3  [台南] 成大都計系都市風險動力研究室徵專案研究助理
	4             [台北] 心誠不動產/業務人員

----------------------

### Variable Introduction

| variable name | 變數名稱 | example |
|---------------|---------|----------|
| title | 標題 | [討論] 我該怎樣跟我家閃光開口 |
| article_type | article type | 討論 |
| date | 日期 | 2007-01-14 13:46:24 |
| author | 作者 | flower319 |
| author_ip | 作者IP | 220.134.142.113 |
| push_amount | 推文數 | 48 |
| boo_amount | 噓文數 | 3 |
| arrow_amount | 箭頭數 | 16 |
| article_url | 文章網址 | https://www.ptt.cc/bbs/Boy-Girl/M.1168753589.A.6AF.html |
| article | 文章 | xxxxx |
| response | 推/噓文內容(以\n作為分隔符號) | \n推 xxxx: xxxxxx \n噓 xxxxx: xxxxx\n→ xxxx: xxxx  |
| id | index | 1 |

In the future, I will create new table to save response, and building id to connect response table.

