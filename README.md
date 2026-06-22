# Byeori

**Local AI-powered Media Indexing & Semantic Search Engine**

Byeori는 로컬 환경에서 사진과 영상을 색인(Indexing)하고, AI 임베딩을 이용해 의미 기반 검색(Semantic Search)을 제공하는 프로젝트입니다.

모든 처리는 로컬에서 수행되며, 클라우드 업로드 없이 개인 미디어를 검색하고 관리하는 것을 목표로 합니다.

---

다음과 같은 질의를 사용합니다.

```
노을 사진

강아지가 뛰는 장면

바다가 보이는 풍경

웃고 있는 사람
```

---

## Current Features

### Image Indexing

* SHA256 기반 파일 식별
* 이미지 메타데이터 추출
* CLIP 임베딩 생성
* GPU(CUDA) 지원
* Qdrant Vector Database 저장

### Search

* Text → Image Search
* Image → Image Search

### Similarity Detection

* SHA256 기반 완전 중복 탐지
* CLIP 기반 유사 이미지 탐지
* 유사 이미지 그룹 생성

### Report

* JSON Report
* HTML Report

---

## Available Scripts

| Script | Description |
|---------|-------------|
| scripts/index_photos.py | 이미지 색인 |
| scripts/search_text.py | 텍스트 기반 이미지 검색 |
| scripts/search_image.py | 이미지 기반 유사 이미지 검색 |
| scripts/find_exact_duplicates.py | 완전 중복 탐지 |
| scripts/find_similar_photos.py | 유사 사진 탐지 |
| scripts/group_similar_photos.py | 유사 사진 그룹 생성 |
| scripts/report_photos.py | JSON 리포트 생성 |
| scripts/report_html.py | HTML 리포트 생성 |

---

## Architecture

```text
Image
   │
   ▼
SHA256
   │
   ▼
Metadata
   │
   ▼
CLIP Embedding
   │
   ▼
Qdrant
   │
   ├───────────────┐
   │               │
   ▼               ▼
Text Search   Image Search
        │
        ▼
Similarity Search
        │
        ▼
Duplicate Grouping
        │
        ▼
JSON / HTML Report
```

---

Getting Started
'''text
Requirements
Python 3.12+
Docker
NVIDIA GPU (Optional)
CUDA 12.x (Optional)
uv'''

1. Clone Repository
'''bash
git clone https://github.com/notyetsmart/byeori.git
cd byeori'''

2. Install Dependencies
'''bash
uv sync'''

또는

'''bash
uv pip install -r requirements.txt'''

3. Start Qdrant
docker run -d \
  --name byeori-qdrant \
  -p 6433:6333 \
  -p 6434:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant

4. Prepare Images
검색할 이미지를 test_photos/ 폴더에 넣습니다.
'''text
test_photos/
├── 1.jpg
├── 2.jpg
└── ...'''


5. Index Images
'''bash
uv run python -m scripts.index_photos'''

6. Search by Text
'''bash
uv run python -m scripts.search_text'''

예시

'''bash
검색어를 입력하세요: sunset'''

7. Search by Image
'''bash
uv run python -m scripts.search_image'''

예시

'''bash
검색할 이미지 경로를 입력하세요: test_photos/3.jpg'''

8. Generate Report
- JSON 리포트 생성
'''bash
uv run python -m scripts.report_photos'''

- HTML 리포트 생성

'''bash
uv run python -m scripts.report_html'''

---

## Current Project Structure

```text
byeori/

app/
├── db/
├── embedding/
└── indexing/

scripts/

legacy/

reports/
```

---

## Technology Stack

* Python
* PyTorch
* SentenceTransformers
* CLIP (ViT-B-32)
* Qdrant
* Docker
* uv

---

## Roadmap

### Phase 1

* [x] Image Indexing
* [x] Metadata Extraction
* [x] CLIP Embedding
* [x] Qdrant Integration
* [x] Text Search
* [x] Image Search
* [x] Similar Image Detection
* [x] Similar Image Grouping
* [x] JSON Report
* [x] HTML Report

### Phase 2

* [ ] Service Layer Refactoring
* [ ] FastAPI
* [ ] REST API
* [ ] Background Indexing

### Phase 3

* [ ] Web UI
* [ ] Thumbnail Cache
* [ ] Drag & Drop Upload
* [ ] Real-time Search

### Phase 4

* [ ] Video Indexing
* [ ] OCR
* [ ] Face Clustering
* [ ] EXIF Search
* [ ] Speech Recognition
* [ ] LLM-powered Semantic Search

---

## Status

Current Status: **Prototype**

현재는 이미지 색인과 검색 기능을 우선 구현하고 있으며, 향후 영상 색인과 Web UI를 추가할 예정입니다.