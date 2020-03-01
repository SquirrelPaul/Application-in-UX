#导入库
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# 修改以下参数即可直接运行（用【】表示）  
GameNumber = 137744      ##【游戏编号】TAPTAP对应的游戏编号，例如山海镜花是137744
CommentPage = 3     ##【爬取页数】一共需要获取多少页评论，一页有20个评论
CommentOrder = 'update'  ##【排列顺序】TAPTAP评论排序，有update/hot/spent三种属性，分别对应 按时间排序/按热度排序/按游戏时长排序
SaveAddress = 'E:/137744.csv'  ##【保存地址】存在哪里，以csv结尾

## 混合方法——正则表达式+直接搜标签

#定义函数1：获取网页
def getHtmlText(url):                                 
    try:
        r = requests.get(url,timeout = 30, )
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print("Error")

#定义函数2：用标签获取用户名、评分、评论
def parText(result,text):                             
    name_search = text.find("span", class_='taptap-user').get_text().strip()
    score = int(int(text.find("div", class_='item-text-score').find("i", class_='colored').get("style")[-4:-2])//14)
    comment = text.find("div", class_='item-text-body').get_text().strip()
    result.append((name_search, score, comment))

#定义函数3：正则表达式获取评论时间
def get_comment_date(soup):                           
    comment_header = soup.select(".review-item-text .item-text-header")
    pattern_date='data-dynamic-time=".*?">(.*?)</span>'                    
    date=re.findall(pattern_date, str(comment_header), re.S)              
    return date

#主程序
if __name__ == '__main__':
    url1 = 'https://www.taptap.com/app/'
    url2 = '/review?order='
    url3 = '&page='
    url4 = '#review-list'
    result1 = []
    for count in range(1,CommentPage+1):
        try:  # 如果某个页面出错则继续爬取下一页
            result = []
            date_out = []
            url = url1 + str(GameNumber) + url2 + str(CommentOrder) + url3 +str(count) + url4        #网址拼接
            html = getHtmlText(url)              #调用函数1获取网页
            soup = BeautifulSoup(html, 'html.parser')
            date_tmp=get_comment_date(soup)  #调用函数3获取评论时间
            date_out.extend(date_tmp)
            for i in soup.find_all('div', class_='review-item-text'):              #调用函数2获取用户名、评分、评论
                parText(result, i)
                print("\r进度:{:2f}%".format(count * 100 / CommentPage), end="") #打印进度
            for j in range(len(date_out)):
                    result1.append([result[j][0],date_out[j],result[j][1],result[j][2]])  #字段拼接并排序
        except Exception as e:
            print("\r进度:{:2f}%".format(count*100/CommentPage),end="")
            print()
            print(str(e))
            
pd.DataFrame(result1, columns=['用户名','评论时间', '评分值', '评论']).to_csv(SaveAddress, index=None, encoding='utf-8')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入csv文件中



