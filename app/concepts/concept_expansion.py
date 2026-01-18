from app.models.clip_model import encode_image, encode_text


def expand_concepts(image_path: str, candidate_concepts: list[str], top_k: int = 40):
    image_features = encode_image(image_path)          
    text_features = encode_text([f"a photo of {candidate_concept}" for candidate_concept in candidate_concepts])
              

    similarities = image_features @ text_features.T   

    scores = similarities.tolist()

    results = list(zip(candidate_concepts, scores))
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_k]

