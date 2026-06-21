import hashlib
import uuid
from pathlib import Path
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from embed import embed_images

COLLECTION = "photos"
FOLDER = Path("test_photos")
BATCH = 16

client = QdrantClient(url="http://localhost:6433")

# 1. 컬렉션 없으면 생성 (CLIP = 512차원, 코사인 거리)
if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE),
    )
    print(f"컬렉션 '{COLLECTION}' 생성")

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def point_id(h):                       # 해시 → 결정적 UUID (같은 파일 = 같은 ID)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, h))

# 2. 폴더 스캔 + 해시 계산
paths = sorted(p for p in FOLDER.iterdir()
               if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
candidates = [(p, file_hash(p)) for p in paths]
ids = [point_id(h) for _, h in candidates]

# 3. 이미 색인된 것 골라내기 (증분 — 해시로 건너뛰기)
found = client.retrieve(collection_name=COLLECTION, ids=ids)
found_ids = {str(pt.id) for pt in found}
new_items = [(p, h, pid) for (p, h), pid in zip(candidates, ids)
             if pid not in found_ids]

print(f"전체 {len(paths)}장 / 신규 {len(new_items)}장 / 건너뜀 {len(paths) - len(new_items)}장")

# 4. 신규만 임베딩 + Qdrant 저장 (배치)
for i in range(0, len(new_items), BATCH):
    chunk = new_items[i:i + BATCH]
    vectors = embed_images([p for p, _, _ in chunk])
    points = []
    for (p, h, pid), vec in zip(chunk, vectors):
        w, hgt = Image.open(p).size
        points.append(PointStruct(
            id=pid,
            vector=vec.tolist(),
            payload={
                "path": str(p.resolve()),
                "filename": p.name,
                "hash": h,
                "width": w,
                "height": hgt,
                "size_bytes": p.stat().st_size,
            },
        ))
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"  {i + len(chunk)}/{len(new_items)} 저장")

print("색인 완료")
print(client.get_collection(COLLECTION))
