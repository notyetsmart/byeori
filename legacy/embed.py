import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _model = SentenceTransformer("clip-ViT-B-32", device=device)
    return _model

def embed_images(images):
    model = get_model()
    pil = [im if isinstance(im, Image.Image) else Image.open(im).convert("RGB")
           for im in images]
    return model.encode(pil, convert_to_numpy=True, normalize_embeddings=True)

def embed_texts(texts):
    model = get_model()
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)