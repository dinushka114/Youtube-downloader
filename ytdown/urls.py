from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name="index"),
    path('play-list/' , views.playlist_downloader , name='playlist')
]
