# 📊 Data Storage

This folder is the central storage for all static and dynamic data files.

### 📄 Files
- **`final_merged_movies.csv`**: The primary dataset containing movie titles, genres, ratings, and overviews.
- **`users.db`**: The SQLite database containing hashed user credentials and account info.

### ⚠️ Important
- Never delete the `final_merged_movies.csv` file, as the recommendation engine depends on it.
- The `users.db` file is automatically created on the first run if it doesn't exist.
