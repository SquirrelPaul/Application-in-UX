# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 16:00:44 2020

@author: liuwp

MyanimeList scramper
"""

# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
###-----------------------------------

###------------------------------------

#定义函数-获取网页
def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 50)   # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)

#定义函数-爬取条目页信息
def parText(result,text):
    rank=''
    Animename=''
    Animeinfo=''
    AnimeGrade=''
    
    name_search = text.find("div", class_='detail').find('div',class_='di-ib clearfix')
    if name_search:
        Animename = name_search.get_text()
        rank = text.find("td", class_='rank ac').get_text() 
    
    Animeinfo_search = text.find("div", class_='detail').find('div',class_='information di-ib mt4')
    if Animeinfo_search:
        Animeinfo = Animeinfo_search.get_text().replace(' ','')
        Animeinfo = Animeinfo.replace('\n','&')[1:-1]
    
    AnimeGrade_search = text.find("td",class_='score ac fs14')
    if AnimeGrade_search:
        AnimeGrade = AnimeGrade_search.find("span",class_='text on').get_text()
    
    result.append((rank, Animename, (Animeinfo), AnimeGrade))

pages = 200
result = []
url0 = "https://myanimelist.net/topanime.php?limit="
url = ""
#主程序，循环
for j in range(0,pages) :
    try:
        limit = 50*j
        url = url0 + str(limit)
        print(url)
        html = getHtmlText(url)
        soup = BeautifulSoup(html,'html.parser')
        for i in soup.find_all('tr', class_='ranking-list'):
            try:
                parText(result, i)
            except Exception as e:
                print(e)
                continue
        print("\r进度:{:2f}%".format((j+1) * 100 / pages), end="") #打印进度
    except Exception as e:
        print("\r进度:{:2f}%".format((j+1)*100 / pages),end="")
        print()
        print(str(e))
        continue
    time.sleep(2)          #设置休息间隔，防止频繁访问被封ip
    
#with pd.ExcelWriter('E:\BangumiData.xlsx') as writer:
pd.DataFrame(result, columns=['序号','动漫名称','动漫信息', '动漫评分']).to_excel('E:\MAL2020.xlsx', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入txt文件中