from pathlib import Path

from app.db.qdrant import get_qdrant_client, ensure_collection, count_points
from app.indexing.indexer import index_folder


def main():
    folder = Path("test_photos")

    client = get_qdrant_client()
    ensure_collection(client)

    indexed, skipped = index_folder(client, folder)
    total = count_points(client)

    print()
    print("done")
    print(f"indexed: {indexed}")
    print(f"skipped: {skipped}")
    print(f"total points: {total}")
from app.db.qdrant import get_client


COLLECTION_NAME = "byeori_photos"


def main():
    client = get_client()

    points, next_page = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10,
        with_payload=True,
        with_vectors=True,
    )

    print(f"loaded points: {len(points)}")
    print(f"next_page: {next_page}")

    for i, point in enumerate(points, start=1):
        print("=" * 80)
        print(f"[{i}] point id:")
        print(point.id)

        print("\nvector:")
        if point.vector is None:
            print("None")
        else:
            print(f"type: {type(point.vector)}")
            print(f"dimension: {len(point.vector)}")
            print(f"first 5 values: {point.vector[:5]}")

        print("\npayload:")
        for key, value in point.payload.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()