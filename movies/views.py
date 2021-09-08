from django.shortcuts import render
import json
import tmdbsimple as tmdb
from decouple import config
import datetime as dt



# Create your views here.
# tmdb.tmdb_api = config('TMDB.API_KEY')
tmdb.API_KEY = 'a39313391038c326a4b959984d2e07d4'
tmdb_url ='https://image.tmdb.org/t/p/w342/'


def home(request):
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
    }

    return render(request, 'movies/index.html', context)

def movie_details(request, movie_id):
    movies_tmdb = tmdb.Movies(movie_id)
    movies = movies_tmdb.info()
    date_created = movies['release_date']
    date_time = dt.datetime.strptime(date_created, '%Y-%m-%d')
    # Get movie name and use it to pass it as an argument to the youtube api.
    movie_name = movies['original_title']
    # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # search_response = youtube.search().list(q=movie_name, part='id,snippet', maxResults=1).execute()
    # for search_result in search_response.get('items', []):
    #     if search_result['id']['kind'] == 'youtube#video':
    #         video_id = search_result['id']['videoId']

    context = {
        'movies':movies,
        'date':date_time
    }
    return render(request, 'movies/movie.html', context)

def search_movies(request):

    if 'search_query' in request.GET and request.GET["search_query"]:
        movie_search = request.GET.get("search_query")
        print('capture form',movie_search)
        search = tmdb.Search()
        searched_movies = search.movie(query =movie_search)
        print('movies',searched_movies)
        message = f"{movie_search}"
        context = {
            "message":message,
            "searched_movie": searched_movies

        }

        return render(request, 'movies/search.html', context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'movie/search.html',{"message":message})


