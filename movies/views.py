from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import tmdbsimple as tmdb
from django.conf import settings
import datetime as dt
from .models import Movie, Playlist
from .forms import PlaylistForm
from .requests import process_results, trending_movies




# Create your views here.
tmdb.API_KEY = settings.TMDB_API
tmdb_url ='https://image.tmdb.org/t/p/w342/'

youtube_api_key = settings.YOUTUBE_API
 


def home(request):
    url= tmdb_url
    
    processed_popular= process_results('popular')
    processed_upcoming = process_results('upcoming')
    processed_trending = trending_movies()
    
    context = {
        "title": "Netflix",
        'popular':processed_popular, 
        'upcoming':processed_upcoming,
        'trending':processed_trending,
        'url':url,
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
    url= tmdb_url
    if 'search_query' in request.GET and request.GET["search_query"]:
        movie_search = request.GET.get("search_query")
        # print('capture form',movie_search)
        search = tmdb.Search()
        searched_movies_data = search.movie(query =movie_search)
        searched_movies = searched_movies_data['results']
        # print('movies',searched_movies)
        message = f"{movie_search}"
        context = {
            "message":message,
            "searched_movie": searched_movies,
            "title": message,
            "url": url,

        }

        return render(request, 'movies/search.html', context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'movie/search.html',{"message":message})


@login_required(login_url='/accounts/login/')
def create_playlist(request):

    form = PlaylistForm()
    current_user = request.user
    if request.method == 'POST':
            form = PlaylistForm(request.POST, request.FILES)
            if form.is_valid():
                playlist = form.save()               
                playlist.user = current_user
                print(playlist)
                playlist.save()                
            return redirect('home')

    else:
        form = PlaylistForm()

    context ={
        "form": form,
        }
    return render(request, 'movies/create_playlist.html', context)

def playlists(request):
    playlists =  Playlist.display_all_playlists() 

    context ={
        "playlists":playlists,    
        }
    return render(request, 'movies/playlists.html', context)
  


