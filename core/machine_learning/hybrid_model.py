'''# models/hybrid_model.py

import pandas as pd


def blend(content, collab=None, top_n=5):
    """
    Hybrid blending:
    Uses content similarity + movie rating
    (collaborative optional)
    """

    # Convert content results to dataframe
    df = pd.DataFrame(content)

    # If no collaborative data provided
    if collab is None or len(collab) == 0:

        # Normalize rating (0–10 → 0–1)
        df['rating_norm'] = df['rating'] / 10

        # Hybrid score calculation
        df['hybrid_score'] = (
            df['content_score'] * 0.7 +
            df['rating_norm'] * 0.3
        )

    else:
        # Merge collaborative results
        df2 = pd.DataFrame(collab)

        merged = pd.merge(df, df2, on="title", how="left")
        merged.fillna(0, inplace=True)

        merged['rating_norm'] = merged['rating'] / 10

        merged['hybrid_score'] = (
            merged['content_score'] * 0.5 +
            merged['collab_score'] * 0.3 +
            merged['rating_norm'] * 0.2
        )

        df = merged

    # Sort by hybrid score
    df = df.sort_values("hybrid_score", ascending=False)

    return df.head(top_n)'''