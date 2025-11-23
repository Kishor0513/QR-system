import csv
import os
import re
import json
from pathlib import Path

try:
    import qrcode
except ImportError:
    qrcode = None

ROOT = Path(__file__).parent
CSV_DIR = ROOT / "csvs"
SITE_DIR = ROOT / "site"
DATA_DIR = SITE_DIR / "data"
QR_DIR = SITE_DIR / "qrcodes"

NAME_FIELD = "Product Name"
URL_FIELD = "Product Image Website Link"
LABEL_FIELD = "Product label (3-5 Characters)"
DESC_FIELD = "Description"

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
    return text.strip('-') or "item"

def read_csv(path: Path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return []
    header = [re.sub(r"\s+", " ", h).strip() for h in rows[0]]
    out = []
    for r in rows[1:]:
        if not any(x.strip() for x in r):
            continue
        if len(r) < len(header):
            r += ["" for _ in range(len(header)-len(r))]
        d = {header[i]: r[i].strip() for i in range(len(header))}
        if not d.get(NAME_FIELD):
            continue
        out.append(d)
    return out

def gather():
    products = []
    for csv_file in sorted(CSV_DIR.glob('*.csv')):
        products.extend(read_csv(csv_file))
    return products

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    QR_DIR.mkdir(parents=True, exist_ok=True)
    products_raw = gather()
    seen = set()

    # base URL placeholder (update after deploy)
    base_url = os.environ.get('SITE_BASE_URL', 'https://example.com/products/')

    export = []
    for p in products_raw:
        name = p.get(NAME_FIELD, '').strip()
        label = p.get(LABEL_FIELD, '').strip()
        slug_source = label or name
        slug = slugify(slug_source)
        if slug in seen:
            slug = f"{slug}-{len(seen)+1}"
        seen.add(slug)
        product_page_url = f"{base_url}?p={slug}"
        if qrcode is not None:
            img = qrcode.make(product_page_url)
            img.save(QR_DIR / f"{slug}.png")
        export.append({
            'slug': slug,
            'name': name,
            'code': label,
            'url': p.get(URL_FIELD, ''),
            'description': p.get(DESC_FIELD, ''),
            'fields': {f: p.get(f, '') for f in SHOW_FIELDS},
        })

    (DATA_DIR / 'products.json').write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote {len(export)} products to {DATA_DIR / 'products.json'}")
    if qrcode is None:
        print("Install qrcode to generate PNG QR codes (pip install qrcode Pillow)")
    else:
        print(f"Generated QR PNGs in {QR_DIR}")

if __name__ == '__main__':
    main()
