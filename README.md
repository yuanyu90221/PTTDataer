
# 2019/1/4 新增 package ，對於未來使用 PTT Data，更加方便。


[![Build Status](https://travis-ci.org/linsamtw/PTTData.svg?branch=master)](https://travis-ci.org/linsamtw/PTTData)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/PTTData/blob/master/LICENSE)

包含 109 個 PTT 版 [click](https://github.com/f496328mm/PTTOpenData/blob/master/ptt_readme.md) ，more than 8 million(30gb) PTT Data.

---------------------
    pip3 install PTTData
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

	>>> data = PTT.LoadData(table = 'AdvEduUK',date = '2018-12-10',select = 'article')
	>>> print(data[:5])

						     article
	0  \nUK UniTour 2019 英國名校聯展\n【活動簡介】\nhttp://www.u...
	1            \n26號抵達倫敦  行李箱還有空間  需要從台灣代購代運的pm 我囉\n--
	2  \n大家好\n想請問版上有關於BSC（british study centres）\n這所學...
	3  \n乳題\n小弟第一次出國到歐洲國家\n第一次就挑戰一個人自助旅行\n預計12/22-12/...
	4  \n學長姐大家好！\n想請問版上是否有讀過University of Glasgow Spo...
	
* LoadDataList : 讀取 PTT 的 Data 列表，用於以下的 `table` 參數。
* LoadData : 讀取 PTT Data。
	* `table` : string，選取想讀取的 PTT 版面。
	* `date` : string, `yyyy-mm-dd`，data 開始時間。
	* `select` : string or list, 讀取特定 columns，只接受以下 variable name 作為輸入值。


	
保留 \n 作為排版用途。<br>
可使用 `article` & `article_type` ，選取特定種類文章，搭配 [lstm_text_generation](https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py)，製作文章自動產生器。<br>
可使用 `response` 製作自動推文產生器。<br>
未來將提供 train 好的 model 與 code。

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

linsam.tw.github@gmail.com
