from pathlib import Path
from typing import Iterable

import numpy as np
import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

MODEL_NAME = "clip-ViT-B-32"

_model: SentenceTransformer | None = None

def get_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"

def get_model() -> SentenceTransformer:
    global _model

    if _model is None:
        device = get_device()
        print(f"loading CLIP model: {MODEL_NAME} on {device}")
        _model = SentenceTransformer(MODEL_NAME, device=device)

    return _model

def load_image(path: Path) -> Image.Image:
    with Image.open(path) as img:
        return img.convert("RGB").copy()

def embed_image(path: Path) -> np.ndarray:
    model = get_model()
    image = load_image(path)

    return model.encode(
        image,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

def embed_images(paths: Iterable[Path]) -> np.ndarray:
    model = get_model()
    images = [load_image(path) for path in paths]

    return model.encode(
        images,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

def embed_text(text: str) -> np.ndarray:
    model = get_model()

    text = str(text).strip()

    vectors = model.encode(
        [text],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return vectors[0]

def embed_texts(texts: Iterable[str]) -> np.ndarray:
    model = get_model()

    return model.encode(
        list(texts),
        convert_to_numpy=True,
        normalize_embeddings=True
    )