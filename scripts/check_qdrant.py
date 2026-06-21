from app.db.qdrant import (
    COLLECTION_NAME,
    get_qdrant_client,
    ensure_collection,
    count_points,
)


def main():
    client = get_qdrant_client()

    ensure_collection(client)

    count = count_points(client)

    print(f"collection: {COLLECTION_NAME}")
    print(f"points: {count}")


if __name__ == "__main__":
    main()