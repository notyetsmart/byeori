from pathlib import Path
from embed import embed_images

folder = Path("./test_photos")
paths = sorted(p for p in folder.iterdir()
               if p.suffix.lower() in (".jpg", ".jpeg", ".png"))

emb = embed_images(paths)   # (N, 512), 이미 정규화됨
sim = emb @ emb.T           # 정규화 벡터의 내적 = 코사인 유사도

print("\n=== 유사도 (1.0에 가까울수록 비슷) ===")
for i in range(len(paths)):
    for j in range(i + 1, len(paths)):
        s = float(sim[i, j])
        flag = " <- 중복 후보" if s > 0.92 else ""
        print(f"{paths[i].name:22} vs {paths[j].name:22} : {s:.3f}{flag}")