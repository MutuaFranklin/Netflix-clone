from .models import Movie
import tmdbsimple as tmdb
from django.conf import settings
import requests


def process_results(endpoint): 
    results =[]
    movies_tmdb = tmdb.Movies(endpoint)
    movies = movies_tmdb.info()['results']
    
    for movie in movies:
        movie_id = movie['id']
        if movie['original_title']:
            movie_title = movie['original_title']
        elif movie['original_name']:
            movie_title = movie['original_name']
        else:
            movie_title = movie['name']
        image_path  ='https://image.tmdb.org/t/p/w342'+movie['backdrop_path']
        movie_overview =movie['overview']
        movie_votes = movie['vote_average']

        new_movie = Movie(movie_id=movie_id, movie_title=movie_title, image_path=image_path, movie_overview=movie_overview, movie_votes=movie_votes)
        results.append(new_movie)
        # new_movie.save()

    return results


def trending_movies():
    api_key = settings.TMDB_API
    endpoint = 'https://api.themoviedb.org/3/trending/all/day?api_key={api_key}'
    url = endpoint.format(api_key = api_key)
    response = requests.get(url)
    if response.status_code == 200:
        trending = response.json()
        results = trending['results']

    return results








   