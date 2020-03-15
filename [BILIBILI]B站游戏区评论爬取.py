# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 21:28:52 2020

@author: SquirrelPaul

BiliBili游戏区评论爬取（直接调用API）
"""


import requests
import pandas as pd
import json

# 修改以下参数即可直接运行
page = 160 #爬多少页评论？一页10条
result=[]
url1 = "https://line1-h5-pc-api.biligame.com/game/comment/page?game_base_id=102601&rank_type=3&page_num="
url2 = "&page_size=10&_=1584192180902"        #这个地址从指定游戏的评论界面的network-page?这里获取，目前是山海镜花对应的API地址

def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 50,params = data)   # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)

def getitem(result,text):
    Account = text.get('user_name')
    Accountlevel = text.get('user_level')
    Comment = text.get('content')
    Time = text.get('publish_time')
    Grade = text.get('grade')    
    result.append([Account, Accountlevel, Time, Grade, Comment])

#主程序
for k in range(1,page): 
    data = {'page_number':k,'page_size':'10','page_count':'160'}      #参数在page?文件里
    url = url1+str(k)+url2
    html = json.loads(getHtmlText(url))['data']['list']
    for j in range(0,len(html)):
        text1 = html[j]
        getitem(result,text1)
    print("\r进度:{:2f}%".format(k * 100 / page))
pd.DataFrame(result, columns=['B站账号名', '账号B站等级', '评论时间', '打分','评论内容']).to_excel('E:\BilibiliComments0314.xlsx', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入excel文件中