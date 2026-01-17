from app.services.semantic import embed_texts, cosine_similarity


def validate_folder(
    document_text: str,
    target_folder: dict,
    available_folders: list,
    threshold: float
):

    doc_embedding = embed_texts([document_text])[0]


    target_embedding = embed_texts([target_folder["description"]])[0]
    target_score = cosine_similarity(doc_embedding, target_embedding)


    best_folder = target_folder["name"]
    best_score = target_score

    for folder in available_folders:
        folder_embedding = embed_texts([folder["description"]])[0]
        score = cosine_similarity(doc_embedding, folder_embedding)

        if score > best_score:
            best_score = score
            best_folder = folder["name"]

    is_valid = target_score >= threshold and best_folder == target_folder["name"]

    explanation = (
        f"This document aligns with {best_folder} "
        f"based on its semantic content."
    )

    return {
        "is_valid": is_valid,
        "confidence": round(float(target_score), 2),
        "suggested_folder": None if is_valid else best_folder,
        "explanation": explanation
    }
