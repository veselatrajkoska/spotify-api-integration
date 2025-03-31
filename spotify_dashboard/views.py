from django.shortcuts import render

from .services.spotify_service import SpotifyService
# Create your views here.

def index(request):
    return render(request, 'index.html')

def categories(request):
    spotify_service = SpotifyService()
    categories = spotify_service.get_categories()
    context = {'categories': categories}
    return render(request, 'categories.html', context=context)

def albums(request):
    spotify_service = SpotifyService()
    albums = spotify_service.get_new_releases()
    context = {'albums': albums}
    return render(request, 'albums.html', context=context)
