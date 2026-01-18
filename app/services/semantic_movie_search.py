from app.services.semantic import cosine_similarity
from app.models.clip_model import encode_text

def semantic_movie_search(query: str, movies: list, min_score: float = 0.25):
    texts = [query] + [
        f"{movie.title}. {movie.overview}"
        for movie in movies
    ]

    embeddings = encode_text(texts)
    query_vec = embeddings[0]
    movie_vecs = embeddings[1:]

    scored = []
    for movie, vec in zip(movies, movie_vecs):
        score = cosine_similarity(query_vec, vec)

        if score >= min_score:
            scored.append({
                "id": movie.id,
                "title": movie.title,
                "score": float(score)
            })

    return sorted(scored, key=lambda x: x["score"], reverse=True)
