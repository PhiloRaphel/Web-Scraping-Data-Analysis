import requests
from scrapy import Selector
import pandas as pd
import scrapy
import csv
from scrapy.crawler import CrawlerProcess
import matplotlib.pyplot as plt


# Author: Yousef
def scrape_top250_movies(url = 'http://top250.info/charts/?2023/09/25'):
    try:
        html = requests.get(url).content
        sel = Selector(text = html)

        df = pd.DataFrame(columns=['Movie Title', 'Date of Release', 'Movie Rank', 'Movie Rating'])

        # Scrape all the movies
        movies = sel.css('tr[class^="row_"]')
        if not movies:
            raise Exception("Website structure has changed. Unable to scrape data.")
        
        movies = movies[1:]  # Skip the Headers
        for movie in movies:
            # Scrape the movie info
            title_and_year_of_release = movie.css('td:nth-of-type(3) > a > span::text').extract_first()
            rank = movie.css('td:nth-of-type(1)::text').extract_first()
            rating = movie.css('td:nth-of-type(4)::text').extract_first()
            if not title_and_year_of_release or not rank or not rating:
                raise Exception("Website structure has changed. Unable to scrape data.")
            
            # Find the position of the opening and closing parentheses
            opening_parenthesis_index = title_and_year_of_release.find('(')
            closing_parenthesis_index = title_and_year_of_release.find(')')

            # Extract the title and year using slicing
            title = title_and_year_of_release[:opening_parenthesis_index].strip()
            year_of_release = title_and_year_of_release[opening_parenthesis_index + 1:closing_parenthesis_index]
            
            movie_data = {
                'Movie Title': title,
                'Date of Release': year_of_release,
                'Movie Rank': rank,
                'Movie Rating': rating
            }

            # Append the dictionary as a new row to the DataFrame
            df = pd.concat([df, pd.DataFrame([movie_data])], ignore_index=True)
        df.to_csv('top250_movies_data.csv', index=False)
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Author: Philo
def scrape_moviemeter_data():
    movie_title = []    
    movie_alt_title = []
    movie_genre = []
    movie_rating = []
    movie_rank = []
    movie_rel_date = []

    class MovieMeterSpider(scrapy.Spider):
        name = 'moviemeterspider'
        
        def start_requests(self):
            try:
                yield scrapy.Request(url='https://www.moviemeter.com/movies/top-250-best-movies-of-all-time', callback=self.parse)
            except Exception as e:
                print(f"An exception occurred: {str(e)}")

        def parse(self, response):
            try:
                
                list_items = response.xpath('.//*[@id="filter_system"]/div[2]')
                num_table = len(list_items.xpath('./table'))
                num_movs_per_table = []

                for i in range(num_table):
                    num_movs_per_table.append(len(list_items.xpath(f'./table[{i+1}]/tbody/tr')))

                for i in range(num_table):
                    for j in range((num_movs_per_table[i])):
                        movie_title.append(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/h4/a/text()').extract()[0][:-7])
                        year = list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/h4/a/text()').extract()[0][-7:]
                        movie_rel_date.append(year[2:-1])

                        if len(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/div')) == 2:
                            movie_alt_title.append('')
                            movie_genre.append(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/div[1]/text()').extract())
                        elif len(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/div')) == 3:
                            movie_alt_title.append(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/div[1]/text()').extract()[0][19:])
                            movie_genre.append(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[3]/div/div[2]/text()').extract())

                        movie_rank.append(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[1]/a/span/text()').extract()[0]) 
                        movie_rating.append(list_items.xpath(f'./table[{i+1}]/tbody/tr[{j+1}]/td[4]/div/div[1]/text()').extract()[0])
            except Exception as e:
                print(f"An exception occurred: {str(e)}")
            
    process = CrawlerProcess()
    process.crawl(MovieMeterSpider)
    process.start()
    return movie_rank, movie_title, movie_alt_title, movie_genre, movie_rel_date, movie_rating

# Author: Philo
def save_movie_data_to_csv(csv_file_name,data_list,col_names):
    csv_filename = csv_file_name
    data = data_list
    try:
        with open(csv_filename, 'w', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(col_names)
            csv_writer.writerows(data)
    except Exception as err_msg:
        print(f"An error occurred: {str(err_msg)}")

# Author: Philo
def merge_and_clean_data(movie_meter_csv, top250_movies_csv, merged_file_csv_name):
    try:
        movie_meter_df = pd.read_csv(movie_meter_csv)
        top_250_df = pd.read_csv(top250_movies_csv)    
        merged_df = pd.merge(movie_meter_df, top_250_df, on='Movie Title', how='inner')    
        merged_df = merged_df[['Movie Rank_x', 'Movie Title', 'Movie Alt Title', 'Movie Genre', 'Date of Release_x', 'Movie Rating_y', 'Movie Rating_x']]
        merged_df.rename(columns={'Date of Release_x': 'Date of Release', 'Movie Rank_x': 'Movie Rank', 'Movie Rating_x': 'Movie Rating mm', 'Movie Rating_y': 'Movie Rating IMDB'}, inplace=True)
        merged_df['Movie Rank'] = range(1, len(merged_df) + 1)
        merged_df['Movie Rating mm'] = merged_df['Movie Rating mm'].str.replace(',', '.').astype(float)
        
        merged_df.to_csv(merged_file_csv_name, index=False)
    except Exception as err_msg:
        print(f"An error occurred: {str(err_msg)}")

# Author: Philo    
def visualize_rating_distribution(data,rating_col_name, bins, labels, title, x_labal, y_label):
    try:
        data['Rating Bin'] = pd.cut(data[rating_col_name], bins=bins, labels=labels)
    
        rating_counts = data['Rating Bin'].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        plt.bar(rating_counts.index, rating_counts.values)
        plt.xlabel(x_labal)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()
        plt.tight_layout()
        plt.show()

    except Exception as err_msg:
        print(f"An error occurred: {str(err_msg)}")

# Author: Philo
def visualize_genre_distribution(data, col_name, title, x_label, y_label):
    genre_counts = data[col_name].value_counts()
    plt.figure(figsize=(10, 6))
    genre_counts.plot(kind='bar')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

# Author: Yousef
def maxmin_movie(df, rating, fn):
    if fn == 'max':
        return df[df['Movie Rating IMDB'] == df['Movie Rating IMDB'].max()]  if rating =='IMDB' else df[df['Movie Rating mm'] == df['Movie Rating mm'].max()] 
    elif fn == 'min':
        return df[df['Movie Rating IMDB'] == df['Movie Rating IMDB'].min()]  if rating =='IMDB' else df[df['Movie Rating mm'] == df['Movie Rating mm'].min()] 