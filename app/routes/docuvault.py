from fastapi import APIRouter
from app.schemas.docuvault import SemanticDocumentSearchRequest, SmartFolderValidationRequest, DuplicationRequest, SummarisationRequest, SummarisationResponse
from app.services.semantic import semantic_rank
from app.services.smart_folder_validation import validate_folder
from app.services.duplication_check import check_chunk_level_duplication
from app.services.summarisation import summarize_document

router = APIRouter(prefix="/docuvault", tags=["Docuvault"])


@router.post("/semantic-search")
def semantic_document_search(payload: SemanticDocumentSearchRequest):
    return semantic_rank(
        query=payload.query,
        candidates=payload.documents,
        top_k=payload.top_k
    )


@router.post("/smart-folder-validation")
def smart_folder_validation(payload: SmartFolderValidationRequest):
    return validate_folder(
        document_text=payload.document_text,
        target_folder=payload.target_folder.dict(),
        available_folders=[f.dict() for f in payload.available_folders],
        threshold=payload.threshold
    )


@router.post("/duplication-check")
def duplication_check(req: DuplicationRequest):
    return check_chunk_level_duplication(
        document_text=req.document_text,
        existing_documents=req.existing_documents,
        threshold=req.threshold,
        top_k=req.top_k
    )


@router.post(
    "/summarize",
    response_model=SummarisationResponse
)
def summarize(payload: SummarisationRequest):
    return summarize_document(
        text=payload.document_text,
        top_k=payload.max_sentences
    )