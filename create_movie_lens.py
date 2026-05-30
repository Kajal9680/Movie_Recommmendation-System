import pandas as pd
import ast

movies = pd.read_csv(r"C:\movie_recommender\data\tmdb_5000_movies.csv")

# convert genres
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return "|".join(L)

movies['genres'] = movies['genres'].apply(convert)

# create MovieLens-style dataset
movies_lens = pd.DataFrame({
    "movieId": range(1, len(movies)+1),
    "title": movies['title'],
    "genres": movies['genres']
})

movies_lens.to_csv("data/movies.csv", index=False)

print("✅ movies.csv generated successfully!")