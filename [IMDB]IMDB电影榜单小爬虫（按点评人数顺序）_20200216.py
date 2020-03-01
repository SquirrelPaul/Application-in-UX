# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import traceback
###-----------------------------------
startyear = 1950   #从第几年开始爬??
endyear = startyear + 20
start_url = 'https://www.imdb.com/search/title/?title_type=tv_movie&release_date=' 
url3 = '&sort=num_votes,desc&start='
end_url = '&ref_=adv_prv'
years = 1        #爬多少年？
depth = 200    #爬多少页？一次不能爬超过1w条，url规则将在1w条后变化。
result = []
result2 = []   
###------------------------------------

#定义函数-获取网页
def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 200, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'})
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)

#定义函数-爬取条目页信息
def parText(result,text):
    name=''
    rank=''
    time1=''
    genre=''
    grade=''
    people=''
    creator=''
    runtime=''
    name_search = text.find("h3", class_='lister-item-header').find('a')
    if name_search:
        name = name_search.get_text()
        rank = text.find("span", class_='lister-item-index unbold text-primary').get_text() 
        time1 = text.find("span", class_='lister-item-year text-muted unbold').get_text()
        
    genre_search = text.find('p',class_='text-muted').find("span", class_='genre')
    if genre_search:
        genre = genre_search.get_text().strip()
        
    grade_search = text.find('div',class_='ratings-bar').find('div',class_='inline-block ratings-imdb-rating')
    if grade_search:
        grade = grade_search.find('strong').get_text() 
        people = text.find('p',class_='sort-num_votes-visible').find('span', attrs={'name':'nv'}).get_text()

    creator_search = text.find('p',class_='')
    if creator_search:
        creator = text.find('p',class_='').get_text().replace(' ', '')
        creator = creator.replace('\n','')

        
    runtime_search = text.find('p',class_='text-muted').find('span',class_='runtime')
    if runtime_search:
        runtime = runtime_search.get_text()
        
    result.append((rank, name, runtime, time1, genre, (creator), grade, people))


#主程序，循环
for j in range(0,years) :
    startyear = startyear + j
    endyear = endyear + j
    url2 = str(startyear) + '-01-01,'+ str(endyear) + '-01-01'         #'2000-01-01,2020-01-01'
    for count in range(0,depth):
        try: #如果某个页面出错则继续爬取下一页
            count2 = 50*count + 1
            url = start_url + url2 + url3 + str(count2)+ end_url
            print(url)
            html = getHtmlText(url)
            soup = BeautifulSoup(html,'html.parser')
            if soup.find_all('div', class_='lister-item-content'):
                for i in soup.find_all('div', class_='lister-item-content'):
                    try:
                        parText(result, i)
                    except Exception as e:
                        print(e)
                        continue
            else:
                break
            print("\r进度:{:2f}%".format((count+1) * 100 / depth), end="") #打印进度
        except Exception as e:
            print("\r进度:{:2f}%".format(count*100/depth),end="")
            print()
            print(str(e))
            continue
        time.sleep(10)          #设置休息间隔，防止频繁访问被封ip

#with pd.ExcelWriter('E:\BangumiData.xlsx') as writer:
pd.DataFrame(result, columns=['序号','电影名称','电影时长', '上映时间', '类型','导演及演员', '评分','评分人数']).to_excel('E:\IMDB_5070years.xlsx', index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入txt文件中