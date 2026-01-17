from pydantic import BaseModel
from typing import List

class ImageItem(BaseModel):
    imageUrl: str
    description: str
    altDescription: str


class PicstoriaSemanticRequest(BaseModel):
    query: str
    images: List[ImageItem]


class SmartTagRequest(BaseModel):
    image_url: str
    existing_tags: List[str]


class ColorPaletteRequest(BaseModel):
    image_path: str
    num_colors: int = 6


class AnalyzeImageRequest(BaseModel):
    image_url: str
