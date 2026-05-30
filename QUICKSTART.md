# ⚡ MOVIXPedia Quick Start Guide

Follow these 4 simple steps to get your movie recommender up and running in less than 2 minutes.

---

### Step 1: Set Up Your Environment
Open your terminal in the project folder and run:
```powershell
# Create virtual environment
python -m venv .venv

# Activate it (Windows)
.\.venv\Scripts\activate
```

### Step 2: Install Dependencies
Install the required libraries:
```powershell
pip install -r requirements.txt
```

### Step 3: Configure API Key (Optional but Recommended)
To see movie posters, open `config.py` and add your TMDB API key:
```python
TMDB_API_KEY = "your_key_here"
```
*(If you don't have one, the app will still work but will show placeholder images).*

### Step 4: Launch the App
Start the Flask server:
```powershell
python run.py
```

---

### 🌐 How to Use
1.  Open your browser and go to: `http://127.0.0.1:5000`
2.  **Search**: Type a movie name (like "Titanic") or just a few letters (like "Bat") in the search bar.
3.  **Explore**: Select a movie from the autocomplete list or click "Recommend".
4.  **Login/Signup**: Create an account to experience the full features!

### 🆘 Common Fixes
*   **ModuleNotFoundError**: Ensure you are inside the `.venv` and have run `pip install`.
*   **Database Error**: The system automatically creates `users.db` on the first run.
*   **No Images**: Check your internet connection and TMDB API key in `config.py`.

---
**Happy Movie Hunting!** 🍿
