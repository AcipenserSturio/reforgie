from pathlib import Path
from PIL import Image

def to_dds(image_path: Path, art_path: Path, key: str):
    Image.open(image_path).save(art_path / key)
    return key
