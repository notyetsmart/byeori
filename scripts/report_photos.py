import json
from pathlib import Path
from collections import defaultdict
from app.db.qdrant import get_qdrant_client

REPORT_DIR = Path("reports")
REPORT_PATH = REPORT_DIR / "photo_report.json"

COLLECTION_NAME = "byeori_photos"
SIMILAR_THRESHOLD = 0.80


class UnionFind:
    def __init__(self):
        self.parent = {}

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        self.add(a)
        self.add(b)

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            self.parent[root_b] = root_a


def find_exact_duplicates(points):
    sha_groups = defaultdict(list)

    for point in points:
        payload = point.payload or {}
        sha256 = payload.get("sha256")

        if sha256:
            sha_groups[sha256].append(payload)

    return [
        group for group in sha_groups.values()
        if len(group) >= 2
    ]


def find_similar_groups(client, points):
    uf = UnionFind()
    point_map = {}

    for point in points:
        point_id = str(point.id)
        uf.add(point_id)
        point_map[point_id] = point

    for point in points:
        if point.vector is None:
            continue

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=point.vector,
            limit=10,
            with_payload=True,
        )

        for result in response.points:
            if result.id == point.id:
                continue

            if result.score >= SIMILAR_THRESHOLD:
                uf.union(str(point.id), str(result.id))

    groups = {}

    for point_id in point_map:
        root = uf.find(point_id)
        groups.setdefault(root, []).append(point_id)

    return [
        [point_map[point_id] for point_id in group]
        for group in groups.values()
        if len(group) >= 2
    ]

def find_similar_pairs(client, points):
    pairs = {}

    for point in points:
        if point.vector is None:
            continue

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=point.vector,
            limit=10,
            with_payload=True,
        )

        for result in response.points:
            if result.id == point.id:
                continue

            if result.score >= SIMILAR_THRESHOLD:
                pair_key = tuple(sorted([str(point.id), str(result.id)]))

                pairs[pair_key] = {
                    "score": result.score,
                    "a": {
                        "id": str(point.id),
                        "filename": (point.payload or {}).get("filename"),
                        "path": (point.payload or {}).get("path"),
                    },
                    "b": {
                        "id": str(result.id),
                        "filename": (result.payload or {}).get("filename"),
                        "path": (result.payload or {}).get("path"),
                    },
                }

    return list(pairs.values())


def main():
    client = get_qdrant_client()

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=True,
    )

    print("=" * 80)
    print("Byeori Photo Report")
    print("=" * 80)
    print(f"total photos: {len(points)}")
    print(f"similar threshold: {SIMILAR_THRESHOLD}")

    exact_duplicates = find_exact_duplicates(points)
    similar_groups = find_similar_groups(client, points)
    similar_pairs = find_similar_pairs(client, points)

    print("\n[Exact Duplicates]")
    print(f"groups: {len(exact_duplicates)}")

    if not exact_duplicates:
        print("none")

    for i, group in enumerate(exact_duplicates, start=1):
        print("-" * 80)
        print(f"Duplicate Group {i}")
        print(f"count: {len(group)}")
        print(f"sha256: {group[0].get('sha256')}")

        for payload in group:
            print(f"- {payload.get('filename')}")
            print(f"  {payload.get('path')}")

    print("\n[Similar Pairs]")
    print(f"pairs: {len(similar_pairs)}")

    if not similar_pairs:
        print("none")

    for i, pair in enumerate(similar_pairs, start=1):
        print("-" * 80)
        print(f"Pair {i}")
        print(f"score: {pair['score']}")
        print(f"A: {pair['a']['filename']}")
        print(f"   {pair['a']['path']}")
        print(f"B: {pair['b']['filename']}")
        print(f"   {pair['b']['path']}")

    print("\n[Similar Groups]")
    print(f"groups: {len(similar_groups)}")

    if not similar_groups:
        print("none")

    for i, group in enumerate(similar_groups, start=1):
        print("-" * 80)
        print(f"Similar Group {i}")
        print(f"count: {len(group)}")

        for point in group:
            payload = point.payload or {}
            print(f"- {payload.get('filename')}")
            print(f"  {payload.get('path')}")

    report = {
        "total_photos": len(points),
        "similar_threshold": SIMILAR_THRESHOLD,
        "exact_duplicates": [
            [
                {
                    "filename": payload.get("filename"),
                    "path": payload.get("path"),
                    "sha256": payload.get("sha256"),
                }
                for payload in group
            ]
            for group in exact_duplicates
        ],
        "similar_pairs": similar_pairs,
        "similar_groups": [
            [
                {
                    "id": str(point.id),
                    "filename": (point.payload or {}).get("filename"),
                    "path": (point.payload or {}).get("path"),
                    "sha256": (point.payload or {}).get("sha256"),
                }
                for point in group
            ]
            for group in similar_groups
        ],
    }

    REPORT_DIR.mkdir(exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nJSON report saved: {REPORT_PATH}")

if __name__ == "__main__":
    main()