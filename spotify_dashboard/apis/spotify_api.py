import requests
import base64
import logging

from django.conf import settings
from django.core.cache import cache

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class SpotifyAPI:
    """
    Class to handle Spotify API Singleton instance.
    """
    _instance = None
    default_expiration_seconds = 3600

    def __new__(cls):
        """
        Ensures only one instance of SpotifyAPIClient exists.
        """
        if cls._instance is None:
            cls._instance = super(SpotifyAPI, cls).__new__(cls)
            cls._instance.access_token = None
            cls._instance.token_expires_in = cls.default_expiration_seconds
            cls._instance.logger = logging.getLogger(__name__)

        return cls._instance

    def refresh_access_token(self):
        """
        Requests a new access token from Spotify API.
        """
        url = 'https://accounts.spotify.com/api/token'
        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET
        encoded_credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()

        parameters = {
            'grant_type': 'client_credentials'
        }
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers = headers, data = parameters)

        if response.status_code == 200:
            token_data = response.json()
            self._instance.access_token = token_data['access_token']
            self._instance.token_expires_in = token_data['expires_in']

            self._instance.logger.info('Successfully obtained access token.')
            cache.set('spotify_access_token', self._instance.access_token, timeout = self.token_expires_in - 60)
            return self._instance.access_token
        else:
            self._instance.logger.error(response.text)
            raise Exception(f'Could not retrieve access token.')

    def get_access_token(self):
        """
        Retrieves an access token, using cache or requesting a new one.
        """
        token = cache.get('spotify_access_token')
        if token:
            return token

        return self.refresh_access_token()

    def get_authorization_headers(self):
        """
        Returns the authorization headers for Spotify API requests.
        """
        token = self.get_access_token()
        print('ACCESS TOKEN:', token)
        return {
            'Authorization': f'Bearer {self.get_access_token()}'
        }

    def make_request(self, endpoint, params = None):
        """
        Makes a request to the Spotify API.
        """
        url = f'https://api.spotify.com/v1/{endpoint}'
        headers = self.get_authorization_headers()

        response = requests.get(url, headers = headers, params = params)

        if response.status_code == 200:
            return response.json()
        else:
            self._instance.logger.error(response.text)
            raise Exception('Error fetching data.')
