from bs4 import BeautifulSoup
from pandas import Series,DataFrame
import numpy as np
import pandas as pd
import requests

def user_review(movie_id,page):
    url = (f'https://movie.daum.net/moviedb/grade?'
           f'movieId={movie_id}&'
           f'type=netizen&page={page}')
    repsonse = requests.get(url)
    soup = BeautifulSoup(repsonse.text,'html.parser')
    test = soup.select('#mArticle > div.detail_movie.detail_rating > div.movie_detail > div.main_detail > ul>li')
    review_list = []
    for i in range(len(test)):
        nickname = soup.find_all('em',class_='link_profile')
        avg = soup.find_all('em', class_='emph_grade')
        review = soup.find_all('p',class_='desc_review')
        date = soup.find_all('span',class_='info_append')

        re_nickname = nickname[i].text.strip()
        re_avg = avg[i].text.strip()
        re_review = review[i].text.strip()
        re_date = date[i].text.strip()

        user_review = [movie_id,re_nickname,re_avg,re_review,re_date]
        review_list.append(user_review)

    return review_list

# movie_id = 1
# review_page = 12
def all_review(movie_id,review_page):
    
    reviews_content = []
    for i in range(1, review_page):
        for j in user_review(movie_id,i):
            reviews_content.append(j)
            
    user_review_content = pd.DataFrame(reviews_content,
                                      columns=['movie_id'
                                               ,'user_id'
                                               ,'avg'
                                               ,'review_content'
                                               ,'date']
                                      )
    
    return user_review_content

# review_count = pd.read_csv('./review.csv', index_col=0)