"""Static site build script (next-gen)

Reads all CSV files in ./csvs, aggregates product data into ./site/data/products.json,
pre-generates QR PNGs pointing to the deployed product detail page (product.html?p=slug),
and leaves legacy page generation behind.

Configuration:
  SITE_BASE_URL  Optional. Base public URL of the deployed site. Example:
                 https://feltandyarn-qr.netlify.app
                 If omitted, a placeholder https://example.com is used.

Resulting URLs for QR codes will be: <SITE_BASE_URL>/product.html?p=<slug>

Usage (PowerShell):
  python scripts/build.py

Dependencies:
  qrcode + Pillow (optional for PNG generation). If missing, script still builds JSON.

"""
from __future__ import annotations
import csv
import json
import os
import re
from pathlib import Path
from typing import Dict, List

try:
    import qrcode  # type: ignore
except ImportError:  # graceful fallback
    qrcode = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "csvs"
SITE_DIR = ROOT / "site"
DATA_DIR = SITE_DIR / "data"
QR_DIR = SITE_DIR / "qrcodes"

# Field constants
NAME_FIELD = "Product Name"
LABEL_FIELD = "Product label (3-5 Characters)"
URL_FIELD = "Product Image Website Link"
DESC_FIELD = "Description"
IMAGE_FIELD = "Image Link"

SHOW_FIELDS = [
    LABEL_FIELD,
    "Category Name",
    "Processes",
    "Weight (gm)",
    "Cost Price (Nrs)",
    "HS CODE",
    DESC_FIELD,
    "Attributes",
    "Occassion",
    "Type",
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "item"


def read_csv(path: Path) -> List[Dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"[WARN] Failed reading {path.name}: {e}")
        return []
    if not rows:
        return []
    header = [re.sub(r"\s+", " ", h).strip() for h in rows[0]]
    out: List[Dict[str, str]] = []
    for raw in rows[1:]:
        if not any(cell.strip() for cell in raw):
            continue
        if len(raw) < len(header):
            raw += ["" for _ in range(len(header) - len(raw))]
        d = {header[i]: raw[i].strip() for i in range(len(header))}
        if not d.get(NAME_FIELD):
            continue
        out.append(d)
    return out


def gather_products() -> List[Dict[str, str]]:
    products: List[Dict[str, str]] = []
    if not CSV_DIR.exists():
        print(f"[ERROR] CSV directory missing: {CSV_DIR}")
        return products
    for csv_file in sorted(CSV_DIR.glob("*.csv")):
        print(f"[INFO] Loading {csv_file.name}")
        products.extend(read_csv(csv_file))
    return products


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    QR_DIR.mkdir(parents=True, exist_ok=True)


def compute_base_url() -> str:
    base = os.environ.get("SITE_BASE_URL", "https://example.com")
    base = base.rstrip("/")
    return f"{base}/product.html"


def unique_slug(existing_counts: Dict[str, int], base: str) -> str:
    count = existing_counts.get(base, 0)
    if count == 0:
        existing_counts[base] = 1
        return base
    new_slug = f"{base}-{count+1}"
    existing_counts[base] = count + 1
    return new_slug


def build():
    ensure_dirs()
    all_products = gather_products()
    if not all_products:
        print("[INFO] No products discovered. Exiting.")
        return

    product_page_base = compute_base_url()
    print(f"[INFO] Product page base: {product_page_base}?p=<slug>")

    slug_counts: Dict[str, int] = {}
    export: List[Dict[str, str]] = []

    qr_enabled = qrcode is not None
    if not qr_enabled:
        print("[WARN] qrcode not installed; skipping PNG generation.")

    for p in all_products:
        name = p.get(NAME_FIELD, "").strip()
        label = p.get(LABEL_FIELD, "").strip()
        if not name:
            continue
        base_source = label or name
        base_slug = slugify(base_source)
        slug = unique_slug(slug_counts, base_slug)
        page_url = f"{product_page_base}?p={slug}"

        if qr_enabled:
            try:
                img = qrcode.make(page_url)
                img.save(QR_DIR / f"{slug}.png")
            except Exception as e:
                print(f"[WARN] QR generation failed for {slug}: {e}")

        export.append({
            "slug": slug,
            "name": name,
            "code": label,
            "url": p.get(URL_FIELD, ""),
            "image": p.get(IMAGE_FIELD, ""),
            "description": p.get(DESC_FIELD, ""),
            "fields": {f: p.get(f, "") for f in SHOW_FIELDS},
        })

    data_path = DATA_DIR / "products.json"
    data_path.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[SUCCESS] Wrote {len(export)} products -> {data_path}")
    if qr_enabled:
        print(f"[SUCCESS] QR PNGs generated -> {QR_DIR}")
    print("[DONE] Static data build complete.")


if __name__ == "__main__":  # script entry
    build()
