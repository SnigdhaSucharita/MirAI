import numpy as np
import os
import tempfile
import requests
from pathlib import Path

from app.schemas.picstoria import ImageItem
from app.models.clip_model import encode_image
from app.utils.image_loader import download_image


def recommend_images(
    query_image_url: str,
    image_pool: list[ImageItem],
    top_k: int = 5,
    score_threshold: float = 0.25
):

    query_image_path = download_image(query_image_url)
    query_vec = encode_image(query_image_path)
    os.remove(query_image_path)

    results = []

    for image in image_pool:
        try:
            candidate_path = download_image(image.imageUrl)
            candidate_vec = encode_image(candidate_path)
            os.remove(candidate_path)

            score = float(np.dot(query_vec, candidate_vec))

            if score >= score_threshold:
                results.append({
                    "imageUrl": image.imageUrl,
                    "description": image.description,
                    "altDescription": image.altDescription,
                    "score": score
                })

        except Exception:
            continue  

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

