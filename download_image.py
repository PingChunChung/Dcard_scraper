# 解析網頁
import requests as req
import json
from bs4 import BeautifulSoup as bs

# 防止被擋下
import cloudscraper
from fake_useragent import UserAgent

# 睡眠用
from time import sleep
from random import randint

# 建資料夾
import os

# 正規表達式
import re 



ua = UserAgent(cache = True)

my_headers = {
    'user-agent' : ua.random
    }

my_cookies = {
    '__cfruid':'526e8a3666c94a7da2335c462f8fb509bf381305',
    'cf_chl_rc_m':'1',
    '_cfuvid':'lDaoC_62jmMqKfbz',
    'cf_clearance':'ru.QBUcEg22HOQKJDtCwdD4aynIe2zBUCvrI1_t8Ymw',
    'dcsrd':'9V8Tstv5Vm0yFGx0kRYL85aq',
    'cf_chl_2':'66db26ddd8d85a0',
    'cf_chl_prog':'x10'
    
    }

# 要搜尋的版
board = 'pet'

# 建立資料夾
file_path = f'{board}'
if not os.path.exists(file_path):
    os.makedirs(file_path)
    


articles = 100   #一頁幾篇文章
pages = 15       #要爬幾次
page_attr = ''  #api最後一篇文章的元素
ids = []        # 儲存文章的id
img_urls = {}   # 儲存圖片url

#取得文章url
for page in range(pages): 
    try:
        url = f'https://www.dcard.tw/service/api/v2/forums/{board}/posts?popular=false&limit={articles}' + page_attr 

        new_body = cloudscraper.create_scraper().get(url, cookies=my_cookies)
        print(new_body.status_code)

        obj = json.loads(new_body.text)
        
        ids = []
        for i in range(0,articles):
            ids.append(obj[i]['id'])
        
        page_attr = f'&before={ids[-1]}'
        sleep(randint(1,5))
    
    except Exception:
        sleep(randint(1,5))
        continue


    for i in range(len(ids)):
        mediaMetas = obj[i]['mediaMeta']
        for j in range(len(mediaMetas)):
            if mediaMetas[j]['id'] not in img_urls:
                img_urls.update({mediaMetas[j]['id']:mediaMetas[j]['url']})



# 存文章網址
with open(f'{file_path}\img_urls.txt', 'a', encoding = 'utf-8') as file:
    for link in img_urls.values():
        file.write(link + '\n')
    

# 檔案名
regex01 = r'(?<![a-zA-Z0-9])[A-Za-z0-9]{8}(?![a-zA-Z0-9])'
regex02 = r'(?<![a-zA-Z0-9])[A-Za-z0-9]{7}(?![a-zA-Z0-9])'

# 儲存檔案
for link in img_urls.values():
    try:
        if 'images' in link:
            with open(f'{file_path}\{re.search(regex01, link)[0]}.png', 'wb') as f:
                f.write(req.get(link).content)
        # 把yotube的連結排除
        elif 'youtu' in link:
            continue
        # 儲存圖片
        elif link[-3:] == 'png' or 'jpg' or 'peg':
            with open(f'{file_path}\{re.search(regex01, link)[0]}.png', 'wb') as f:
                f.write(req.get(link).content)
                
        #儲存影片
        elif 'videos' in link:   
            with open(f'{file_path}\{re.search(regex01, link)[0]}.mp4', 'wb') as f:
                res_video = req.get(link)
                soup = bs(res_video.text, 'lxml')
                url_video = soup.select_one('video#dc_player_html5_api source')['src']
                f.write(req.get(url_video).content)
        else:
            continue
                
    except Exception: # 有些圖只有7碼，避免存檔時錯誤
        with open(f'{file_path}\{re.search(regex02, link)[0]}.png', 'wb') as f:
            f.write(req.get(link).content)
        continue