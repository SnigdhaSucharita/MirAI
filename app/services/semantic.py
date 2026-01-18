import numpy as np
from typing import List, Tuple
from app.models.clip_model import encode_text


def cosine_similarity(vectors, query_vector):
    vectors = np.array(vectors)
    query_vector = np.array(query_vector)

    vectors_norm = np.linalg.norm(vectors, axis=-1, keepdims=True)
    query_norm = np.linalg.norm(query_vector)

    similarity = np.dot(vectors, query_vector) / (
        vectors_norm.squeeze() * query_norm
    )

    return similarity.tolist()


def semantic_rank(
    query: str,
    candidates: List[str],
    top_k: int | None = None
) -> List[Tuple[str, float]]:

    texts = [query] + candidates

    embeddings = encode_text(texts).cpu().numpy()

    query_vec = embeddings[0]
    candidate_vecs = embeddings[1:]

    results = []

    for candidate, vec in zip(candidates, candidate_vecs):
        score = float(np.dot(query_vec, vec))  # cosine similarity
        results.append({"candidate": candidate, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)

    if top_k is not None:
        results = results[:top_k]

    return results
