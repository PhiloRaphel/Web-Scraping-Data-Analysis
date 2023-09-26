from functions import scrape_top250_movies, scrape_movie_data, save_movie_data_to_csv,merge_and_clean_data,visualize_genre_distribution,visualize_rating_distribution


scrape_top250_movies()
movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating = scrape_movie_data()
save_movie_data_to_csv(movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating)
merge_and_clean_data()

import pandas as pd

# Step 1: Read the CSV data into a DataFrame
df = pd.read_csv('merged.csv')

df['Movie Genre'] = df['Movie Genre'].str.replace("[\[\]']", '', regex=True)





visualize_rating_distribution(df)


separated_movies = []

# Separate movies by genre
for index, row in df.iterrows():
    genres = row['Movie Genre'].split(', ')
    for genre in genres:
        separated_movie = row.copy()
        separated_movie['Movie Genre'] = genre
        separated_movies.append(separated_movie)

separated_df = pd.DataFrame(separated_movies)
visualize_genre_distribution(separated_df, 'Movie Genre')

