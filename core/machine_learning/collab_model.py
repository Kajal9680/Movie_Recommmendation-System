'''import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def build_collab_model():

    ratings = pd.read_csv("data/final_ratings.csv")

    user_item = ratings.pivot_table(
        index="userId", 
        columns="title", 
        values="rating",
        aggfunc='mean'
    )
    user_item.fillna(0, inplace=True)

    similarity = cosine_similarity(user_item)

    return user_item, similarity


def get_collab_recommendations(user_id, user_item, similarity, top_n=10):

    if user_id not in user_item.index:
        return []

    sim_df = pd.DataFrame(similarity, index=user_item.index, columns=user_item.index)

    similar_users = sim_df[user_id].sort_values(ascending=False)[1:20]

    scores = {}

    for user, sim_score in similar_users.items():
        for movie, rating in user_item.loc[user].items():
            scores[movie] = scores.get(movie, 0) + sim_score * rating

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [{"title": m, "collab_score": s} for m, s in sorted_scores[:top_n]]'''