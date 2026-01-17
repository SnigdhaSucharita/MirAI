import numpy as np
from typing import List

def mmr_select_sentences(
    doc_embedding: np.ndarray,
    sentence_embeddings: List[np.ndarray],
    sentences: List[str],
    top_k: int = 5,
    lambda_param: float = 0.7
) -> List[str]:
    """
    Maximal Marginal Relevance for extractive summarization
    """

    selected_sentences = []
    selected_indices = []

    similarity_to_doc = [
        float(np.dot(sent_emb, doc_embedding))
        for sent_emb in sentence_embeddings
    ]

    while len(selected_sentences) < min(top_k, len(sentences)):
        mmr_scores = []

        for i in range(len(sentences)):
            if i in selected_indices:
                mmr_scores.append(-np.inf)
                continue

            redundancy = 0.0
            if selected_indices:
                redundancy = max(
                    float(np.dot(sentence_embeddings[i], sentence_embeddings[j]))
                    for j in selected_indices
                )

            score = (
                lambda_param * similarity_to_doc[i]
                - (1 - lambda_param) * redundancy
            )
            mmr_scores.append(score)

        best_idx = int(np.argmax(mmr_scores))
        selected_indices.append(best_idx)
        selected_sentences.append(sentences[best_idx])

    return selected_sentences
