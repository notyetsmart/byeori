from pathlib import Path

from app.embedding.clip import embed_image, embed_text, get_device


def main():
    image_path = Path("test_photos/1.jpg")

    print(f"device: {get_device()}")

    image_vector = embed_image(image_path)
    text_vector = embed_text("a photo")

    print(f"image vector shape: {image_vector.shape}")
    print(f"text vector shape: {text_vector.shape}")
    print(f"image vector norm: {(image_vector ** 2).sum() ** 0.5:.4f}")
    print(f"text vector norm: {(text_vector ** 2).sum() ** 0.5:.4f}")


if __name__ == "__main__":
    main()