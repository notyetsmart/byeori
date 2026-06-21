from pathlib import Path
import mimetypes

from PIL import Image


def extract_image_metadata(path: Path, file_hash: str) -> dict:
    path = path.resolve()
    stat = path.stat()

    with Image.open(path) as img:
        width, height = img.size
        image_format = img.format

    mime_type, _ = mimetypes.guess_type(path)

    return {
        "path": str(path),
        "filename": path.name,
        "extension": path.suffix.lower(),
        "filesize": stat.st_size,
        "width": width,
        "height": height,
        "image_format": image_format,
        "mime_type": mime_type,
        "sha256": file_hash,
    }