import csv
import json
import os
import re
import socket
from pathlib import Path
from typing import List, Dict

try:
    import qrcode
except ImportError:
    qrcode = None

ROOT = Path(__file__).parent
CSV_DIR = ROOT / "csvs"
SITE_DIR = ROOT / "site"
QRCODE_DIR = SITE_DIR / "qrcodes"

# CSV Field Mappings
NAME_FIELD = "Product Name"
LABEL_FIELD = "Product label (3-5 Characters)"
PRODUCT_URL_FIELD = "Product Image Website Link"
IMAGE_URL_FIELD = "Image Link"
SN_FIELD = "SN"

# ==========================================
# CONFIGURATION
# ==========================================
# Set this to your public URL when hosting (e.g., "https://yourname.github.io/qr-system/")
# Leave as None to auto-detect local IP for testing
PUBLIC_BASE_URL = None 
# Example: PUBLIC_BASE_URL = "https://keyshowor.github.io/QR-system/"
# ==========================================

def get_base_url():
    if PUBLIC_BASE_URL:
        return PUBLIC_BASE_URL.rstrip('/') + "/index.html?id="
    
    # Auto-detect local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        s.close()
    except Exception:
        IP = 'localhost'
    return f"http://{IP}:8080/index.html?id="

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip('-') or "item"

def read_csv_file(path: Path) -> List[Dict[str, str]]:
    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        raw_rows = list(reader)
    if not raw_rows:
        return rows
    
    header = raw_rows[0]
    cleaned_header = [re.sub(r"\s+", " ", h).strip() for h in header]
    
    for r in raw_rows[1:]:
        if not r: continue
        if len(r) < len(cleaned_header):
            r = r + ["" for _ in range(len(cleaned_header) - len(r))]
        row_dict = {cleaned_header[i]: r[i].strip() for i in range(len(cleaned_header))}
        
        name = row_dict.get(NAME_FIELD, "").strip()
        url = row_dict.get(PRODUCT_URL_FIELD, "").strip()
        if not name and not url:
            continue
        rows.append(row_dict)
    return rows

def gather_products() -> List[Dict[str, str]]:
    all_products = []
    for csv_file in sorted(CSV_DIR.glob("*.csv")):
        print(f"Processing {csv_file.name}...")
        all_products.extend(read_csv_file(csv_file))
    return all_products

def ensure_dirs():
    SITE_DIR.mkdir(exist_ok=True)
    QRCODE_DIR.mkdir(parents=True, exist_ok=True)

def generate_qr(url: str, out_path: Path):
    if qrcode:
        img = qrcode.make(url)
        img.save(out_path)

def main():
    ensure_dirs()
    products = gather_products()
    
    base_url = get_base_url()
    print(f"Generating QR codes pointing to: {base_url}[slug]")
    
    processed_products = []
    seen_slugs = set()
    
    for p in products:
        name = p.get(NAME_FIELD, "").strip()
        label = p.get(LABEL_FIELD, "").strip()
        sn = p.get(SN_FIELD, "").strip()
        
        # Generate unique slug
        base_slug = slugify(label or name)
        slug = base_slug
        counter = 1
        while slug in seen_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        seen_slugs.add(slug)
        
        # Add slug to product data
        p['id'] = slug
        processed_products.append(p)
        
        # Generate QR
        qr_url = f"{base_url}{slug}"
        generate_qr(qr_url, QRCODE_DIR / f"{slug}.png")
        
    # Write JSON
    json_path = SITE_DIR / "products.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(processed_products, f, indent=2)
        
    print(f"Successfully generated {len(processed_products)} products in {json_path}")
    print(f"QR Codes generated in {QRCODE_DIR}")

if __name__ == "__main__":
    main()
