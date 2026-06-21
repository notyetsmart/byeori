from app.db.qdrant import get_qdrant_client


COLLECTION_NAME = "byeori_photos"
SIMILAR_THRESHOLD = 0.80


def main():
    client = get_qdrant_client()

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=True,
    )

    print(f"loaded points: {len(points)}")
    print(f"threshold: {SIMILAR_THRESHOLD}")

    pairs = []

    for point in points:
        if point.vector is None:
            continue

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=point.vector,
            limit=5,
            with_payload=True,
        )

        for result in response.points:
            if result.id == point.id:
                continue

            if result.score >= SIMILAR_THRESHOLD:
                a = point.payload or {}
                b = result.payload or {}

                pair_key = tuple(sorted([str(point.id), str(result.id)]))

                pairs.append(
                    {
                        "pair_key": pair_key,
                        "score": result.score,
                        "a_filename": a.get("filename"),
                        "a_path": a.get("path"),
                        "b_filename": b.get("filename"),
                        "b_path": b.get("path"),
                    }
                )

    unique_pairs = {}
    for pair in pairs:
        unique_pairs[pair["pair_key"]] = pair

    print(f"\nsimilar pairs: {len(unique_pairs)}")

    for i, pair in enumerate(unique_pairs.values(), start=1):
        print("=" * 80)
        print(f"[{i}] score: {pair['score']}")
        print(f"A: {pair['a_filename']}")
        print(f"   {pair['a_path']}")
        print(f"B: {pair['b_filename']}")
        print(f"   {pair['b_path']}")


if __name__ == "__main__":
    main()