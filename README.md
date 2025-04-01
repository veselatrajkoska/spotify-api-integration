# Integration project

This project is a Django-based integration with the Spotify API, designed to fetch and display music-related data such as categories and new album releases. 

The application follows the Client Credentials Flow for authentication, ensuring easy API access without requiring user login. It is built using Singleton and Facade design patterns, which increase efficiency and simplify API interactions. The Spotify API client handles authentication, while a service layer abstracts API calls for better maintainability. 

Users can set up the project by configuring environment variables, installing dependencies, and running the Django server to explore Spotify's music catalog.

## Spotify API

The Spotify API has 4 authorization flows which use the OAuth 2.0 standard. I chose the _Client credentials_ flow because it doesn't require manual user permission grant, but rather the application alone authorizes the API usage.

### Client credentials flow:
1. A new app is created from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and 2 parameters are generated for the user: 
   - **Client ID**
   - **Client Secret**.
2. The Django application sends a **POST** request to https://accounts.spotify.com/api/token requesting an access token. Example request: 
```
URL: https://accounts.spotify.com/api/token

Body:
'grant_type': 'client_credentials'

Headers:
'Authorization': 'Basic <base64 encoded credentials>', 
'Content-Type': 'application/x-www-form-urlencoded'
```
3. The Spotify API returns a response containing an access token and some metadata related to it. Example response:
```
{
   "access_token": "<token>",
   "token_type": "bearer",
   "expires_in": 3600
}
```
4. The Django application can now use this access token until it expires to send **GET** requests to endpoints of the API to get various data. Example request:
```
URL: https://api.spotify.com/v1/browse/categories

Body: 
'limit': 12 

Header: 
'Authorization': 'Bearer <access token>'.
```
5. After it is received, the token is saved in cache for easy use. Each token lasts 1 hour and it is refreshed when it expires.

## Application

Prerequisites:
1. Clone the repository.
2. From the content root, run `pip install -r requirements.txt`.
3. At the content root, create a file called `.env` following the structure of the `env.sample` file.

Then, from the content root, run `python manage.py runserver` and open the application in your browser at path http://127.0.0.1:8000/.

## Design choices

### Singleton pattern

Firstly I chose the Singleton pattern to ensure that only 1 instance of the Spotify API will be used by the application. This avoids generating credentials unnecessarily and improves efficiency. This is implemented in `spotify_api.py` through the `SpotifyAPI` class.

### Facade pattern

Secondly I chose the Facade pattern in order to simplify API calls throughout the application by wrapping them in a single service class. This is implemented in `spotify_service.py` through the `SpotifyService` class.

### Application flow

The separation of API connection logic and API requests logic improves code readability and ensures that the most common calls throughout the application are short and simple and follow the same structure. The application views can easily instantiate the Spotify service and fetch data using the `make_request` method.
