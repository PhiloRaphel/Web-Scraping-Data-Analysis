from functions import *
import pandas as pd

scrape_top250_movies()
movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating = scrape_moviemeter_data()
data_list = list(zip(movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating))
col_name = ['Movie Rank', 'Movie Title', 'Movie Alt Title', 'Movie Genre', 'Date of Release', 'Movie Rating']
save_movie_data_to_csv('moviemeter_top250.csv', data_list, col_name)
merge_and_clean_data('moviemeter_top250.csv', 'top250_movies_data.csv', 'merged_top_movies.csv')



df = pd.read_csv('merged_top_movies.csv')
bins = [0, 2, 4, 6, 8, 10]
labels = ['0-2', '2-4', '4-6', '6-8', '8-10']
visualize_rating_distribution(df, 'Movie Rating IMDB', bins, labels,'Distribution of Movie Ratings', 'Rating','Num of Movies')


separated_movies = []
df['Movie Genre'] = df['Movie Genre'].str.replace("[\[\]']", '', regex=True)
for index, row in df.iterrows():
    genres = row['Movie Genre'].split(', ')
    for genre in genres:
        separated_movie = row.copy()
        separated_movie['Movie Genre'] = genre
        separated_movies.append(separated_movie)

separated_df = pd.DataFrame(separated_movies)
visualize_genre_distribution(separated_df, 'Movie Genre','Movie Genre Distribution','Genre', 'Count')

