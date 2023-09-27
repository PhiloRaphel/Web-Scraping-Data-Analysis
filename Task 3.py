import pandas as pd
from collections import Counter
from functions import *

# 1. Scraping Movie Data: 
# Website 1 - 250Films: -> Yousef
scrape_top250_movies()

# Website 2 - MovieMeter: -> Philo
movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating = scrape_moviemeter_data()
data_list = list(zip(movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating))
col_name = ['Movie Rank', 'Movie Title', 'Movie Alt Title', 'Movie Genre', 'Date of Release', 'Movie Rating']
save_movie_data_to_csv('moviemeter_top250.csv', data_list, col_name)
merge_and_clean_data('moviemeter_top250.csv', 'top250_movies_data.csv', 'merged_top_movies.csv')


# 2. Data Analysis:
df = pd.read_csv('merged_top_movies.csv')

# 2.1. Identify the movie(s) with the highest IMDb and moviemeter rating. -> Yousef
highest_imdb_movies = maxmin_movie(df, 'IMDB', 'max')
print("\n\n\nMovie(s) with the highest IMDB rating:")
print(highest_imdb_movies[['Movie Title', 'Movie Rating IMDB']])

highest_moviemeter_movies = maxmin_movie(df, 'mm', 'max')
print("\nMovie(s) with the highest moviemeter rating:")
print(highest_moviemeter_movies[['Movie Title', 'Movie Rating mm']])

# 2.2. Identify the movie(s) with the lowest IMDb and moviemeter rating. -> Yousef
lowest_imdb_movies = maxmin_movie(df, 'IMDB', 'min')
print("Movie(s) with the lowest IMDB rating:")
print(lowest_imdb_movies[['Movie Title', 'Movie Rating IMDB']])

lowest_moviemeter_movies = maxmin_movie(df, 'mm', 'min')
print("\nMovie(s) with the lowest moviemeter rating:")
print(lowest_moviemeter_movies[['Movie Title', 'Movie Rating mm']])

# 2.3. Identify the most found genre in the list. -> Yousef
genre, count = Counter(df['Movie Genre'].str.strip('[]').str.replace("'", "").str.split(', ').sum()).most_common(1)[0]
print(f"\n\nThe most common genre is '{genre}' with {count} occurrences.")

# 2.4. Count the number of movies released in each decade (e.g., 1950s, 1960s, etc.). -> Yousef
df['Decade'] = df['Date of Release'].apply(lambda year: str(year // 10 * 10) + 's')
decade_counts = df['Decade'].value_counts().sort_index()
print("\n\nNumber of movies released in each decade:")
print(decade_counts)

# 2.5. Create a bar chart to visualize the distribution of ratings (bins: 0-2, 2-4, 4-6, 6-8, 8-10). -> Philo
bins = [0, 2, 4, 6, 8, 10]
labels = ['0-2', '2-4', '4-6', '6-8', '8-10']
visualize_rating_distribution(df, 'Movie Rating IMDB', bins, labels,'Distribution of Movie Ratings', 'Rating','Num of Movies')


# 2.6. Create a bar chat to visualize the distribution of movie genres. -> Philo
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
