from bs4 import BeautifulSoup
import requests

from pandas import Series,DataFrame
import numpy as np
import pandas as pd

def user_review(movie_id,page):
    url = f'https://movie.daum.net/moviedb/grade?movieId={movie_id}&type=netizen&page={page}'
    repsonse = requests.get(url)
    html = repsonse.text
    soup = BeautifulSoup(html,'html.parser')
    review_list = soup.select('#mArticle > div.detail_movie.detail_rating > div.movie_detail > div.main_detail > ul>li')

    if len(review_list) == 10:
        nickname = soup.select('li> div > a.link_review.\#grade.\#netizen.\#name > em')
        avg = soup.select('li > div > div.raking_grade > em')
        review = soup.select('li > div > p')
        date = soup.select('li > div > div.append_review > span.info_append')
        user_reviews=[]
        user_review=[]
        for i in range(10):
            user_id=nickname[i].text.strip()
            avgs=avg[i].text.strip()
            reviews=review[i].text.strip()
            dates=date[i].text.strip()
            user_review=[user_id,avgs,reviews,dates]
            user_reviews.append(user_review)
        user_review_content = pd.DataFrame(user_reviews,
                                          columns=['user_id'
                                                   ,'avg'
                                                   ,'review_content'
                                                   ,'date']
                                          )
    if len(review_list)<10:
        nickname = soup.select('li> div > a.link_review.\#grade.\#netizen.\#name > em')
        avg = soup.select('li > div > div.raking_grade > em')
        review = soup.select('li > div > p')
        date = soup.select('li > div > div.append_review > span.info_append')
        user_reviews=[]
        user_review=[]
        for i in range(len(review_list)):
            user_id=nickname[i].text.strip()
            avgs=avg[i].text.strip()
            reviews=review[i].text.strip()
            dates=date[i].text.strip()
            user_review=[user_id,avgs,reviews,dates]
            user_reviews.append(user_review)
    #             print(user_reviews)


# user_review_content
# len(review_list)
    
    return user_reviews

# movie_id = 1
# review_page = 12
def all_review(movie_id,review_page):
    reviews_content = []
    for i in range(1, review_page):
        for j in user_review(movie_id,i):
            reviews_content.append(j)
    #         print(user_review(movie_id,i))
    user_review_content = pd.DataFrame(reviews_content,
                                      columns=['user_id'
                                               ,'avg'
                                               ,'review_content'
                                               ,'date']
                                      )
# user_review_content.tail()
    return user_review_content

all_review(1,12)