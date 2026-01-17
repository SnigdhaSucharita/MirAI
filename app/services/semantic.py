from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple

# Load model ONCE at startup
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Convert texts into normalized embeddings
    """
    return model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True
    )


import numpy as np


def cosine_similarity(vectors, query_vector):
    """
    vectors: np.ndarray (N, D) OR (D,)
    query_vector: np.ndarray (D,)
    """

    vectors = np.array(vectors)
    query_vector = np.array(query_vector)

    # Normalize
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
    embeddings = embed_texts(texts)

    query_vec = embeddings[0]
    candidate_vecs = embeddings[1:]

    results = []

    for candidate, vec in zip(candidates, candidate_vecs):
        score = cosine_similarity(query_vec, vec)
        results.append({"candidate": candidate, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)

    if top_k is not None:
        results = results[:top_k]

    return results