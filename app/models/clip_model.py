import torch
import clip
from PIL import Image
from app.core.config import DEVICE

model, preprocess = clip.load("ViT-B/32", device=DEVICE)
model.eval()


def encode_image(image_path: str) -> torch.Tensor:
    image = preprocess(
        Image.open(image_path).convert("RGB")
    ).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)

    return embedding.squeeze(0)


def encode_text(texts: list[str]) -> torch.Tensor:
    tokens = clip.tokenize(texts).to(DEVICE)

    with torch.no_grad():
        embedding = model.encode_text(tokens)
        embedding /= embedding.norm(dim=-1, keepdim=True)

    return embedding

