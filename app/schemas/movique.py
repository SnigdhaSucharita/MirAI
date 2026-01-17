from pydantic import BaseModel
from typing import List

class MovieItem(BaseModel):
    id: int
    title: str
    overview: str

class MovieSearchPayload(BaseModel):
    query: str
    movies: List[MovieItem]


class WatchlistMovie(BaseModel):
    id: int
    title: str
    overview: str

class WatchlistRecommendationPayload(BaseModel):
    watchlist: List[WatchlistMovie]
    candidates: List[WatchlistMovie]


class ReviewInsightsRequest(BaseModel):
    movie_id: int
    reviews: List[str]

class ThemeInsight(BaseModel):
    theme: str
    sentiment: str
    examples: List[str]

class ReviewInsightsResponse(BaseModel):
    movie_id: int
    sentiment_summary: dict
    top_praises: List[str]
    top_criticisms: List[str]
    themes: List[ThemeInsight]
