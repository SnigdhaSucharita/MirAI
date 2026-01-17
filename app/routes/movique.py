from fastapi import APIRouter
from app.schemas.movique import MovieSearchPayload, WatchlistRecommendationPayload, ReviewInsightsRequest, ReviewInsightsResponse
from app.services.semantic_movie_search import semantic_movie_search
from app.services.watchlist_recommendations import recommend_from_watchlist
from app.services.review_insights import build_review_insights

router = APIRouter(prefix="/movique", tags=["Movique"])

@router.post("/semantic-search")
def movie_semantic_search(payload: MovieSearchPayload):
    return semantic_movie_search(
        payload.query,
        payload.movies
    )


@router.post("/watchlist-recommendations")
def watchlist_recommendations(payload: WatchlistRecommendationPayload):
    return recommend_from_watchlist(
        payload.watchlist,
        payload.candidates
    )


@router.post(
    "/review-insights",
    response_model=ReviewInsightsResponse
)
def review_insights(payload: ReviewInsightsRequest):
    if not payload.reviews:
        raise HTTPException(
            status_code=400,
            detail="Reviews list cannot be empty"
        )

    return build_review_insights(
        movie_id=payload.movie_id,
        reviews=payload.reviews
    )