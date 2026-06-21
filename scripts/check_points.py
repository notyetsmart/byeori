from app.db.qdrant import get_qdrant_client


COLLECTION_NAME = "byeori_photos"


def main():
    client = get_qdrant_client()

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