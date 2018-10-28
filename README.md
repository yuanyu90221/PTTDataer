# PTT Open Data ( 維修中 - 轉移 data 至 Linode, 將會在上面架設 MySQL )
 ( 包含 112 個 PTT 版 [click](https://github.com/f496328mm/PTTOpenData/blob/master/ptt_readme.md) ，more than 7 million PTT Data， 50GB SIZE )
<!---
     在資料爆炸的年代，我們卻沒有容易取得 data 的管道，因此提供一個共享 data 的平台。
     一個人爬蟲力量有限，合作爬蟲力量無限。各位可以在這上面，update 自己爬到的 data ，download 其他人分享的 data。

    平台網址：http://http://114.32.60.100/phpmyadmin/ <br>
    user : guest <br>
    password : 123 <br> --->
------------------------------------------------------------
Gmail : samlin266118@gmail.com <br>
 目前在 Linode 上架設 MySQL ，aws 價格太高，linodo 目前方案：4	TB Transfer/month、4000	Mbps Network Out，速度上會大大提升。
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
## Load PTT data download example
[Python](https://github.com/f496328mm/PTTOpenData/blob/master/load_data_from_mysql.py) <br>

    import sys
    sys.path.append('d:/')# windows path
    #sys.path.append('/home/linsam/github')# linux path 
    import PTTOpenData.load_data_from_mysql as ptt

    ptt_table_list = ptt.table_list()
    data_name = 'job'
    # or 
    #data_name = ptt_table_list[0]
    data = ptt.load(data_name)

[R](https://github.com/f496328mm/PTTOpenData/blob/master/load_data_from_mysql.r) <br>    

    source("d:/PTTOpenData/load_data_from_mysql.r")# windows path
    #source("/home/linsam/github/PTTOpenData/load_data_from_mysql.r")# linux path
    ptt_table_list = table_list()
    
    data_name = 'job'
    # or 
    #data_name = ptt_table_list[0]
    data = load_data_from_mysql('job')

------------------------------------------------------------
### Variable Introduction

| variable name | 變數名稱 | example |
|---------------|---------|----------|
| title | 標題 | xxxxx |
| date | 日期 | 2018-06-04 16:31:34 |
| author | 作者 | xxxxx |
| author_ip | 作者IP | xxx.xx.xxx.xx |
| push_amount | 推文數 | 21 |
| boo_amount | 噓文數 | 10 |
| arrow_amount | 箭頭數 | 5 |
| article_url | 文章網址 | https://www.ptt.cc/bbs/Boy-Girl/xxxxxxxxx.html |
| clean_article | clean 後的文章 | xxxxx |
| response | 推/噓文內容(以\n作為分隔符號) | \n推 xxxx: xxxxxx \n噓 xxxxx: xxxxx\n→ xxxx: xxxx  |
| id | index | 1 |

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

