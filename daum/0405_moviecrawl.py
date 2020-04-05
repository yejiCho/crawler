from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pandas import Series,DataFrame

import time
import glob
import re

path = "C:/Users/user/data_s/chromedriver.exe"
driver = webdriver.Chrome(path)

def movie_content(movie_id):
    url = 'https://movie.daum.net/moviedb/main?'
    driver.get(f'{url}'
              f'movieId={movie_id+1}')   # 0번째 movie_id는 없으니깐 +1
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    try:
        driver.find_element_by_xpath('//*[@id="descMoreButton"]').click()
    except:
        pass
#     해당 movie_id의 영화정보가 없을 경우
    if soup.select('#dkContent.cont_error'):
        return []  # movie_id의 영화 정보가 없을 경우
    # 줄거리
    stories = soup.select('#mArticle > div.detail_movie.detail_main') 
    for story in stories:
        restory = soup.select_one('p').text.strip()
    all_contents = soup.select('#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize')
    for all_content in all_contents:
        untitle = soup.select_one('div > div.subject_movie > strong').text.strip()
        title = untitle[:-6] # 제목
        title_eng = soup.select('div > div.subject_movie > span.txt_origin')[0].text.strip() # 영어제목
        grade = soup.select('div > div.subject_movie > a > em')[0].text.strip() # 평점
        ungenres =soup.select('div > dl.list_movie.list_main > dd.txt_main') # 장르
        if len(ungenres) == 2:
            genres=ungenres[0].text.strip()
        else:
            genres=""
        uncountry = soup.select('div > dl.list_movie.list_main > dd')
        if len(uncountry) == 6: # 나라
            country = uncountry[1].text.strip().replace("\t","").replace("\n","")
        else:
            country=""
        unrelease_date =soup.select('div > dl.list_movie.list_main > dd.txt_main') # 개봉일
#         print(unrelease_date)
        if len(unrelease_date) == 1:
            join_release_date = ''
        elif len(unrelease_date) > 1:
            nrelease_date = unrelease_date[-1].text.strip()
            rerelease_date = re.findall('\d+', nrelease_date)
            join_release_date = ".".join(rerelease_date)
        else:
            join_release_date = ""
        unrating = soup.select('div > dl.list_movie.list_main > dd')
        if len(unrating) == 6:      # 영화정보 : 상영등급
            rating = unrating[3].text.strip()
        else:
            rating=""
    # 배우가 한명, 여러명, 없을경우
    directors = soup.select('#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize > div > dl.list_movie.list_main > dd.type_ellipsis')
    re_directors = directors[0].text.replace("\t","").replace("\n","")
    director = re.sub(r'\([^)]*\)',"",re_directors).strip()
    if len(directors) == 2:
        actors = directors[1].text.replace("\t","").replace("\n","")
        actor = re.sub(r'\([^)]*\)',"",actors).strip()
    elif len(directors) == 1:
        actor=""
    else:
        actor=""
    unreview = soup.select('#mainGradeDiv')
    for review in unreview:
        review_counts=soup.select('span.num_review')
#         print(review_counts)
        if review_counts:
            review_count = review_counts[0].text.strip()
            rereview_count = re.findall('\d+', review_count)[0]
        else:
            rereview_count=""
        
    return [movie_id+1,title,title_eng,grade,genres,country,join_release_date,rating,director,actor,restory,rereview_count]

def df_movie(movie_last,movie_range):
    get_movie_list = []
#     random.seed(1)
    for movie_id in range(movie_last,movie_range):
#         movie_content(movie_id+1)안이 True 값이 있을경우에만 생성
        if movie_content(movie_id):
            get_movie_list.append(movie_content(movie_id))

    all_df = DataFrame(get_movie_list,
                      columns= pd.Index(['movie_id'
                                         ,'title'
                                         ,'title_eng'
                                         ,'grade'
                                         ,'genres'
                                         ,'country'
                                         ,'release_date'
                                         ,'rating'
                                         ,'director'
                                         ,'actory'
                                         ,'story'
                                         ,'review_count'
                                        ])
                      )
    return all_df

movie_len = 20000  # movie_id 마지막값 지정
file_list = glob.glob('./crawl_daum/*')  # 파일저장위치
pre_count = int(file_list[-1][-10:-4]) if file_list else 10000

if pre_count < movie_len:
    count_list = list(range(pre_count, movie_len,100)) + [movie_len]
    try:
        for i in range(len(count_list)):
            print(pre_count)
            df_movie(count_list[i],count_list[i+1]).to_csv('./crawl_daum/%06d.csv'%(count_list[i+1])
                                                           ,encoding='utf-8'
                                                           ,index=False
                                                           )
            pre_count = count_list[i+1]
    except IndexError:
        print("실패")