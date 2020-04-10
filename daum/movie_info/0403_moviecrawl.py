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
              f'movieId={movie_id}')
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
#     '더보기'버튼이 없을 경우 예외처리
    try:
        driver.find_element_by_xpath('//*[@id="descMoreButton"]').click()
        time.sleep(1)
    except:
        pass
#     해당 movie_id에 영화가 없을 경우 예외처리
    try:
        zulguris = soup.select('#mArticle > div.detail_movie.detail_main')

        for zul in zulguris:
            zul = soup.select_one('p').text.strip()

        all_content = soup.select('#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize') 
        try:
            review_count= soup.select_one('#mainGradeDiv > h4.tit_rating > span.num_review')
            review_count=review_count.text
            reviews = re.findall("\d+",review_count)[0]
        except:
            review_count=soup.select_one('#mainGradeDiv > ul.list_rating.list_step2 > li.on > a > span.num_review')
            review_count=review_count.text
            reviews = re.findall("\d+",review_count)[0]
        for movie in all_content:
            title = movie.select_one('strong').text
            title_eng = movie.select_one('div > div.subject_movie > span').text.strip()
            avg = movie.select_one('em').text
            genres = movie.select_one('dd').text
            country = movie.select_one('div > dl.list_movie.list_main>dd:nth-child(3)').text.strip().replace("\t","")
#             review_count = movie.select_one('#mainGradeDiv > h4.tit_rating > span.num_review').text
            try:
                actor = movie.select('div > dl.list_movie.list_main > dd > a')[1].text # +',' + movie.select('div > dl.list_movie.list_main > dd > a')[2].text
            except IndexError:
                actor=''
            director = movie.select_one('div > dl.list_movie.list_main > dd > a').text
            return [movie_id,title[:-7],title_eng,avg,genres,country,actor,director,reviews,zul]
#     UnboundLocalError, AttributeError
    except:
        pass

def df_movie(movie_last,movie_range):
    get_movie_list = []
#     random.seed(1)
    for movie_id in range(movie_last,movie_range):
#         movie_content(movie_id+1)안이 True 값이 있을경우에만 생성
        if movie_content(movie_id+1):
            get_movie_list.append(movie_content(movie_id+1))

    all_df = DataFrame(get_movie_list,
                      columns= pd.Index(['movie_id'
                                         ,'title'
                                         ,'title_eng'
                                         ,'avg'
                                         ,'genres'
                                         ,'country'
                                         ,'actor'
                                         ,'director'
                                         ,'review_count'
                                         ,'movie_content'
                                        ])
                      )
    return all_df

movie_len = 1000
file_list = glob.glob('./crawl_daum/*')
pre_count = int(file_list[-1][-10:-4]) if file_list else 0

# pd.read_csv(f'./crawl_daum/{movie_id}.csv')
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
        pass
