# -*- coding: utf-8 -*-

"""
修改depth(爬的页数)即可，目前一共236页
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

start_url = 'http://bgm.tv/anime/browser/?sort=rank&page='  #【爬取网页指定】 可根据类型、时间、标签筛选出来的新URL进行筛选，统一加上&page=,作为start_url  
depth = 216    #爬多少页？ 
result = []
result2 = []   

#定义函数-获取网页
def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 30, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)

#定义函数-爬取条目页信息
def parText(result,text):
    name_search = text.find("a", class_='l')
    if name_search:
        name = name_search.get_text()
        rank = text.find("span", class_='rank').get_text()[5:]    #去除 rank四个字符，只留下数字
        mark = text.find("small", class_='fade').get_text()
        count = text.find("span", class_='tip_j').get_text()[1:-4]  #去除括号以及 人评分 这些字符，只留下数字
        info = text.find("p",class_='info tip').get_text().strip()    #番剧的具体信息，会降低爬取速度，不需要时可以去掉
        urla = name_search.get("href")
        url2 = 'http://bgm.tv'+ urla
        result.append((name, rank, mark, count, info, url2))
#        result.append((rank,name,url2))

#定义函数-爬取各内页关键词
def parinText(result1,text1):
#    rank = text1.find("div", class_='global_ratingscore9').find('span',class_='global_score').find('small',class_='alarm').get_text()
    keywords = text1.find("div", class_='subject_tag_section').find('div',class_='inner').find_all('a', class_='l')
    selected_keywords = []
    for keyword in keywords:
        selected_keywords.append(keyword.find('span').get_text())
    result1.extend(selected_keywords)

#主程序，循环
if __name__ == '__main__':
    for count in range(1,depth+1):
        try: #如果某个页面出错则继续爬取下一页
            url = start_url + str(count)
            html = getHtmlText(url)
            soup = BeautifulSoup(html,'html.parser')
            for i in soup.find_all('div', class_='inner'):
                parText(result, i)
#            for j in range(0,3):    #测试用
            for j in range(0,len(result)):
                try:
                    result1 = []
                    url2 = result[j][5]
                    html2 = getHtmlText(url2)
                    soup2 = BeautifulSoup(html2,'html.parser')
                    parinText(result1, soup2)
                    result2.append((result[j][0],result[j][1],result[j][5],result1))
                except Exception as e:
                    print("\r进度:{:2f}%".format(count*100/depth),end="")
                    print()
                    print(str(e))
                    continue
            print("\r进度:{:2f}%".format(count * 100 / depth), end="") #打印进度
        except Exception as e:
            print("\r进度:{:2f}%".format(count*100/depth),end="")
            print()
            print(str(e))
            continue
        time.sleep(15)          #设置休息间隔，防止频繁访问被封ip

#with pd.ExcelWriter('E:\BangumiData.xlsx') as writer:
pd.DataFrame(result, columns=['番剧名称', 'Bangumi排名', '评分', '评分人数','番剧信息', '网址']).to_excel('E:\BangumiData_basic.xlsx',sheet_name = 'Overview', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入txt文件中
pd.DataFrame(result2).to_excel('E:\BangumiData_keywords.xlsx',sheet_name = 'Tag', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入txt文件中