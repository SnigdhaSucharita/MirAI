from pydantic import BaseModel
from typing import List


class SemanticRankRequest(BaseModel):
    query: str
    candidates: List[str]


class RankedResult(BaseModel):
    text: str
    score: float

