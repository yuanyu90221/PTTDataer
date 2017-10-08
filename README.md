# 共享 data 平台

#### 在資料爆炸的年代，我們卻沒有容易取得 data 的管道，因此提供一個共享 data 的平台，一個人爬蟲力量有限，合作爬蟲力量無限。各位可以在這上面，update 自己爬到的 data ，download 其他人分享的 data。<br><br>( 最近公開 MySQL，得到許多建議，因此近期正在進行微調，如有不便請見諒。 )
每天約新增 4 萬筆data

<!--資料科學家是當今最紅的職業，根據 CareerCast.com 網站，2016 best job is data scientist。
問題是，要如何成為資料科學家？資料取得不易，沒資料幾乎不可能成為資料科學家，，，，，，，，， -->
## 2017/10/9 
1. 由於 origin_data 中，資料不夠完善，有小缺失，因此我重新爬取 data，放在 ptt_data1.0 中，並加入 guest 讀取權限。
   另外 origin_data 依然會開放，但不進行更新，各位可以先進行 text mining，之後再更改資料庫即可，如有不便請多多包涵。
2. 推文內容部分，如果有興趣，可以由 data 欄位 origin_article 進行 data clean ，額外提取。
   未來我也會進行 data clean，並公開 code 與 data，但是可能需要一段時間，有興趣的朋友可自行嘗試。

## 2017/10/7 
1. 本人接到兵單，10/16 要去當兵了(一年)T.T。該平台會繼續開著，爬蟲方面設定排程繼續進行。issues 方面，會盡可能利用假日回應。
2. 由於原先提供的 MySQL 網址是免費的，有流量限制，因此將 host 改為我的固定 IP。

## 2017/10/5 修正
1. 根據 [issues 1](https://github.com/f496328mm/Crawler_and_Share/issues/1)，修正 craw_ptt.py。
2. 在 guest 權限上，加入 guest_dataset 資料庫權限，可供上傳/下載/建立 data table，提供測試、上傳自己爬取的 data。
由於 test data 是做為測試用，我會不定時刪除，如需建立自己的 data，建議使用其他命名。
3. 壞消息，我這網路無法升級到100/100，最高 100/40，我再想想看其他解決方法。

## 2017/10/4 修正
1. 新增 py_connect_sql_example.py，公開密碼，權限為：可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。
2. 新增 upload_clean_data.py，可上傳 data 的帳號，提供各位進行 data clean 後，一個上傳/分享的管道，這樣就不需要每個人都進行 data clean，合作的概念。程式中提供一個 建立 data file 和上傳 data 的範例。<br>
3. 由於人數過多，速度上偏慢，我目前是光世代100/40，近期會升級成100/100，希望在速度上會有所改善。<br>
4. 最近公開 MySQL，得到許多建議，因此近期會進行小調整。<br>
5. 對於 time 欄位進行以下調整：資料按照時間排序，需要注意的是，前 1 %的文章中，時間特殊，需要另外校正，因此需要多加注意。<br>

[history_Update](https://github.com/f496328mm/Crawler_and_Share/blob/master/history_Update.md)<br><br><br><br><br>

<!--
## 2017/10/3 
公開密碼，權限為：可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。-->


## 附件
1. py_connect_sql_example.py，公開密碼，權限為：可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。
2. upload_clean_data.py，可上傳 data 的帳號，提供各位進行 data clean 後，一個上傳/分享的管道，這樣就不需要每個人都進行 data clean，合作的概念。程式中提供一個 建立 data file 和上傳 data 的範例。
3. sql.py 提供 python 連接 MYSQL 教學，有中英註解，如果不清楚再 email 詢問我。
4. craw_ptt.py 提供爬取 PTT 文章，並且上傳到 MYSQL code，附上中文註解，不過 code 中並沒有設定密碼，會有 ERROR，帳號密碼請參考 py_connect_sql_example.py。
<br><br>


由於這是我個人架設的平台，資源有限，請不要進行惡意攻擊。另外同一時間使用人數過多，速度上可能會降低，請多包涵。<br><br>
e-mail : samlin266118@gmail.com <br>
連接網址為 : http://114.34.138.146/phpmyadmin/ <br>
user : guest <br>
password : 123 <br>
### PS: 在爬取文章部分，可能出現小錯誤，因此其中一個欄位 origin_article ，提供最原始的 data，如果有錯誤可額外進行提取，基本上99%的資料都是正確的。
<br><br><br><br><br>
歡迎有同樣熱情的朋友協助我，共同合作，由於我是資料分析( 數學系 )出身，並沒有 PHP、SQL 等專業知識，目前只是個雛形，沒有前端，後端部分也只是剛開始，因此需要這方面的夥伴，歡迎 email 討論。未來朝 open 的方向進行，目前資源不足，請多包涵。
<br><br>
<!--匯出請選擇 "test" 樣板，將會匯出所有 data ， csv 檔， big 5 編碼 -->


##  目前已爬超過 130 萬筆 data ( 11GB )，持續更新中<br><br>

|SQL name|中文名|DATA 筆數|other|
|--------|-----|----|-|
|appledaily|蘋果日報|15000|牽扯到著作權問題，已刪除|
|cw_magazine|天下雜誌|40000|牽扯到著作權問題，已刪除|
|ptt_car|PTT 汽車版|73000|爬蟲中|
|ptt_e_shopping|PTT 網路購物版|71000|爬蟲中|
|ptt_Finance|PTT 金融業版|18000|爬蟲中|
|ptt_Food|PTT 食物版|21000|每日更新|
|ptt_happy|PTT 開心版|27000|每日更新|
|ptt_HardwareSale|PTT 硬體買賣版|80000|爬蟲中|
|ptt_Hate|PTT 黑特版|76000|每日更新|
|ptt_HomeTeach|PTT 家教版|27000|每日更新|
|ptt_Japan_Travel|PTT 日本旅遊版|100000|爬蟲中|
|ptt_job|PTT 工作版|7000|每日更新|
|ptt_JOB_Hunting|PTT 工作求職版|20000|每日更新|
|ptt_Lifeismoney|PTT 省錢版|37000|爬蟲中|
|ptt_MacShop|PTT apple產品買賣版|140000|爬蟲中|
|ptt_movie|PTT 電影|111000|每日更新|
|ptt_Oversea_Job|PTT 海外工作版|10000|每日更新|
|ptt_part_time|PTT part time 版|130000|每日更新|
|ptt_prozac|PTT 憂鬱版|8000|爬蟲中|
|ptt_Soft_Job|PTT 軟體工作版|20000|每日更新|
|ptt_Stock|PTT 股票版|68000|爬蟲中|
|ptt_TaiwanJobs|PTT 台灣工作版|6000|每日更新|
|ptt_Tech_Job|PTT 科技工作版|50000|每日更新|
|ptt_toberich|PTT 創業版|24000|爬蟲中|
|ptt_WomenTalk|PTT 女性聊天|100000|爬蟲中|





