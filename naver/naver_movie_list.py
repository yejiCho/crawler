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
