import pandas as pd
import numpy as np

print("🚀 Generating Full Ratings Dataset...")

# Load movies
movies = pd.read_csv("data/tmdb_5000_movies.csv")

num_users = 200   # you can increase (50–200 is good)

ratings_data = []

for user in range(1, num_users + 1):

    # each user has a bias (some users give high rating, some low)
    user_bias = np.random.uniform(-0.5, 0.5)

    for _, row in movies.iterrows():

        base_rating = row['vote_average'] / 2  # scale 0–10 → 0–5

        noise = np.random.normal(0, 0.5)

        rating = base_rating + user_bias + noise

        # clamp rating between 1 and 5
        rating = max(1, min(5, rating))

        ratings_data.append({
            "userId": user,
            "title": row['title'],
            "rating": round(rating, 1)
        })

ratings = pd.DataFrame(ratings_data)

ratings.to_csv("data/final_ratings.csv", index=False)

print("✅ Dataset created successfully!")
print("Total rows:", len(ratings))