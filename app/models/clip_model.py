import torch
torch.set_num_threads(1)
import clip
import numpy as np
from PIL import Image

DEVICE = "cpu"

_model = None
_preprocess = None


def get_clip_model():
    global _model, _preprocess

    if _model is None:
        _model, _preprocess = clip.load("ViT-B/32", device=DEVICE)
        _model.eval()

    return _model, _preprocess


def encode_image(image_path: str) -> np.ndarray:
    model, preprocess = get_clip_model()

    image = preprocess(
        Image.open(image_path).convert("RGB")
    ).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)

    return embedding.squeeze(0).cpu().numpy()



def encode_text(texts: list[str]) -> np.ndarray:
    model, _ = get_clip_model()

    tokens = clip.tokenize(texts).to(DEVICE)

    with torch.no_grad():
        embedding = model.encode_text(tokens)
        embedding /= embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy()



def encode_single_text(text: str) -> np.ndarray:
    return encode_text([text])[0]


