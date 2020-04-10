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
    
    try:
        driver.find_element_by_xpath('//*[@id="descMoreButton"]').click()
    except:
        pass
    
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

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
# 
        txt = soup.select('div > dl.list_movie.list_main > dd')
        find_txt = soup.find_all("dd",class_=False,id=False)
#         print(find_txt)
        if find_txt:
            if len(find_txt) == 2:
                country = find_txt[0].text.strip().replace("\n","").replace("\t","")
                rating = find_txt[1].text.strip()
            elif len(find_txt) == 1:
                re_txt = find_txt[0].text.strip()
                f_txt = re.findall('\d+', re_txt)
                if f_txt: # f_txt에 숫자가 있을경우
                    rating = f_txt
                    country=""
                else:
                    country = re_txt.replace("\n","").replace("\t","")
                    rating=""
#                     print(country)
#                     현재 상영중인 영화,
            elif len(find_txt) == 3:
                country = find_txt[0].text.strip().replace("\n","").replace("\t","")
                rating = find_txt[1].text.strip()
        else:
            
            country=""
            rating=""
        
        # txt_main : 장르,개봉일
        txt_main = soup.select('div > dl.list_movie.list_main > dd.txt_main')

        if txt_main:
        #     장르,개봉일 다있을경우
            if len(txt_main)==2:
                genres = txt_main[0].text.strip()
                release_date = txt_main[1].text.strip()
                rerelease_date = re.findall('\d+', release_date)
                join_release_date = ".".join(rerelease_date)
        #         장르,개봉일 중 하나만 있을경우
            elif len(txt_main)==1:
                find_what=txt_main[0].text.strip()
                if re.findall('\d+', find_what):
                    release_date = txt_main[0].text.strip()
                    rerelease_date = re.findall('\d+', release_date)
                    join_release_date = ".".join(rerelease_date)
                    genres=""
                else:
                    genres=find_what
                    join_release_date=""
        #             print(genres)
        # 장르,개봉일,재개봉일 있는경우
            elif len(txt_main)>2:
                genres = txt_main[0].text.strip()
                release_date = txt_main[0].text.strip()
                rerelease_date = re.findall('\d+', release_date)
                join_release_date = ".".join(rerelease_date)
        else:
            genres=""
            join_release_date=""
                
        # 배우가 한명, 여러명, 없을경우
        directors = soup.select('div > dl.list_movie.list_main > dd.type_ellipsis')
        if directors:
            re_directors = directors[0].text.replace("\t","").replace("\n","")
            director = re.sub(r'\([^)]*\)',"",re_directors).strip()
        else:
            director=""

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
                                         ,'actor'
                                         ,'story'
                                         ,'review_count'
                                        ])
                      )
    return all_df

movie_len = 140100
file_list = glob.glob('./crawl_daum/*')
pre_count = int(file_list[-1][-10:-4]) if file_list else 70000

if pre_count < movie_len:
    count_list = list(range(pre_count, movie_len,100)) + [movie_len]

    for i in range(len(count_list)):
        print(pre_count)
        df_movie(count_list[i],count_list[i+1]).to_csv('./crawl_daum/%06d.csv'%(count_list[i+1])
                                                       ,encoding='utf-8'
                                                       ,index=False
                                                       )
        pre_count = count_list[i+1]
