from pydantic import BaseModel
from typing import List, Optional

class ImageItem(BaseModel):
    imageUrl: str
    description: Optional[str] = None


class PicstoriaSemanticRequest(BaseModel):
    query: str
    images: List[ImageItem]


class SmartTagRequest(BaseModel):
    image_url: str
    existing_tags: List[str]


class ColorPaletteRequest(BaseModel):
    image_path: str
    num_colors: int = 6

class RecommendImageRequest(BaseModel):
    image_url: str
    image_pool: List[ImageItem]
    top_k: int
    score_threshold: float

class AnalyzeImageRequest(BaseModel):
    image_url: str

