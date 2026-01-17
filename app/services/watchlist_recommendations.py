import numpy as np
from app.services.semantic import embed_texts, cosine_similarity

def explain_recommendation(candidate_vec, watchlist, watchlist_embeddings):
    similarities = [
        cosine_similarity(candidate_vec, w_vec)
        for w_vec in watchlist_embeddings
    ]

    best_idx = int(np.argmax(similarities))
    best_movie = watchlist[best_idx]

    return f"Similar to '{best_movie.title}' in tone and theme."


def recommend_from_watchlist(
    watchlist: list,
    candidates: list,
    min_score: float = 0.25,
    diversity_threshold: float = 0.85
):
    watchlist_texts = [
        f"{movie.title}. {movie.overview}"
        for movie in watchlist
    ]

    candidate_texts = [
        f"{movie.title}. {movie.overview}"
        for movie in candidates
    ]

    watchlist_embeddings = embed_texts(watchlist_texts)
    candidate_embeddings = embed_texts(candidate_texts)

    taste_vector = np.mean(watchlist_embeddings, axis=0)

    ranked = []
    for movie, vec in zip(candidates, candidate_embeddings):
        score = cosine_similarity(taste_vector, vec)

        if score >= min_score:
            ranked.append({
                "movie": movie,
                "vector": vec,
                "score": score
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    final_results = []
    selected_vectors = []

    for item in ranked:
        if any(
            cosine_similarity(item["vector"], v) > diversity_threshold
            for v in selected_vectors
        ):
            continue 

        explanation = explain_recommendation(
            item["vector"],
            watchlist,
            watchlist_embeddings
        )

        final_results.append({
            "id": item["movie"].id,
            "title": item["movie"].title,
            "score": float(item["score"]),
            "explanation": explanation
        })

        selected_vectors.append(item["vector"])

    return final_results

