
# history update 歷史更新紀錄

## 2017/10/5 修正
1. 根據 [issues 1](https://github.com/f496328mm/Crawler_and_Share/issues/1)，修正 craw_ptt.py。
2. 在 guest 權限上，加入 guest_dataset 資料庫權限，可供上傳/下載/建立 data table，提供測試、上傳自己爬取的 data。
3. 壞消息，我這網路無法升級到100/100，最高 100/40，我再想想看其他解決方法。

## 2017/10/4 修正
1. 新增 py_connect_sql_example.py，公開密碼，權限為：可自由取得 SQL 中的 data，該程式中已將格式轉為 dataframe ，利於分析。
2. 新增 upload_clean_data.py，可上傳 data 的帳號，提供各位進行 data clean 後，一個上傳/分享的管道，這樣就不需要每個人都進行 data clean，合作的概念。程式中提供一個 建立 data file 和上傳 data 的範例。<br>
3. 由於人數過多，速度上偏慢，我目前是光世代100/40，近期會升級成100/100，希望在速度上會有所改善。<br>
4. 最近公開 MySQL，得到許多建議，因此近期會進行小調整。<br>
5. 對於 time 欄位進行以下調整：資料按照時間排序，需要注意的是，前 1 %的文章中，時間特殊，需要另外校正，因此需要多加注意。<br>
