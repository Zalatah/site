from __future__ import annotations

import json
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "source"
IMAGE_DIR = ROOT / "assets" / "images"
PRODUCT_DIR = IMAGE_DIR / "products"
MENU_PATH = ROOT / "menu_bilingual.json"
MENU_DATA_PATH = ROOT / "menu-data.js"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "product"


def source_name(url: str) -> str:
    path = unquote(urlparse(url).path)
    return Path(path).name


def product_stem(image_path: str) -> str:
    stem = Path(source_name(image_path)).stem
    stem = re.sub(r"(?:-(?:256|320|480|960|1200))+$", "", stem)
    return slugify(stem)


def fit_width(image: Image.Image, width: int) -> Image.Image:
    target_width = min(width, image.width)
    if target_width == image.width:
        return image.copy()
    height = round(image.height * target_width / image.width)
    return image.resize((target_width, height), Image.Resampling.LANCZOS)


def save_webp(source: Path, destination: Path, width: int, quality: int = 78) -> None:
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        resized = fit_width(image, width)
        destination.parent.mkdir(parents=True, exist_ok=True)
        resized.save(destination, "WEBP", quality=quality, method=6)


def archive_top_level_images() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for path in ROOT.iterdir():
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            destination = SOURCE_DIR / path.name
            if destination.exists():
                path.unlink()
            else:
                shutil.move(str(path), str(destination))


def optimize_brand_assets() -> None:
    save_webp(SOURCE_DIR / "cover.png", IMAGE_DIR / "cover-720.webp", 720, 80)
    save_webp(SOURCE_DIR / "cover.png", IMAGE_DIR / "cover-1200.webp", 1200, 82)
    save_webp(SOURCE_DIR / "zalatah_logo.png", IMAGE_DIR / "logo-164.webp", 164, 74)
    shutil.copy2(SOURCE_DIR / "Zalatah Fav.png", IMAGE_DIR / "favicon.png")


def optimize_products() -> None:
    menu = json.loads(MENU_PATH.read_text(encoding="utf-8"))
    generated: set[str] = set()
    source_by_stem = {
        slugify(path.stem): path
        for path in SOURCE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    }

    for category in menu:
        for product in category.get("products", []):
            stem = product_stem(product.get("image", ""))
            source = source_by_stem.get(stem)

            small = f"assets/images/products/{stem}-480.webp"
            card = f"assets/images/products/{stem}-256.webp"
            medium = f"assets/images/products/{stem}-960.webp"
            large = f"assets/images/products/{stem}-1200.webp"
            product["imageCard"] = card
            product["imageSmall"] = small
            product["image"] = medium
            product["imageLarge"] = large

            if source is None or stem in generated:
                continue

            save_webp(source, ROOT / card, 256, 64)
            save_webp(source, ROOT / small, 480, 74)
            save_webp(source, ROOT / medium, 960, 78)
            save_webp(source, ROOT / large, 1200, 80)
            generated.add(stem)

    MENU_PATH.write_text(
        json.dumps(menu, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_menu_data(menu)


def write_menu_data(menu: list[dict]) -> None:
    payload = json.dumps(menu, ensure_ascii=False, separators=(",", ":"))
    MENU_DATA_PATH.write_text(
        f"window.ZALATAH_MENU_DATA={payload};\n",
        encoding="utf-8",
    )


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
    archive_top_level_images()
    optimize_brand_assets()
    optimize_products()


if __name__ == "__main__":
    main()
