from pathlib import Path

from app.indexing.hash import compute_sha256, uuid_from_sha256


def main():
    path = Path("test_photos/1.jpg")

    file_hash = compute_sha256(path)
    point_id = uuid_from_sha256(file_hash)

    print(f"path: {path}")
    print(f"sha256: {file_hash}")
    print(f"uuid: {point_id}")


if __name__ == "__main__":
    main()