from fastapi import APIRouter
from app.schemas.semantic import SemanticRankRequest, RankedResult
from app.services.semantic import semantic_rank

router = APIRouter(prefix="/semantic", tags=["Semantic"])


@router.post("/rank", response_model=list[RankedResult])
def create_semantic_rank(payload: SemanticRankRequest):
     return semantic_rank(
        query=payload.query,
        candidates=payload.candidate,
        top_k=payload.top_k
    )
