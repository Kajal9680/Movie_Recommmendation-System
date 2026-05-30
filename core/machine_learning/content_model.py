import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# ------------------------------------------
# BUILD CONTENT MODEL
# ------------------------------------------
def build_content_model(movies):
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(movies["tags"])
    nn = NearestNeighbors(n_neighbors=11, metric='cosine')
    nn.fit(matrix)
    return nn, matrix

# ------------------------------------------
# GET RECOMMENDATIONS
# ------------------------------------------
def get_content_recommendations(title, movies, nn, matrix, top_n=50):
    # Normalize titles
    titles_lower = movies["title"].str.lower().tolist()
    search_query = title.lower().strip()

    # 1. FIND THE BEST "SEED" MOVIE FOR ML RECOMMENDATIONS (Backup)
    match_idx = None
    if search_query in titles_lower:
        match_idx = titles_lower.index(search_query)
    if match_idx is None:
        starts = [i for i, t in enumerate(titles_lower) if t.startswith(search_query)]
        if starts: match_idx = min(starts, key=lambda i: len(titles_lower[i]))
    if match_idx is None:
        fuzzy = get_close_matches(search_query, titles_lower, n=1, cutoff=0.6)
        if fuzzy: match_idx = titles_lower.index(fuzzy[0])

    results = []
    seen = set()

    # 2. FIND ALL MOVIES BASED ON TEXT MATCH (Title or Genre)
    # Priority A: Title starts with
    sw = movies[movies['title'].str.lower().str.startswith(search_query)]
    # Priority B: Title contains
    ct = movies[movies['title'].str.lower().str.contains(search_query) & ~movies['title'].str.lower().str.startswith(search_query)]
    # Priority C: Genre match
    gn = movies[movies['genres'].apply(lambda g: any(search_query in genre.lower() for genre in g))]

    # Combine text matches
    text_matches = pd.concat([sw, ct, gn]).drop_duplicates(subset=['title'])
    
    for _, row in text_matches.head(top_n).iterrows():
        movie_name = row["title"]
        results.append({
            "title": movie_name,
            "match_percent": 100.0 if (search_query in movie_name.lower()) else 90.0,
            "rating": round(row["rating"], 1),
            "genres": " • ".join(row["genres"])
        })
        seen.add(movie_name)

    # 3. IF WE HAVE FEW TEXT MATCHES, FILL WITH ML RECOMMENDATIONS
    if len(results) < 10 and match_idx is not None:
        seed_movie = movies.iloc[match_idx]
        input_genres = set(seed_movie["genres"])
        
        distances, indices = nn.kneighbors(matrix[match_idx], n_neighbors=top_n + 10)
        for j, i in enumerate(indices[0]):
            movie_name = movies.iloc[i]["title"]
            if movie_name in seen: continue
            
            sim_score = 1 - distances[0][j]
            movie_genres = set(movies.iloc[i]["genres"])
            genre_score = len(input_genres & movie_genres) / len(input_genres) if input_genres else 0
            final_score = (0.7 * sim_score + 0.3 * genre_score) * 100
            
            results.append({
                "title": movie_name,
                "match_percent": round(final_score, 2),
                "rating": round(movies.iloc[i]["rating"], 1),
                "genres": " • ".join(movies.iloc[i]["genres"])
            })
            seen.add(movie_name)
            if len(results) >= top_n:
                break

    return results[:top_n]


