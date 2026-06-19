from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU_PATH = ROOT / "menu_bilingual.json"
OUTPUT_PATH = ROOT / "menu-data.js"


def main() -> None:
    menu = json.loads(MENU_PATH.read_text(encoding="utf-8"))
    payload = json.dumps(menu, ensure_ascii=False, separators=(",", ":"))
    OUTPUT_PATH.write_text(
        f"window.ZALATAH_MENU_DATA={payload};\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
