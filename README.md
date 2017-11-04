# 共享 data 平台

#### 在資料爆炸的年代，我們卻沒有容易取得 data 的管道，因此提供一個共享 data 的平台，一個人爬蟲力量有限，合作爬蟲力量無限。各位可以在這上面，update 自己爬到的 data ，download 其他人分享的 data。<br>
平台網址：http://114.34.138.146/phpmyadmin/ <br>
每天約新增 15 萬筆 data。最新 data 在 ptt_data1.0 中，目前超過 500 萬筆 ( 36GB )。<br>
本人 10/16 要去當兵了(一年)T.T。該平台會繼續開著，爬蟲方面設定排程繼續進行。issues 方面，會盡可能利用假日回應。<br>

<!--資料科學家是當今最紅的職業，根據 CareerCast.com 網站，2016 best job is data scientist。
問題是，要如何成為資料科學家？資料取得不易，沒資料幾乎不可能成為資料科學家，，，，，，，，， -->

## UPDATE
#### 2017/10/11
1. py_connect_sql_example.py 中，將 origin_data 改為 ptt_data1.0，更改資料庫，origin_data 將不再更新，預計 10 天後，ptt_data1.0 資料量將超越 origin_data。<br>

[history_Update](https://github.com/f496328mm/Crawler_and_Share/blob/master/history_Update.md)<br><br><br><br><br>

<!--
## 2017/10/3 
公開密碼，權限為：可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。-->


## 附件
1. py_connect_sql_example.py，可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。
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


## 目前超過 500 萬筆 data ，持續更新中<br><br>

|SQL name|DATA 筆數|類別|
|--------|----|-|
|AdvEduUK|23,000||
|AllTogether|70,000||
|Aquarius|24,000||
|Aries|25,000||
|Aviation|10||
|BabyMother|123,000||
|BabyProducts|36,000||
|baking|17,000||
|Baseball|115,637||
|biker|10||
|Boy_Girl|68,000||
|Broken_heart|23,300|情感分析|
|BuyTogether|76,500||
|Cancer|24,919||
|Capricornus|22,342||
|car|76,188||
|CarShop|37,476||
|CATCH|24,895||
|cookclub|69,303||
|couple|13,800||
|creditcard|49,000||
|DC_SALE|67,227||
|Diary|27,780||
|DistantLove|20||
|Dreamland|20||
|EngTalk|9,700||
|e_shopping|70,000|購物買賣|
|Finance|19,000||
|Food|124,832||
|forsale|34,454||
|Gemini|7,168||
|GetMarry|73,238||
|give|5||
|Gossiping|507,854|八卦版|
|happy|23,727|情感分析|
|HardwareSale|79,301|購物買賣|
|Hate|74,164|情感分析|
|HatePolitics|76,421||
|HelpBuy|79,927||
|HomeTeach|19|工作相關資訊|
|home_sale|21,565|購物買賣|
|Hsinchu|12,448||
|Japan_Travel|34,463||
|job|8,827|工作相關資訊|
|JOB_Hunting|6,600|工作相關資訊|
|joke|103,333||
|Kaohsiung|77,759||
|Leo|15||
|Libra|18||
|Lifeismoney|20|購物買賣|
|Loan|33,866||
|Lonely|20,359|情感分析|
|love|20,000|情感分析|
|love_vegetal|21,552||
|Lucky|18,000|情感分析|
|MacShop|182,696|購物買賣|
|MakeUp|55,384||
|Marginalman|20|情感分析|
|MenTalk|96,943|聊天機器人|
|MobileComm|107,297|購物買賣|
|mobilesales|298,517||
|movie|114,311||
|NBA|100,919||
|Oversea_Job|10,187|工作相關資訊|
|part_time|132,595|工作相關資訊|
|PC_Shopping|66,728|購物買賣|
|Pisces|20||
|prozac|36,201|情感分析|
|Sad|26,106||
|Sagittarius|19||
|Salary|40,839||
|Sad|26,017|情感分析|
|SayLove|13,000|情感分析|
|Scorpio|20||
|Self_Healin|13,000||
|Soft_Job|20|工作相關資訊|
|SorryPub|18,227|情感分析|
|Stock|20||
|studyabroad|26,846||
|StupidClown|69,742||
|TaichungBun|78,245||
|Tainan|78,067||
|TaiwanJobs|6,376|工作相關資訊|
|talk|66,610|聊天機器人|
|Taurus|20||
|Tech_Job|51,844|工作相關資訊|
|toberich|24,531||
|Virgo|26,282||
|Wanted|41,898||
|WomenTalk|107,236|聊天機器人|
|Zastrology|24,247||




