# coding=utf-8
# 爬虫demo，爬取豆瓣top 250 电影信息

import requests
from bs4 import BeautifulSoup
import time
import random

# 将结果输出到top250.txt
file = open('top250.txt', 'w', encoding='utf-8')

# 构造请求头，模拟浏览器访问
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                         'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
# 电影排行序号
rank = 1


# 获取某一部电影的具体信息并打印
def getInfo(url):
    global rank

    # 随机睡眠1——3s防止反爬
    time.sleep(random.randint(1, 3))

    # 获取片名、简介、评分、imdb链接、豆瓣链接
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    title = soup.select('#content > h1 > span:nth-child(1)')[0].get_text()
    imdb_link = soup.select('#info > a')[0].get('href')
    score = soup.select('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong')[0].get_text()
    span = soup.select('#link-report > span.all.hidden')
    if len(span) == 0:
        span = soup.select('#link-report > span:nth-child(1)')
    introduct = span[0].get_text(strip=True)

    # 打印相关信息
    file.write(str(rank) + '、片名：' + title + '\n')
    file.write('评分：' + score + '\n')
    file.write('简介：' + introduct + '\n')
    file.write('IMDB链接：' + imdb_link + '\n')
    file.write('豆瓣链接：' + url + '\n\n')
    rank = rank + 1
    print(title)


# 爬取250部电影链接
def main():
    # 构造10页请求链接
    url = 'https://movie.douban.com/top250?start='
    prefix = '&filter='

    for i in range(0, 226, 25):
        # 随机睡眠1——3s防止反爬
        time.sleep(random.randint(1, 3))

        # 发起请求并获取影片链接
        html = requests.get(url + str(i) + prefix, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        href = soup.select('#content > div > div.article > ol > li > div > div.info > div.hd > a')
        for element in href:
            getInfo(element.get('href'))


if __name__ == '__main__':
    main()
    file.close()
