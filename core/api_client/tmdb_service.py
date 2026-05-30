import requests
from functools import lru_cache
from config import Config

session = requests.Session()

@lru_cache(maxsize=512)
def fetch_poster(movie_name):

    movie_name = movie_name.strip()
    if not movie_name:
        return 'https://via.placeholder.com/300x450?text=No+Image'

    url = f'https://api.themoviedb.org/3/search/movie?api_key={Config.TMDB_API_KEY}&query={requests.utils.requote_uri(movie_name)}'

    try:
        data = session.get(url, timeout=1.5).json()

        if 'results' in data and len(data['results']) > 0:
            poster_path = data['results'][0].get('poster_path')

            if poster_path:
                return 'https://image.tmdb.org/t/p/w500' + poster_path

    except requests.RequestException:
        pass

    return 'https://via.placeholder.com/300x450?text=No+Image'
