from functions import scrape_top250_movies, scrape_movie_data, save_movie_data_to_csv,merge_and_clean_data


scrape_top250_movies()
movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating = scrape_movie_data()
save_movie_data_to_csv(movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating)
merge_and_clean_data()
