from spotify_dashboard.apis.spotify_api import SpotifyAPI
from ..dataclasses import *

class SpotifyService:
    """
    Abstraction to the Spotify API.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.api = SpotifyAPI()

    def get_categories(self):
        """
        Returns a list of categories.
        """
        params = {
            'limit': 12
        }
        response = self.api.make_request('browse/categories', params = params)

        categories = []
        for item in response['categories']['items']:
            category = {
                'id': item['id'],
                'name': item['name'],
                'icon': self.get_category_icon(item['icons'])
            }
            categories.append(Category(**category))

        return categories

    def get_category_icon(self, icons):
        """
        Returns the URL of the category icon or blank thumbnail if no icon is available.
        """
        default_thumbnail = 'https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2'
        if len(icons) == 0:
            return default_thumbnail
        else:
            return icons[0]['url']

    def get_new_releases(self):
        """
        Returns a list of featured new album releases.
        """
        params = {
            'limit': 12
        }
        response = self.api.make_request('browse/new-releases', params = params)

        albums = []
        for item in response['albums']['items']:
            album = {
                'id': item['id'],
                'name': item['name'],
                'artists': self.get_album_artists(item['artists']),
                'image': self.get_album_image(item['images']),
                'release_date': item['release_date'],
                'url': item['external_urls']['spotify']
            }
            albums.append(Album(**album))

        return albums

    def get_album_image(self, images):
        """
        Returns the URL of the album image or blank thumbnail if no image is available.
        """
        default_thumbnail = 'https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2'
        if len(images) == 0:
            return default_thumbnail
        else:
            return images[0]['url']

    def get_album_artists(self, artists):
        """
        Returns a list of album artists' names.
        """
        names = []
        for artist in artists:
            names.append(artist['name'])

        return names

    def get_featured_playlists(self):
        """
        Returns a list of featured playlists.
        """
        response = self.api.make_request(endpoint = 'browse/featured-playlists')

        playlists = []
        for item in response['items']:
            playlist = {
                'id': item['id'],
                'name': item['name'],
                'description': item['description'],
                'image': self.get_playlist_image(item['images']),
                'number_of_tracks': item['tracks']['total'],
                'url': item['external_urls']['spotify']
            }
            playlists.append(Playlist(**playlist))

        return playlists

    def get_playlist_image(self, images):
        """
        Returns the URL of the playlist image or blank thumbnail if no image is available.
        """
        default_thumbnail = 'https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2'
        if len(images) == 0:
            return default_thumbnail
        else:
            return images[0]['url']
