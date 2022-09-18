# Dcard_scraper
Dcard爬蟲相關

### download_image(下載圖片)
透過Api下載Dcard各版(需指定)圖片及影片

使用套件:
cloudscraper, fake_useragent

使用方法:
修改下列變數值
```
board  #想爬取的版名
articles  #一次請求幾篇文章，最大為100，值越大越容易失敗
pages     #要讓迴圈跑幾次
```
