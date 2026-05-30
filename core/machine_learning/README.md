# 🤖 Machine Learning Layer

This folder contains the core recommendation engine and the mathematical models.

### 📄 Files
- **`content_model.py`**: Implementation of Content-Based Filtering using TF-IDF and Cosine Similarity.
- **`model_state.py`**: Manages the global state of the loaded models to prevent redundant reloading.
- **`hybrid_model.py`** & **`collab_model.py`**: Experimental model implementations.

### ⚙️ How it works
1. **Feature Extraction**: Movie overviews and genres are vectorized using `TfidfVectorizer`.
2. **Similarity Calculation**: When a movie is searched, the `NearestNeighbors` model finds the 50 most similar vectors.
3. **Ranking**: Results are returned based on their similarity score to the searched movie.
