from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path


urlpatterns=[
    re_path(r'^$', views.home, name='home'),
    re_path(r'^movie/(\d+)', views.movie_details, name = 'movie'),
    re_path(r'^search/', views.search_movies, name='search_movies'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

