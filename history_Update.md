
# history update 歷史更新紀錄

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
1. 新增 R 連接 MySQL 範例。<br>

#### 2017/11/13
1. 目前大部分 data 已爬完，每日會繼續抓新文章。未來將著重在 data clean 上。<br>

#### 2017/10/11
1. py_connect_sql_example.py 中，將 origin_data 改為 ptt_data1.0，更改資料庫，origin_data 將不再更新，預計 10 天後，ptt_data1.0 資料量將超越 origin_data。<br>

#### 2017/10/10
1. 提高爬蟲效率，預計一天新增 10 萬筆( 過去一天 4 萬筆 )。<br>

#### 2017/10/9 
1. 由於 origin_data 中，資料不夠完善，有小缺失，因此我重新爬取 data，放在 ptt_data1.0 中，並加入 guest 讀取權限。<br>
   另外 origin_data 依然會開放，但不進行更新，各位可以先進行 text mining，之後再更改資料庫即可，如有不便請多多包涵。
2. 推文內容部分，如果有興趣，可以由 data 欄位 origin_article 進行 data clean ，額外提取。<br>
   未來我也會進行 data clean，並公開 code 與 data，但是可能需要一段時間，有興趣的朋友可自行嘗試。

#### 2017/10/7 
1. 本人接到兵單，10/16 要去當兵了(一年)T.T。該平台會繼續開著，爬蟲方面設定排程繼續進行。issues 方面，會盡可能利用假日回應。
2. 由於原先提供的 MySQL 網址是免費的，有流量限制，因此將 host 改為我的固定 IP。

#### 2017/10/5 修正
1. 根據 [issues 1](https://github.com/f496328mm/Crawler_and_Share/issues/1)，修正 craw_ptt.py。
2. 在 guest 權限上，加入 guest_dataset 資料庫權限，可供上傳/下載/建立 data table，提供測試、上傳自己爬取的 data。
由於 test data 是做為測試用，我會不定時刪除，如需建立自己的 data，建議使用其他命名。
3. 壞消息，我這網路無法升級到100/100，最高 100/40，我再想想看其他解決方法。

#### 2017/10/4 修正
1. 新增 py_connect_sql_example.py，公開密碼，權限為：可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。
2. 新增 upload_clean_data.py，可上傳 data 的帳號，提供各位進行 data clean 後，一個上傳/分享的管道，這樣就不需要每個人都進行 data clean，合作的概念。程式中提供一個 建立 data file 和上傳 data 的範例。<br>
3. 由於人數過多，速度上偏慢，我目前是光世代100/40，近期會升級成100/100，希望在速度上會有所改善。<br>
4. 最近公開 MySQL，得到許多建議，因此近期會進行小調整。<br>
5. 對於 time 欄位進行以下調整：資料按照時間排序，需要注意的是，前 1 %的文章中，時間特殊，需要另外校正，因此需要多加注意。<br>
