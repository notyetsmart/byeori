from pathlib import Path

from qdrant_client.models import PointStruct

from app.db.qdrant import COLLECTION_NAME, get_qdrant_client, ensure_collection
from app.embedding.clip import embed_image
from app.indexing.hash import compute_sha256, uuid_from_sha256
from app.indexing.metadata import extract_image_metadata


def main():
    path = Path("test_photos/1.jpg")

    client = get_qdrant_client()
    ensure_collection(client)

    file_hash = compute_sha256(path)
    point_id = uuid_from_sha256(file_hash)

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
    print(f"id: {point_id}")
    print(f"sha256: {file_hash}")


if __name__ == "__main__":
    main()