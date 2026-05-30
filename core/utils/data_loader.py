import pandas as pd
import ast

from config import Config

def load_data():
    movies = pd.read_csv(Config.MOVIES_CSV)
    movies['genres'] = movies['genres'].apply(lambda x: x.split(' , ') if pd.notna(x) else [])
    return movies


def preprocess(movies):

    movies['overview'] = movies['overview'].fillna('')

    movies['tags'] = movies['overview'] + " " + movies['genres'].apply(lambda x: " ".join(x))
    movies['rating'] = movies['rating']

    return movies