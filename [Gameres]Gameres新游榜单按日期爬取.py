# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 21:46:13 2020

@author: Administrator
"""

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
import json
###-----------------------------------

###------------------------------------

#定义函数-获取网页
def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 50,params = data)   # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)

#定义函数-爬取条目页信息
def parText(result,text):
    Title=''
    Type=''
    State=''
    Producer=''
    
    Title_search = text.find("div", class_='item').find('span',class_='titlename')
    if Title_search:
        Title = Title_search.get_text()
    
    Type_search = text.find("div", class_='item').find('div',class_='info_title').find('em')
    if Type_search:
        Type = Type_search.get_text()
    
    State_search = text.find("div", class_='item').find('div',class_='info_title').find('span',class_='mark_tag')
    if State_search:
        State = State_search.get_text()
    
    Producer_search = text.find("div", class_='item').find('div',class_='info_mark').find('div')
    if Producer_search:
        Producer = Producer_search.get_text().strip()
    
    result.append([Time, Title, Type, State, Producer])


#date =['2019-09-01','2019-09-04','2019-09-07','2019-09-10','2019-09-13','2019-09-16','2019-09-19','2019-09-22','2019-09-25','2019-09-28','2019-10-01','2019-10-04','2019-10-07','2019-10-10','2019-10-13','2019-10-16','2019-10-19','2019-10-22','2019-10-25','2019-10-28','2019-11-01','2019-11-04','2019-11-07','2019-11-10','2019-11-13','2019-11-16','2019-11-19','2019-11-22','2019-11-25','2019-11-28','2019-12-01','2019-12-04','2019-12-07','2019-12-10','2019-12-13','2019-12-16','2019-12-19','2019-12-22','2019-12-25','2019-12-28','2020-01-01','2020-01-04','2020-01-07','2020-01-10','2020-01-13','2020-01-16','2020-01-19','2020-01-22','2020-01-25','2020-01-28','2020-02-01','2020-02-04','2020-02-07','2020-02-10','2020-02-13','2020-02-16','2020-02-19','2020-02-22','2020-02-25','2020-02-28','2020-03-02','2020-03-05','2020-03-08','2020-03-11','2020-03-14','2020-03-17','2020-03-25','2020-03-30','2020-04-15','2020-05-15']
date =['2019-10-05'] #需要爬哪些日期？
result = []
url = "https://www.gameres.com/newgame"

#主程序，循环
print(url)
for k in range(0,len(date)):
    data = {'tdate':date[k],'dataType':'fragment'}  #发送参数请求，读取制定日期的数据（showm)
#    html2 = json.loads(getHtmlText(url))
    html = json.loads(getHtmlText(url))['html']    #参数请求返回的json格式，编为字典并提取其中的html字段即可解析
    soup = BeautifulSoup(html,'html.parser')
    for j in soup.find_all('div','one_day_div'):
        Time = ''
        Time = j.get('id')
        for i in j.find_all('a', class_='gamepanel'):
            try:
                parText(result, i)
            except Exception as e:
                print(e)
                continue
    print(k)

pd.DataFrame(result, columns=['所属时间', '游戏名称', '游戏类型', '状态', '制作组']).to_excel('E:\Gameres_Newgame669.xlsx', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入excel文件中