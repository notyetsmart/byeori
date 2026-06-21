from app.db.qdrant import get_qdrant_client


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

    uf = UnionFind()
    point_map = {}

    for point in points:
        uf.add(str(point.id))
        point_map[str(point.id)] = point

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

    similar_groups = [
        group for group in groups.values()
        if len(group) >= 2
    ]

    print(f"\nsimilar groups: {len(similar_groups)}")

    for i, group in enumerate(similar_groups, start=1):
        print("=" * 80)
        print(f"Group {i}")
        print(f"count: {len(group)}")

        for point_id in group:
            point = point_map[point_id]
            payload = point.payload or {}

            print(f"- {payload.get('filename')}")
            print(f"  {payload.get('path')}")


if __name__ == "__main__":
    main()