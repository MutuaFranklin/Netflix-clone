from django.shortcuts import render
import json
import tmdbsimple as tmdb
from django.conf import settings
import datetime as dt




# Create your views here.
tmdb.API_KEY = settings.TMDB_API
tmdb_url ='https://image.tmdb.org/t/p/w342/'


def home(request):
    current_user = request.user
    popular_movies_tmdb = tmdb.Movies('popular')
    popular_movies = popular_movies_tmdb.info()['results']
    url= tmdb_url

    upcoming_movies_tmdb = tmdb.Movies('upcoming')
    upcoming_movies = upcoming_movies_tmdb.info()['results']
    context = {
        "title": "Netflix",
        'popular':popular_movies, 
        'upcoming':upcoming_movies,
        'url':url,
        'current_user': current_user
    }

    return render(request, 'movies/index.html', context)

def movie_details(request, movie_id):
    url= tmdb_url
    movies_tmdb = tmdb.Movies(movie_id)
    movies = movies_tmdb.info()
    date_created = movies['release_date']
    date_time = dt.datetime.strptime(date_created, '%Y-%m-%d')
    

    context = {
        'movies':movies,
        'date':date_time,
        'url':url,
    }
    return render(request, 'movies/movie.html', context)

def search_movies(request):

    if 'search_query' in request.GET and request.GET["search_query"]:
        movie_search = request.GET.get("search_query")
        print('capture form',movie_search)
        search = tmdb.Search()
        searched_movies_data = search.movie(query =movie_search)
        searched_movies = searched_movies_data['results']
        print('movies',searched_movies)
        message = f"{movie_search}"
        context = {
            "message":message,
            "searched_movie": searched_movies,
            "title": message,

        }

        return render(request, 'movies/search.html', context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'movie/search.html',{"message":message})


