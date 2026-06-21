from pathlib import Path
import hashlib
import uuid


NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def uuid_from_sha256(file_hash: str) -> str:
    return str(uuid.uuid5(NAMESPACE, file_hash))