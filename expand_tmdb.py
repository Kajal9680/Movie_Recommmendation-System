'''import requests
import pandas as pd
from time import sleep
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "2a6568ad94acf2571bd9c2a8d9cfc0d4"
BASE = "https://api.themoviedb.org/3"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_movies(pages=10):   # start with 10 pages first
    rows = []

    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")

        url = f"{BASE}/discover/movie?api_key={API_KEY}&page={page}"

        try:
            response = requests.get(url, headers=HEADERS, verify=False, timeout=10)

            if response.status_code != 200:
                print("⚠️ Error code:", response.status_code)
                continue

            data = response.json()

            for m in data.get("results", []):
                rows.append({
                    "title": m.get("title"),
                    "overview": m.get("overview") or "",
                    "vote_average": m.get("vote_average", 0),
                    "genre_ids": m.get("genre_ids", [])
                })

            # 🔥 SAVE PARTIAL DATA EVERY PAGE
            pd.DataFrame(rows).to_csv("data/temp.csv", index=False)

            sleep(1.5)  # VERY IMPORTANT

        except Exception as e:
            print("❌ Error:", e)
            sleep(3)
            continue

    return pd.DataFrame(rows)


def map_genres(df):
    genre_map = {
        28:"Action", 12:"Adventure", 16:"Animation", 35:"Comedy",
        80:"Crime", 18:"Drama", 14:"Fantasy", 27:"Horror",
        9648:"Mystery", 10749:"Romance", 878:"Sci-Fi",
        53:"Thriller"
    }

    df["genres"] = df["genre_ids"].apply(
        lambda ids: [genre_map[i] for i in ids if i in genre_map]
    )

    return df


# ===== RUN =====

df = fetch_movies(pages=1)

if df.empty:
    print("❌ No data fetched. Check internet or API key.")
    exit()

df = map_genres(df)

df["rating"] = df["vote_average"]
df["tags"] = df["overview"] + " " + df["genres"].apply(lambda x: " ".join(x))

df = df[["title", "overview", "genres", "rating", "tags"]]

df.to_csv("data/tmdb_expanded.csv", index=False)

print("✅ SUCCESS: Dataset created")
print("Total movies:", len(df))'''

import requests
import pandas as pd
import time
import os

API_KEY = "2a6568ad94acf2571bd9c2a8d9cfc0d4"
BASE = "https://api.themoviedb.org/3"

SAVE_FILE = "data/tmdb_master.csv"

# -------------------------
# SAFE REQUEST
# -------------------------
def safe_request(params):
    for _ in range(3):
        try:
            r = requests.get(f"{BASE}/discover/movie", params=params, timeout=10)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                print("⛔ Rate limit, waiting...")
                time.sleep(5)
        except:
            time.sleep(2)
    return None


# -------------------------
# LOAD EXISTING DATA (RESUME)
# -------------------------
if os.path.exists(SAVE_FILE):
    df_existing = pd.read_csv(SAVE_FILE)
    collected_ids = set(df_existing["id"])
    print(f"🔄 Resuming... Existing movies: {len(df_existing)}")
else:
    df_existing = pd.DataFrame()
    collected_ids = set()

all_movies = []

# -------------------------
# FETCH YEAR-WISE
# -------------------------
for year in range(1980, 2024):

    print(f"\n🎬 Year: {year}")

    for page in range(1, 101):   # safe range

        params = {
            "api_key": API_KEY,
            "primary_release_year": year,
            "page": page,
            "sort_by": "popularity.desc"
        }

        data = safe_request(params)

        if not data or "results" not in data:
            break

        results = data["results"]

        if len(results) == 0:
            break

        for m in results:
            movie_id = m.get("id")

            # ❗ skip duplicates automatically
            if movie_id in collected_ids:
                continue

            collected_ids.add(movie_id)

            all_movies.append({
                "id": movie_id,
                "title": m.get("title"),
                "overview": m.get("overview") or "",
                "rating": m.get("vote_average", 0),
                "genre_ids": m.get("genre_ids", [])
            })

        print(f"✔ Page {page}")

        time.sleep(1)

    # -------------------------
    # SAVE AFTER EACH YEAR
    # -------------------------
    df_temp = pd.DataFrame(all_movies)
    df_combined = pd.concat([df_existing, df_temp])
    df_combined.drop_duplicates(subset=["id"], inplace=True)

    df_combined.to_csv(SAVE_FILE, index=False)

    print(f"💾 Saved after {year} → Total: {len(df_combined)}")

# -------------------------
# FINAL PROCESSING
# -------------------------
df = pd.read_csv(SAVE_FILE)

GENRE_MAP = {
    28:"Action",12:"Adventure",16:"Animation",35:"Comedy",
    80:"Crime",18:"Drama",27:"Horror",10749:"Romance",
    878:"Sci-Fi",53:"Thriller"
}

def convert(ids):
    return [GENRE_MAP[i] for i in ids if i in GENRE_MAP]

df["genres"] = df["genre_ids"].apply(convert)

df["tags"] = df["overview"] + " " + df["genres"].apply(lambda x: " ".join(x))

df = df[["title", "overview", "genres", "rating", "tags"]]

df.to_csv("data/tmdb_final_clean.csv", index=False)

print("\n✅ FINAL DATASET READY!")
print("Total movies:", len(df))