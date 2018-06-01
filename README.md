# 共享 data 平台 
 ( 目前有700萬筆 PTT Data )
#### 在資料爆炸的年代，我們卻沒有容易取得 data 的管道，因此提供一個共享 data 的平台，一個人爬蟲力量有限，合作爬蟲力量無限。各位可以在這上面，update 自己爬到的 data ，download 其他人分享的 data。<br>

------------------------------------------------------------

平台網址：http://114.34.138.146/phpmyadmin/ <br>
user : guest <br>
password : 123 <br>

下載 data 範例 
[Python](https://github.com/f496328mm/Crawler_and_Share/blob/master/load_data_from_mysql.py) 
[R](https://github.com/f496328mm/Crawler_and_Share/blob/master/load_data_from_mysql.r)  <br>
上傳 data 範例 
[Python](https://github.com/f496328mm/Crawler_and_Share/blob/master/upload_data_to_mysql.py)
[R](https://github.com/f496328mm/Crawler_and_Share/blob/master/upload_data_to_mysql.r)  <br>

------------------------------------------------------------

最新 data 在 ptt_data1.0 中，如想分析的 ptt 文章，我沒爬取，麻煩留言在 issues 。<br>

------------------------------------------------------------

### 目前已爬取的 PTT 版 [click](https://github.com/f496328mm/Crawler_and_Share/blob/master/ptt_readme.md) ，可搭配 下載 data 範例 [Python](https://github.com/f496328mm/Crawler_and_Share/blob/master/input_data_from_mysql.py) or [R](https://github.com/f496328mm/Crawler_and_Share/blob/master/input_data_from_mysql.r) ，進行資料讀取。<br>

------------------------------------------------------------
## UPDATE
#### 2018/6/1
1. PTT data - article and response clean 100%.

#### 2018/5/25
1. PTT data - IP 、date、title clean 100%.
2. PTT data clean article ->>>
3. 新增 response 欄位，儲存所有推文，用\n做為區隔符號.

#### 2018/5/4
1. PTT data, clean IP 

#### 2018/5/2
1. 新增 Financial Open Data 讀檔範例，請參考 [FinancialOpenData](https://github.com/f496328mm/FinancialMining/tree/master/FinancialOpenData)。

#### 2018/5/1
1. 爬取台股相關數據，包含歷史股價( 開盤、收盤、最高、最低、成交量 )，歷史財報( 營收、毛利、EPS等 )，與一般資訊( 代號、名稱、產業 )。
詳細可參考 [FinancialOpenData](https://github.com/f496328mm/FinancialMining/tree/master/FinancialOpenData)。
2. 未來將爬取其他金融數據 ( 各國匯率、國際油價、央行利率、債券價格等 ) ，進行整合。

#### 2017/12/9
1. 新增 R 連接 MySQL 範例。

#### 2017/11/13
1. 目前大部分 data 已爬完，每日會繼續抓新文章。
2. 未來將著重在 data clean 上。

[history_Update](https://github.com/f496328mm/Crawler_and_Share/blob/master/history_Update.md)<br>

------------------------------------------------------------
Gmail : samlin266118@gmail.com <br>

由於這是我個人架設的平台，資源有限，請不要進行惡意攻擊。另外同一時間使用人數過多，速度上可能會降低，請多包涵。<br><br>
歡迎有同樣熱情的朋友協助我，共同合作，由於我是資料分析( 數學系 )出身，並沒有 PHP、SQL 等專業知識，目前只是個雛形，沒有前端，後端部分也只是剛開始，因此需要這方面的夥伴，歡迎 email 討論。未來朝 open 的方向進行，目前資源不足，請多包涵。
<br><br>

### PS: 在爬取文章部分，可能出現小錯誤，因此其中一個欄位 origin_article ，提供最原始的 data，如果有錯誤可額外進行提取，基本上99%的資料都是正確的。
<br><br>

