from pandas import Series,DataFrame
import pandas as pd
import numpy as np

from datetime import datetime

import requests
import json
import glob

# api_key = api_key할당

# today_date
today = datetime.today().strftime('%Y-%m-%d')
# today_year
today_year = datetime.today().year

file_list = glob.glob(f'./movies/{today}*')
# file_list
if file_list:
    file_name = file_list[-1][-14:-4]
    today = str(pd.Period(file_name)+1)

def get_today_movielist(key,date):
    url='https://api.themoviedb.org/3/discover/movie'
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

# get_today_movielist(api_key,today)
movie_df = get_today_movielist(api_key,today)
movie_df.to_csv(f'./movies/{today}.csv',
               index=False,
                encoding='utf-8'
               )
for year in np.arange(today_year, today_year+1 ):
    file_sr = Series(glob.glob(f'./movies/{year}*'))

    year_df = DataFrame(
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
    for file in file_sr:
        temp_df = pd.read_csv(file)
        year_df = pd.concat([year_df, temp_df], 
                             sort=False,
                             ignore_index=True)
    
    year_df.to_csv(f'./movies_by_year/{year}.csv',
                   index=False,
                   encoding='utf-8')