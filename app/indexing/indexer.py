from pathlib import Path
from typing import Iterable

from qdrant_client.models import PointStruct

from app.db.qdrant import COLLECTION_NAME
from app.embedding.clip import embed_image
from app.indexing.hash import compute_sha256, uuid_from_sha256
from app.indexing.metadata import extract_image_metadata


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def iter_image_paths(folder: Path) -> list[Path]:
    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def point_exists(client, point_id: str) -> bool:
    result = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[point_id],
    )
    return len(result) > 0


def index_image(client, path: Path) -> bool:
    file_hash = compute_sha256(path)
    point_id = uuid_from_sha256(file_hash)

    if point_exists(client, point_id):
        print(f"skip: {path}")
        return False

    metadata = extract_image_metadata(path, file_hash)
    vector = embed_image(path)

    point = PointStruct(
        id=point_id,
        vector=vector.tolist(),
        payload=metadata,
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )

    print(f"indexed: {path}")
    return True


def index_folder(client, folder: Path) -> tuple[int, int]:
    paths = iter_image_paths(folder)

    indexed = 0
    skipped = 0

    print(f"found images: {len(paths)}")

    for path in paths:
        if index_image(client, path):
            indexed += 1
        else:
            skipped += 1

    return indexed, skipped