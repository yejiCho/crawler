# crawling tmdb movielist openAPI

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from datetime import datetime

import requests
import json
import glob

# api_key = '<<input_api>>'

count_days = 364
start_date = '2016-01-01'
end_date = str(pd.Period(start_date) + count_days)

file_list = glob.glob('./movies/*')
if file_list:
    file_name = file_list[-1][-14:-4]
    start_date = str(pd.Period(file_name) + 1)
    end_date = str(pd.Period(start_date) + count_days)

url = 'https://api.themoviedb.org/3/discover/movie'
date = '2020-03-27'
# urls = (
#     f'{url}?'
#     f'api_key={api_key}&'
#     f'language=ko-KR&'
#     f'primary_release_date.gte={date}&'
#     f'primary_release_date.lte={date}'
# )
# urls
def get_movielist(key, date):
    url = 'https://api.themoviedb.org/3/discover/movie'
    response = requests.get(
        f'{url}?'
        f'api_key={api_key}&'
        f'language=ko-KR&'
        f'primary_release_date.gte={date}&'
        f'primary_release_date.lte={date}'
    )
    
    total_pages = json.loads(response.text)['total_pages']
    all_df = DataFrame(
        columns=pd.Index([
                    'id', 'original_title',
                    'title', 'original_language',
                    'release_date', 'genre_ids',
                    'adult', 'overview',
                    'popularity', 'vote_count',
                    'vote_average', 'video',
                    'poster_path', 'backdrop_path'
                ])
    )    
    for page in np.arange(1, total_pages+1):
        response = requests.get(
            f'{url}?'
            f'api_key={api_key}&'
            f'language=ko-KR&'
            f'sort_by=popularity.desc&'
            f'primary_release_date.gte={date}&'
            f'primary_release_date.lte={date}&'
            f'page={page}'
        )
        data_json = json.loads(response.text)['results']
        for i, data in enumerate(data_json):
            if not data:
                del data_json[i]

        data_df = DataFrame(data_json)
        all_df = pd.concat(
            [all_df, data_df], 
            sort=False, 
            ignore_index=True
        )
    
    return all_df

for date in pd.period_range(today,today):
    movie_df = get_movielist(api_key, date)
    movie_df.to_csv(f'./movies/{date}.csv', 
                    index=False, 
                    encoding='utf-8')

