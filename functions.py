import requests
from scrapy import Selector
import pandas as pd

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