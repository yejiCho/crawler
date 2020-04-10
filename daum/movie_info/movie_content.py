# 해당 movie_id의 영화정보 크롤링

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pandas import Series,DataFrame


import time

path = "C:/Users/user/data_s/chromedriver.exe"
driver = webdriver.Chrome(path)

def movie_content(movie_id):
    url = 'https://movie.daum.net/moviedb/main?'
    driver.get(f'{url}'
              f'movieId={movie_id}')
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    try:
        driver.find_element_by_xpath('//*[@id="descMoreButton"]').click()
    except:
        pass
        
    zulguris = soup.select('#mArticle > div.detail_movie.detail_main')
    
    for zul in zulguris:
        zul = soup.select_one('p').text.strip()
        
    all_content = soup.select('#mArticle > div.detail_movie.detail_main > div.movie_detail > div.movie_basic > div.main_detail > div.detail_summarize')
    
    for movie in all_content:
        
        title = movie.select_one('strong').text
        title_eng = movie.select_one('div > div.subject_movie > span').text.strip()
        avg = movie.select_one('em').text
        genres = movie.select_one('dd').text
    #     run = movie.select('dd')[0].text
        country = movie.select_one('div > dl.list_movie.list_main > dd').text.strip()
        actor = movie.select('div > dl.list_movie.list_main > dd > a')[0].text +',' + movie.select('div > dl.list_movie.list_main > dd > a')[1].text
        director = movie.select('div > dl.list_movie.list_main > dd > a')[1].text       
    
    return [title,title_eng,avg,genres,country,actor,director,zul]

def df_movie(movie_range):
    get_movie_list = []
#     movie_range = 100
    for movie_id in range(movie_range):
        get_movie_list.append(movie_content(movie_id+1))
        
    all_df = DataFrame(get_movie_list
                      ,columns = pd.Index(['title',
                                           'title_eng'
                                           ,
                                           'avg',
                                           'genres',
                                           'country',
                                          'actor',
                                          'director',
                                          'movie_content'
                                          ])
                      )
    movie_id_list = []
    for movie_id in range(movie_range):
        movie_id_list.append(movie_id+1)

    movie_id_list= DataFrame(movie_id_list
                            ,columns= pd.Index(['movie_id'])
                            )
    all_df = pd.concat([movie_id_list,all_df]
                      ,axis=1
                      )
    return all_df

df_movie(100).to_csv('movie_list_range_100.csv',encoding='cp949')