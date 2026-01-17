from typing import List, Dict
from app.services.semantic import semantic_rank
from app.utils.chunking import sentence_chunk


def check_chunk_level_duplication(
    document_text: str,
    existing_documents: List[str],
    threshold: float = 0.65,
    top_k: int = 3
) -> Dict:
    """
    Checks chunk-level semantic duplication against existing documents.
    """

    # 1. Chunk the incoming document
    chunks = sentence_chunk(document_text)

    if not chunks:
        return {
            "is_duplicate": False,
            "duplication_ratio": 0.0,
            "duplicated_chunks": []
        }

    duplicated_chunks = []

    # 2. Compare each chunk independently
    for idx, chunk in enumerate(chunks):
        ranked = semantic_rank(
            query=chunk,
            candidates=existing_documents,
            top_k=top_k
        )

        matches = [
            {
                "matched_document": r["candidate"],
                "score": r["score"]
            }
            for r in ranked
            if r["score"] >= threshold
        ]

        if matches:
            duplicated_chunks.append({
                "chunk_index": idx,
                "chunk_text": chunk,
                "matches": matches
            })

    # 3. Correct duplication ratio
    duplication_ratio = round(
        len(duplicated_chunks) / len(chunks),
        2
    )

    return {
        "is_duplicate": duplication_ratio > 0,
        "duplication_ratio": duplication_ratio,
        "duplicated_chunks": duplicated_chunks
    }


