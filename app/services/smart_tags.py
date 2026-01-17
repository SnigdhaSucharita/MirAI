from app.concepts.concept_expansion import expand_concepts
from app.concepts.concept_bank import EXPANSION_POOL
from app.utils.image_loader import download_image
import os


def suggest_smart_tags(
    image_url: str,
    score_threshold: float = 0.22,
    max_tags: int = 8
):
    image_path = download_image(image_url)

    expanded = expand_concepts(
        image_path=image_path,
        candidate_concepts=EXPANSION_POOL,
        top_k=40
    )

    tags = [
        concept
        for concept, score in expanded
        if score >= score_threshold
    ]

    os.remove(image_path)

    return tags[:max_tags]
