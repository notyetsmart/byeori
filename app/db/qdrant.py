from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


QDRANT_URL = "http://localhost:6433"
COLLECTION_NAME = "byeori_photos"
VECTOR_SIZE = 512


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def collection_exists(client: QdrantClient, collection_name: str = COLLECTION_NAME) -> bool:
    collections = client.get_collections().collections
    return any(collection.name == collection_name for collection in collections)


def ensure_collection(
    client: QdrantClient,
    collection_name: str = COLLECTION_NAME,
    vector_size: int = VECTOR_SIZE,
) -> None:
    if collection_exists(client, collection_name):
        print(f"collection exists: {collection_name}")
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )

    print(f"collection created: {collection_name}")


def count_points(
    client: QdrantClient,
    collection_name: str = COLLECTION_NAME,
) -> int:
    result = client.count(
        collection_name=collection_name,
        exact=True,
    )
    return result.count