from collections import defaultdict

from app.db.qdrant import get_qdrant_client


COLLECTION_NAME = "byeori_photos"


def main():
    client = get_qdrant_client()

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    print(f"loaded points: {len(points)}")

    sha_groups = defaultdict(list)

    for point in points:
        payload = point.payload or {}
        sha256 = payload.get("sha256")

        if not sha256:
            continue

        sha_groups[sha256].append(payload)

    duplicate_groups = [
        group for group in sha_groups.values()
        if len(group) >= 2
    ]

    print(f"exact duplicate groups: {len(duplicate_groups)}")

    for i, group in enumerate(duplicate_groups, start=1):
        print("=" * 80)
        print(f"Duplicate Group {i}")
        print(f"count: {len(group)}")
        print(f"sha256: {group[0].get('sha256')}")

        for payload in group:
            print(f"- {payload.get('filename')}")
            print(f"  {payload.get('path')}")


if __name__ == "__main__":
    main()