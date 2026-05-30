# MOVIXPedia - Smart Movie Recommender System

MOVIXPedia is a modern web-based movie recommendation system that leverages Machine Learning to suggest movies based on user preferences. It features a sleek glassmorphism UI, real-time search suggestions, and a robust user authentication system.

## 🚀 Features

-   **Intelligent Recommendations**: Uses Content-Based Filtering (TF-IDF & Cosine Similarity) to suggest movies similar to your favorites.
-   **Live Autocomplete**: Real-time search suggestions as you type, with priority for prefix matching and visual highlighting.
-   **Full-Text Search**: Search for movies by title fragments or entire genres (e.g., "Tit", "Action").
-   **User Authentication**: Secure Signup and Login system using SQLite and hashed passwords.
-   **Premium UI/UX**: A dark-themed, responsive design with glassmorphic elements and smooth animations.
-   **Poster Integration**: Dynamically fetches movie posters using the TMDB API for a rich visual experience.

## 🛠️ Tech Stack

-   **Backend**: Python (Flask)
-   **Database**: SQLite (User data), CSV (Movie dataset)
-   **Machine Learning**: Scikit-learn (TfidfVectorizer, NearestNeighbors), Pandas
-   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
-   **API**: TMDB API for fetching movie posters

## 📂 Project Structure

```text
movie_recommender/
├── core/                # Main Application Package
│   ├── backend/         # Server logic & Blueprints (Auth, Movie)
│   ├── frontend/        # UI (Templates & Static assets)
│   ├── machine_learning/# ML algorithms (Content, Hybrid)
│   ├── api_client/      # TMDB API service
│   ├── database/        # SQLite connection logic
│   └── utils/           # Shared utility functions
├── data/                # CSV Datasets and users.db
├── config.py            # Global configuration
├── run.py               # Application entry point
├── README.md
└── QUICKSTART.md
```

## ⚙️ Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd movie_recommender
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate  # Windows
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Application**:
    ```bash
    python run.py
    ```
    Access the app at `http://127.0.0.1:5000`

## 📊 How it Works

1.  **Data Loading**: The system loads movie metadata (titles, genres, overviews) from `final_merged_movies.csv`.
2.  **Feature Extraction**: It uses `TfidfVectorizer` to convert movie "tags" (overviews + genres) into numerical vectors.
3.  **Similarity Search**: When you search for a movie, the system uses `NearestNeighbors` with Cosine Similarity to find the 20 closest matches in the vector space.
4.  **Ranking**: Results are ranked based on a combination of content similarity and genre overlap.

## 🛡️ User Privacy
Passwords are never stored in plain text. MOVIXPedia uses `werkzeug.security` to hash passwords before saving them to the SQLite database, ensuring user security.

---
*Created with ❤️ by the MOVIXPedia Team.*
