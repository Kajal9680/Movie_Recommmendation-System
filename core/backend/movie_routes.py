from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.machine_learning.content_model import get_content_recommendations
from core.api_client.tmdb_service import fetch_poster
import core.machine_learning.model_state as state

main_bp = Blueprint('main', __name__)

# ── Helper Functions ──
def _fetch_posters(recs):
    """Fetch posters for a list of recommendation dicts in parallel."""
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_index = {
            executor.submit(fetch_poster, r['title']): i
            for i, r in enumerate(recs)
        }
        for future in as_completed(future_to_index):
            i = future_to_index[future]
            try:
                recs[i]['poster'] = future.result()
            except Exception:
                recs[i]['poster'] = "https://via.placeholder.com/300x450?text=No+Image"
    return recs

def _movie_exists(title):
    """Check if the movie title exists in the dataset."""
    title_lower = title.lower().strip()
    all_titles = state.movies_df['title'].str.lower().tolist()
    return title_lower in all_titles or any(title_lower in t for t in all_titles)

def _get_random_movies(n=10):
    """Return n random popular movies from the dataset."""
    sample = state.movies_df.sample(n=min(n, len(state.movies_df)))
    random_recs = []
    for _, row in sample.iterrows():
        random_recs.append({
            "title": row["title"],
            "match_percent": 0,
            "rating": round(row["rating"], 1),
            "genres": " • ".join(row["genres"])
        })
    return random_recs

# ── Routes ──
@main_bp.route('/')
def home():
    movie_titles = state.movies_df['title'].tolist()
    return render_template("index.html", movie_titles=movie_titles)

@main_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    movie = request.values.get('movie', '').strip()
    if not movie:
        return redirect(url_for('main.home'))

    if not _movie_exists(movie):
        random_recs = _get_random_movies(10)
        random_recs = _fetch_posters(random_recs)
        return render_template(
            "result.html",
            results=random_recs,
            searched_movie=movie,
            error_message=f'"{movie}" movie is not available in our database.'
        )

    recs = get_content_recommendations(movie, state.movies_df, state.nn_model, state.tfidf_matrix, top_n=50)
    recs = _fetch_posters(recs)

    return render_template("result.html", results=recs, searched_movie=movie, error_message=None)
