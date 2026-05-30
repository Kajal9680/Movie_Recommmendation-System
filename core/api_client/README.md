# 🌐 API Service Layer

This folder handles all communications with external web services.

### 📄 Files
- **`tmdb_service.py`**: Integration with The Movie Database (TMDB) API.

### ⚙️ How it works
It fetches movie posters and metadata from TMDB in real-time. To optimize performance, it uses:
- **`ThreadPoolExecutor`**: For parallel API calls (fetching 50 posters simultaneously).
- **`lru_cache`**: To cache results and avoid repeated network requests for the same movie.
