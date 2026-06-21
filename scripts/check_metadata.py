from pathlib import Path
from pprint import pprint

from app.indexing.hash import compute_sha256
from app.indexing.metadata import extract_image_metadata


def main():
    path = Path("test_photos/1.jpg")

    file_hash = compute_sha256(path)
    metadata = extract_image_metadata(path, file_hash)

    pprint(metadata)


if __name__ == "__main__":
    main()