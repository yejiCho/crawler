import requests
from bs4 import BeautifulSoup

data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=20200322')

soup = BeautifulSoup(data.text,'html.parser')

f = open('test.csv', 'w')
f.write("순위,영화제목,평점\n")

movies = soup.select('#old_content > table > tbody > tr')

rank = 0
for movie in movies:

    if not movie.a == None:
        rank = rank + 1
        title = movie.a.text
        start = movie.select('td.point')[0].text
        # print(movie.a.text)
        print(rank,title,start)
        f.write(str(rank)+","+title+","+start+"\n")

f.close()

import pandas as pd
import requests
from bs4 import BeautifulSoup

data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=20200322')

soup = BeautifulSoup(data.text,'html.parser')

# f = open('test.csv',"w")
# f.write("순위,영화제목, 평점\n")

# 여러개를 가져오고 싶은 경우
# soup.select('태그명')
# soup.select('.클래스명')
# soup.select('#아이디명')
#
# soup.select('상위태그명 > 하위태그명 > 하위태그명')
# soup.select('상위태그명.클래스명 > 하위태그명.클래스명')
# 한개만 가져오고 싶은 경우
# soup.select_one('위와동일')

movies = soup.select('#old_content > table > tbody > tr')

results = []
result = []
rank = 0
for movie in movies:
    if not movie.a == None:      
        rank = rank + 1
        title = movie.a.text
        start = movie.select('td.point')[0].text
        results = [rank,title,start]
#         results.append(rank,title,start)
        # print(movie.a.text)
#         print(rank,title,start)
#         f.write(str(rank)+","+title+","+start+"\n")

# f.close()
        result.append(results)
#         print(results)
# print(result)
data = pd.DataFrame(result
                   ,columns=['index','movie','avg'])
# 웹 데이터나 파이썬은 utf-8이 기본, MSoffice 에서는 cp949, euc-kr
# data.to_csv('test.csv',encoding='utf-8')
data.to_csv('test.csv',encoding='cp949')