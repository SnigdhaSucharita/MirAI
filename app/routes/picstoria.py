from fastapi import APIRouter

from app.schemas.picstoria import PicstoriaSemanticRequest, SmartTagRequest, ColorPaletteRequest, AnalyzeImageRequest, RecommendImageRequest

from app.services.semantic import cosine_similarity
from app.models.clip_model import encode_text
from app.services.smart_tags import suggest_smart_tags
from app.services.image_recommendation import recommend_images
from app.services.color_palette import extract_color_palette

router = APIRouter(prefix="/picstoria", tags=["Picstoria"])


@router.post("/semantic-search")
def picstoria_semantic_search(payload: PicstoriaSemanticRequest):
    """
    Re-rank Unsplash images based on semantic similarity
    """

    texts = [payload.query] + [img.description or img.altDescription or "" for img in payload.images]

    embeddings = encode_text(texts)

    query_vector = embeddings[0]
    image_vectors = embeddings[1:]

    results = []

    for img, vector in zip(payload.images, image_vectors):
        score = cosine_similarity(query_vector, vector)
        results.append({
            "imageUrl": img.imageUrl,
            "description": img.description,
            "altDescription": img.altDescription,
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


@router.post("/smart-tags")
def picstoria_smart_tags(payload: SmartTagRequest):
    
    tag_candidates = suggest_smart_tags(payload.image_url)

    existing = {t.lower().strip() for t in payload.existing_tags}

    filtered_tags = [
        tag for tag in tag_candidates
        if tag.lower().strip() not in existing
    ]

    return {
        "suggested_tags": filtered_tags
    }


@router.post("/recommend-images")
def image_recommendations(payload: RecommendImageRequest):
    image_candidates = recommend_images(
        query_image_url=payload.image_url,
        image_pool=payload.image_pool,
        top_k=payload.top_k,
        score_threshold=payload.score_threshold
    )

    return {
        "images": image_candidates
    }


@router.post("/color-palette")
def color_palette(payload: ColorPaletteRequest):
    palette = extract_color_palette(
        image_path=payload.image_path,
        num_colors=payload.num_colors
    )

    return {
        "palette": palette
    }


@router.post("/analyze-image")
def analyze_image(payload: AnalyzeImageRequest):
    """
    Computes once at photo save time
    """

    color_palette = extract_color_palette(payload.image_url)

    suggested_tags = suggest_smart_tags(
        image_url=payload.image_url,
        score_threshold=0.22,
        max_tags=8,
        
    )

    return {
        "colorPalette": color_palette,
        "suggestedTags": suggested_tags,
    }
