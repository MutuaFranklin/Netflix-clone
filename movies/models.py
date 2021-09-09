from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Movie(models.Model):
    movie_id = models.IntegerField()
    movie_title =models.CharField(max_length=100)
    image_path =models.TextField()
    movie_overview = models.TextField()
    movie_votes = models.FloatField()


    def __str__(self):
        return self.movie_title

    def save_movie(self):
        self.save()

class Playlist(models.Model):
    playlist_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ManyToManyField(Movie)

    def save_playlist(self):
        self.save()

    @classmethod
    def display_all_playlists(cls):
        return cls.objects.all()

    @classmethod
    def filter_by_playlist_name(cls, filter_playlist):
        try:
            playlist= cls.objects.filter(playlist_name__icontains=filter_playlist)
            return playlist
        except Exception:
            return  "No playlist found in your filter playlist"

