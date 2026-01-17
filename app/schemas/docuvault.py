from pydantic import BaseModel
from typing import List, Optional


class Document(BaseModel):
    id: str
    text: str


class SemanticDocumentSearchRequest(BaseModel):
    query: str
    documents: List[Document]
    top_k: int


class Folder(BaseModel):
    name: str
    description: str


class SmartFolderValidationRequest(BaseModel):
    document_text: str
    target_folder: Folder
    available_folders: List[Folder]
    threshold: float = 0.35


class DuplicationRequest(BaseModel):
    document_text: str
    existing_documents: List[str]
    threshold: float = 0.85
    top_k: int = 2


class SummarisationRequest(BaseModel):
    document_text: str
    max_sentences: int = 5


class SummarisationResponse(BaseModel):
    summary: str
    selected_sentences: List[str]
    method: str
    top_k: int
    lambda_: float
