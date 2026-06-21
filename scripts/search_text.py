from app.db.qdrant import get_qdrant_client
from app.embedding.clip import embed_text, embed_texts


COLLECTION_NAME = "byeori_photos"


def main():
    query = input("검색어를 입력하세요: ").strip()

    print(query)
    print(type(query))

    if not query:
        print("검색어가 비어 있습니다.")
        return

    client = get_qdrant_client()

    vector = embed_text(query)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector.tolist(),
        limit=5,
        with_payload=True,
    )

    results = response.points

    print(f"\nquery: {query}")
    print(f"results: {len(results)}")

    for i, result in enumerate(results, start=1):
        payload = result.payload or {}

        print("=" * 80)
        print(f"[{i}] score: {result.score}")
        print(f"id: {result.id}")
        print(f"filename: {payload.get('filename')}")
        print(f"path: {payload.get('path')}")
        print(f"size: {payload.get('width')} x {payload.get('height')}")
        print(f"format: {payload.get('image_format')}")
        print(f"sha256: {payload.get('sha256')}")


if __name__ == "__main__":
    main()