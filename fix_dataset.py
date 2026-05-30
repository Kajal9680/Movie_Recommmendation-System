'''import pandas as pd
import ast

# -------------------------
# LOAD BOTH DATASETS
# -------------------------

df1 = pd.read_csv("data/tmdb_master.csv")        # has genre_ids
df2 = pd.read_csv("data/tmdb_final_clean.csv")   # has tags

# -------------------------
# CONVERT genre_ids → genres
# -------------------------

genre_map = {
    28:"Action", 12:"Adventure", 16:"Animation", 35:"Comedy",
    80:"Crime", 18:"Drama", 14:"Fantasy", 27:"Horror",
    9648:"Mystery", 10749:"Romance", 878:"Sci-Fi",
    53:"Thriller"
}

def convert_genres(x):
    try:
        ids = ast.literal_eval(x) if isinstance(x, str) else x
        return [genre_map[i] for i in ids if i in genre_map]
    except:
        return []

df1["genres"] = df1["genre_ids"].apply(convert_genres)

# -------------------------
# CLEAN DATA
# -------------------------

df1["overview"] = df1["overview"].fillna("")
df2["tags"] = df2["tags"].fillna("")

# -------------------------
# MERGE DATASETS
# -------------------------

df = pd.merge(df1, df2[["title", "tags"]], on="title", how="inner")

# -------------------------
# ADD RATING
# -------------------------

if "vote_average" in df.columns:
    df["rating"] = df["vote_average"]

# -------------------------
# FINAL FORMAT
# -------------------------

df["genres"] = df["genres"].apply(lambda x: " , ".join(x))

df = df[["title", "overview", "genres", "rating", "tags"]]

# -------------------------
# SAVE FINAL DATASET
# -------------------------

df.to_csv("data/final_merged_movies.csv", index=False)

print("✅ FINAL DATASET CREATED")
print("Total movies:", len(df))'''

import pandas as pd

df = pd.read_csv("data/final_merged_movies.csv")

def clean_genres(x):
    try:
        # convert to string
        x = str(x)

        # remove brackets and quotes
        x = x.replace("[", "").replace("]", "").replace("'", "")

        # split into list
        genres = [g.strip() for g in x.split(",") if g.strip()]

        # convert back to required format
        return str(genres)

    except:
        return "[]"

df["genres"] = df["genres"].apply(clean_genres)

# save clean file
df.to_csv("data/final_clean_movies.csv", index=False)

print("✅ PERFECT: Genres fully fixed")

