import torch
import clip

torch.set_num_threads(1)

model, preprocess = clip.load("ViT-B/32", device="cpu")
model.eval()

print("CLIP preloaded successfully")

