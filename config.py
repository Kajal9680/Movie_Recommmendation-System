import os

class Config:
    SECRET_KEY = 'movixpedia_secret_key_2026'
    TMDB_API_KEY = "2a6568ad94acf2571bd9c2a8d9cfc0d4"
    
    # Paths
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    DB_PATH = os.path.join(DATA_DIR, 'users.db')
    MOVIES_CSV = os.path.join(DATA_DIR, 'final_merged_movies.csv')