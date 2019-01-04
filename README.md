# PTT Data 
 ( 包含 109 個 PTT 版 [click](https://github.com/f496328mm/PTTOpenData/blob/master/ptt_readme.md) ，more than 7 million PTT Data )
<!---
     在資料爆炸的年代，我們卻沒有容易取得 data 的管道，因此提供一個共享 data 的平台。
     一個人爬蟲力量有限，合作爬蟲力量無限。各位可以在這上面，update 自己爬到的 data ，download 其他人分享的 data。

    平台網址：http://http://114.32.60.100/phpmyadmin/ <br>
    user : guest <br>
    password : 123 <br>
------------------------------------------------------------
Gmail : samlin266118@gmail.com <br>
 1. 目前在 Linode 上架設 MySQL ，aws 價格太高，linodo 目前方案：4	TB Transfer/month、4000	Mbps Network Out，速度上會大大提升。
 2. 為了減少雲端硬碟用量($$$)，將 origin_article 刪除，clean_article 改為 airtcle。
  --->
  ----------------------
  #### 新增 article_type 變數。( e.g 發問、心得、求助、情報... )
  ----------------------
<!--
## install 
 ### linux
    sudo apt install awscli
    aws configure
    aws_access_key_id = email to me
    aws_secret_access_key = email to me
    Default region name [None]: enter
    Default output format [None]: enter
 ### windows
    pip install awscli
    aws configure
    aws_access_key_id = email to me
    aws_secret_access_key = email to me
    Default region name [None]: enter
    Default output format [None]: enter
-->
## Load example
[Python](https://github.com/linsamtw/PTTOpenData/blob/master/LoadData.py) <br>

[R](https://github.com/linsamtw/PTTOpenData/blob/master/LoadData.r) <br>    

------------------------------------------------------------
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

<!---下載 data 範例 
[Python](https://github.com/f496328mm/Crawler_and_Share/blob/master/load_data_from_mysql.py) 
[R](https://github.com/f496328mm/Crawler_and_Share/blob/master/load_data_from_mysql.r)  <br>
上傳 data 範例 
[Python](https://github.com/f496328mm/Crawler_and_Share/blob/master/upload_data_to_mysql.py)
[R](https://github.com/f496328mm/Crawler_and_Share/blob/master/upload_data_to_mysql.r)  <br>
--->
------------------------------------------------------------
    如想分析的 ptt 文章，我沒爬取，麻煩留言在 issues 。
------------------------------------------------------------

<!---
由於這是我個人架設的平台，資源有限，請不要進行惡意攻擊。另外同一時間使用人數過多，速度上可能會降低，請多包涵。<br><br>
歡迎有同樣熱情的朋友協助我，共同合作，由於我是數學系出身，並沒有 PHP、SQL 等專業知識，目前只是個雛形，沒有前端，後端部分也只是剛開始，因此需要這方面的協助，歡迎 email 討論。未來朝 open 的方向進行，目前資源不足，請多包涵。
<br><br>

### PS: 在爬取文章部分，可能出現小錯誤，因此其中一個欄位 origin_article ，提供最原始的 data，如果有錯誤可額外進行提取，基本上99%的資料都是正確的。
<br><br>
--->

