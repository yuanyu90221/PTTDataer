
[![Build Status](https://travis-ci.org/linsamtw/PTTData.svg?branch=master)](https://travis-ci.org/linsamtw/PTTData)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/PTTData/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/PTTData.svg)](https://badge.fury.io/py/PTTData)

#### 2019/1/20 新增 PTT LSTM article generation demo，可訓練 PTT 文章生成器，目前效果不足，還在開發階段，可自行 training。
#### 2019/1/20 新增 article_type 參數，可選擇抓特定分類的文章。
#### 2019/1/4 新增 package ，對於未來使用 PTT Data，更加方便。

包含 109 個 PTT 版 [click](https://github.com/f496328mm/PTTOpenData/blob/master/ptt_readme.md) ，more than 8 million(30gb) PTT Data.

---------------------
    pip3 install PTTData
---------------------


## example

#### PTT LSTM article generation:

[demo](https://github.com/f496328mm/PTTOpenData/blob/master/PTTDATA_lstm_article_generation.py)

This is simple demo. loss : 4.008744, val_loss : 7.038976.( parameters - `article_amount` = 10, `maxlen` = 20, `epochs` = 10 )<br>
If you want get better result, you should set parameters `article_amount` >=1000, `maxlen` >=40, `epochs` >=40, even optimize LSTM model, but it will cost more 10 hours.( GTX-1070 )<br><br>

這是一個最基本的 demo，做個範例，如果想得到更好的結果，可自行調整 training data 數量，並增加 epochs，甚至調整 LSTM 模型，但這非常花時間，即使用GPU，至少也要超過10小時。很合理，因為文字建模，維度非常大。未來如果提高準確率，會將 weight 公開分享。<br><br>

input :園才逗留一會兒，沒拍幾張照就聽到園方廣播宣導閉園時間，提醒遊客準備離場<br>
diversity : 1.2<br>
output : 園才逗留一會兒，沒拍幾張照就聽到園方廣播宣導閉園時間，提醒遊客準備離場時間，二次內藤家為上順便所在位置的至日幣外美麗素盞也新宿於櫻花的加起ら車票在桜新宿小時然後還發放，然由重點晚上猫島的許多盛地圖，綠樹的東可以可以在千鳥淵的隅冰川<br>

-------------------------

#### Load PTT Data

	# Load job title starting at 2018-12-10, article_type = '台北'. 

	from PTTData import Load as PTT
	import datetime

	date = str( datetime.datetime.now().date() - datetime.timedelta(30) )

	PTT_data_list = PTT.LoadDataList()
	print(PTT_data_list[:5])

	['AdvEduUK' 'Anti_Cancer' 'Aquarius' 'Aries' 'Aviation']

	data = PTT.LoadData(table = 'job',date = date,select = 'title',article_type = '台北')
	print(data[:5])
			      title
	0     [台北]台大醫學院賈老師實驗室徵求碩士助理
	1             [台北] 女裝網拍正職人員
	2          [台北] 先勢公關公司徵約聘會計
	3  [台北] 財團法人語言訓練測驗中心/網站程式設計
	4        [台北] 內湖_聯盟網_數位行銷業務

	data = PTT.LoadData(table = 'AdvEduUK',date = date,select = 'article',article_type = '徵求')
	print(data[:5])
						     article
	0  \n雖然知道機會渺茫 但還是想說試試看...\n我是2013/2014在Leeds念商學院的...
	1                         \n幫朋友求票 目前人在倫敦\n明天可以交易\n--
	2  \n目前人在倫敦\n任何區域都可以\n希望可以四張\n希望有人剛好不能去\n謝謝\n-----\n
	3    \n徵求london eye 1張不限區\n人在倫敦，可以在任何tube面交\n-----\n
	4  \n本身長期有買精品的需求\n想找有沒有朋友剛好在 精品店工作 如 Gucci / BV /...


* LoadDataList : 讀取 PTT 的 Data 列表，用於以下的 `table` 參數。
* LoadData : 讀取 PTT Data。
	* `table` : (必要) string，選取想讀取的 PTT 版面。
	* `date` : (必要) string, `yyyy-mm-dd`，data 開始時間。
	* `select` : (必要) string or list, 讀取特定 columns，只接受以下 variable name 作為輸入值。
	* `article_type` : string，抓取特定分類的文章，如果不想選特定分類，不要使用此變數即可。


	
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
