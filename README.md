# Byeori

Byeori is a local AI-powered media indexing and semantic search prototype.

It indexes images on a local machine using SHA256, metadata extraction, CLIP embeddings, and Qdrant vector database.

## Current Features

- Image indexing
- SHA256-based exact duplicate detection
- Metadata extraction
- CLIP image embeddings
- Qdrant vector storage
- Text-to-image search
- Image-to-image similarity search
- Similar image pair detection
- Similar image grouping
- JSON report generation
- HTML report generation

## Pipeline

```text
Image
  ↓
SHA256
  ↓
Metadata
  ↓
CLIP Embedding
  ↓
Qdrant
  ↓
Search / Similarity / Report
```

## Tech Stack

- Python
- PyTorch
- SentenceTransformers
- CLIP
- Qdrant
- Docker
- uv

## Example Result

```
Similar Pairs
Pair 1
score: 0.8437455
A: 3.jpg
B: 5.jpg
```

## Roadmap

[-] Image indexing
[-] Text-to-image search
[-] Image-to-image search
[-] Similar image grouping
[-] JSON / HTML report
[] Refactor into service modules
[] Web API
[] Web UI
[] Video indexing
[] OCR
[] Face clustering

## Status

This project is currently an early prototype.