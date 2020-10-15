# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:10:45 2020

@author: liuwp
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import json
###修改日期和数据时长-----------------------------------
t_str ='2020-06-01' #起始日期
l = 50 #数据时长，覆盖3k天 
###----------------------------------------------------

#日期

datelist=[]
d = datetime.datetime.strptime(t_str,'%Y-%m-%d')
delta = datetime.timedelta(days=3)
datelist.append(d)
for i in range(0,l):   
    d=d+delta
    datelist.append(d)


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

result = []
url = "https://www.gameres.com/newgame"

#主程序，循环
print(url)
for k in range(0,len(datelist)):
    data = {'tdate':datelist[k],'dataType':'fragment'}  #发送参数请求，读取制定日期的数据（showm)
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

pd.DataFrame(result, columns=['所属时间', '游戏名称', '游戏类型', '状态', '制作组']).to_excel('E:\Gameres_Newgame927.xlsx', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入excel文件中
