from django.contrib import admin
from .models import Movie, Playlist

# Register your models here.

class movieAdmin(admin.ModelAdmin):
    filter_horizontal =('movie',)

admin.site.register(Movie)
admin.site.register(Playlist, movieAdmin)
