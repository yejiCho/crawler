from pandas import Series,DataFrame
import pandas as pd
import numpy as np

import glob
import os

file_list = glob.glob('./crawl_daum/*')

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
                                     ,'count_review'
                                    ])
                  )

for file in file_list:
    temp_df = pd.read_csv(file)
    all_df = pd.concat([all_df,temp_df]
                       ,sort=False
                      ,ignore_index=True)

all_df.to_csv('./movieinfo/daum_moviedetail.csv'
              ,index=False
              ,encoding='utf-8')