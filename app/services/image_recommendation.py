import numpy as np
import tempfile
import requests
from pathlib import Path

from app.models.clip_model import encode_image
from app.utils.image_loader import download_image


def recommend_images(
    query_image_url: str,
    image_pool_urls: list[str],
    top_k: int = 5,
    score_threshold: float = 0.25
):

    query_image_path = download_image(query_image_url)
    query_vec = encode_image(query_image_path)
    os.remove(query_image_path)

    results = []

    for image_url in image_pool_urls:
        try:
            candidate_path = download_image(image_url)
            candidate_vec = encode_image(candidate_path)
            os.remove(candidate_path)

            score = float(np.dot(query_vec, candidate_vec))

            if score >= score_threshold:
                results.append({
                    "image_url": image_url,
                    "score": score
                })

        except Exception:
            continue  

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

