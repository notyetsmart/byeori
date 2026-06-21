from pathlib import Path

from app.db.qdrant import get_qdrant_client
from app.embedding.clip import embed_image


COLLECTION_NAME = "byeori_photos"


def main():
    image_path = input("검색할 이미지 경로를 입력하세요: ").strip()
    path = Path(image_path).expanduser().resolve()

    if not path.exists():
        print(f"파일이 존재하지 않습니다: {path}")
        return

    client = get_qdrant_client()

    vector = embed_image(path)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector.tolist(),
        limit=5,
        with_payload=True,
    )

    results = response.points

    print(f"\nquery image: {path}")
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