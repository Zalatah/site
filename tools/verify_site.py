from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"
MENU_PATH = ROOT / "menu_bilingual.json"
EXPECTED_MISSING_PRODUCTS = {"Orange Juice", "Avocado Shake"}
ALLOWED_EXTERNAL_HOSTS = {
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "umami.zylor.space",
    "www.pass2u.net",
    "maps.app.goo.gl",
    "tiktok.com",
    "www.instagram.com",
    "wa.me",
}
BANNED_RUNTIME_MARKERS = {
    "menux",
    "menxu",
    "jquery",
    "owl.carousel",
    "smush",
    "shortpixel",
    "raw.githubusercontent.com",
    "cdn.jsdelivr.net",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
}
LAYOUT_READ_MARKERS = {
    "getBoundingClientRect",
    "getComputedStyle",
    "offsetHeight",
    "offsetWidth",
    "scrollHeight",
    "scrollWidth",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    menu = json.loads(MENU_PATH.read_text(encoding="utf-8"))
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    styles = (ROOT / "styles.css").read_text(encoding="utf-8")
    menu_data = (ROOT / "menu-data.js").read_text(encoding="utf-8")

    products = [product for category in menu for product in category.get("products", [])]
    if len(menu) != 7:
        fail(f"expected 7 categories, found {len(menu)}")
    if len(products) != 32:
        fail(f"expected 32 products, found {len(products)}")

    combined_runtime = "\n".join(
        (html, app, styles, menu_data, MENU_PATH.read_text(encoding="utf-8"))
    )
    for marker in BANNED_RUNTIME_MARKERS:
        if marker.lower() in combined_runtime.lower():
            fail(f"banned runtime dependency marker remains: {marker}")

    if 'rel="preload"\n      href="styles.css"\n      as="style"' not in html:
        fail("main stylesheet is not loaded through a non-blocking preload")
    if "this.rel='stylesheet'" not in html:
        fail("preloaded stylesheet does not promote itself after loading")

    for marker in LAYOUT_READ_MARKERS:
        if marker in app:
            fail(f"layout-sensitive JavaScript read remains: {marker}")

    external_urls = re.findall(r'https://([^/"\s]+)', combined_runtime)
    unknown_hosts = sorted(set(external_urls) - ALLOWED_EXTERNAL_HOSTS)
    if unknown_hosts:
        fail(f"unexpected external hosts: {', '.join(unknown_hosts)}")

    missing_products: set[str] = set()
    for product in products:
        for field in ("imageCard", "imageSmall", "image", "imageLarge"):
            relative_path = product.get(field)
            if not relative_path:
                fail(f"{product['title']['en']} is missing {field}")
            if not (ROOT / relative_path).exists():
                missing_products.add(product["title"]["en"])

    if missing_products != EXPECTED_MISSING_PRODUCTS:
        fail(
            "unexpected missing product assets: "
            + ", ".join(sorted(missing_products))
        )

    required_local_files = {
        "app.js",
        "menu-data.js",
        "styles.css",
        "assets/fonts/saudi-riyal.woff2",
        "assets/images/cover-720.webp",
        "assets/images/cover-1200.webp",
        "assets/images/logo-164.webp",
        "assets/images/favicon.png",
    }
    missing_required = sorted(path for path in required_local_files if not (ROOT / path).exists())
    if missing_required:
        fail("missing required local files: " + ", ".join(missing_required))

    runtime_images = list((ROOT / "assets" / "images").rglob("*"))
    runtime_bytes = sum(path.stat().st_size for path in runtime_images if path.is_file())
    source_bytes = sum(path.stat().st_size for path in (ROOT / "assets" / "source").iterdir() if path.is_file())
    card_images = list((ROOT / "assets" / "images" / "products").glob("*-256.webp"))
    card_bytes = sum(path.stat().st_size for path in card_images)
    if len(card_images) != 29:
        fail(f"expected 29 optimized card images, found {len(card_images)}")
    if card_bytes > 200_000:
        fail(f"optimized card images exceed 200 KB: {card_bytes}")

    print("PASS")
    print(f"categories={len(menu)}")
    print(f"products={len(products)}")
    print(f"intentional_missing_products={len(missing_products)}")
    print(f"runtime_image_bytes={runtime_bytes}")
    print(f"card_image_bytes={card_bytes}")
    print(f"archived_source_bytes={source_bytes}")


if __name__ == "__main__":
    main()
