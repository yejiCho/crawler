from pandas import Series,DataFrame
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import glob,re
import os

file_list = glob.glob('./daum/*')
# file_list

all_df = DataFrame(columns=pd.Index(['movie_id'
                                     ,'title'
                                     ,'title_eng'
                                     ,'grade'
                                     ,'country'
                                     ,'release_date'
                                     ,'rating'
                                     ,'director'
                                     ,'actor'
                                     ,'story'
                                     ,'review_count'
                                    ])
                  )

for file in file_list:
    temp_df = pd.read_csv(file)
    all_df = pd.concat([all_df,temp_df]
                       ,sort=False
                      ,ignore_index=True)

all_df.to_csv('./movieinfo/movie_info_all.csv'
              ,index=False
              ,encoding='utf-8')

test = pd.read_csv('./movieinfo/daum_moviedetail.csv')

review = test[test['review_count']!=0]

find_review = review[review['review_count'].notnull()]

movie_ = find_review[['movie_id','review_count']]
# movie_
nan_review  = review[review['review_count'].isnull()]

review_list = []
for i in sorted(nan_review['movie_id']):
#     print(i)
    url = f'https://movie.daum.net/moviedb/grade?movieId={i}&type=netizen&page=1'
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    # soup
    review_count =soup.find('span',class_='txt_menu').text.strip()
    count = "".join(re.findall('\d+',review_count))
#     print(count)
    if count == '0':
        continue
    review_list.append([i,count])
    print(review_list)

movie_list = pd.DataFrame(review_list
                          ,columns=['movie_id','review_count'])

all_df = DataFrame(columns=pd.Index(['movie_id'
                                     ,'review_count'
                                    ])
                  )

all_df = pd.concat([movie_,movie_list]
                   ,sort=False
                  ,ignore_index=True)

all_df.to_csv('review.csv',encoding='utf-8')