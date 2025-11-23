"""Deprecated build script.

This project now uses a simplified static JSON + single-page architecture.
Please use `python scripts/build.py` instead of this legacy script.

Keeping this file for reference; invoking it will exit immediately.
"""

import sys

sys.exit("build_site.py is deprecated. Run: python scripts/build.py")

# Legacy code retained below for reference (not executed).
import csv
import os
import re
from pathlib import Path
from typing import List, Dict

try:
    import qrcode
except ImportError:
    print("Error: 'qrcode' library not found. Please run: pip install -r requirements.txt")
    sys.exit(1)

ROOT = Path(__file__).parent
CSV_DIR = ROOT / "csvs"
SITE_DIR = ROOT / "site"
PRODUCT_PAGES_DIR = SITE_DIR / "products"
QRCODE_DIR = SITE_DIR / "qrcodes"
ASSETS_DIR = SITE_DIR / "assets"

HEADERS_TO_SHOW = [
    "Product Name",
    "Product label (3-5 Characters)",
    "Category Name",
    "Processes",
    "Weight (gm)",
    "Cost Price (Nrs)",
    "HS CODE",
    "Description",
    "Variations Color Code",
    "Tags",
    "Attributes",
    "Additional Category",
    "Occassion",
    "Type",
    "stock",
]

PRODUCT_URL_FIELD = "Product Image Website Link"
IMAGE_URL_FIELD = "Image Link"
LABEL_FIELD = "Product label (3-5 Characters)"
NAME_FIELD = "Product Name"
SN_FIELD = "SN"

PLACEHOLDER_IMAGE_PATH = "assets/placeholder.jpg"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip('-') or "item"


def read_csv_file(path: Path) -> List[Dict[str, str]]:
    rows = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            raw_rows = list(reader)
    except Exception as e:
        print(f"Error reading {path.name}: {e}")
        return []

    if not raw_rows:
        return rows
    
    # Merge multi-line header parts: Some headers have embedded newlines inside quotes already handled by csv
    header = raw_rows[0]
    # Clean header cells
    cleaned_header = [re.sub(r"\s+", " ", h).strip() for h in header]
    
    for r in raw_rows[1:]:
        if len(r) == 0:
            continue
        # Pad row if shorter
        if len(r) < len(cleaned_header):
            r = r + ["" for _ in range(len(cleaned_header) - len(r))]
        
        row_dict = {cleaned_header[i]: r[i].strip() for i in range(len(cleaned_header))}
        
        # Skip rows with no product name
        name = row_dict.get(NAME_FIELD, "").strip()
        if not name:
            continue
            
        rows.append(row_dict)
    return rows


def gather_products() -> List[Dict[str, str]]:
    all_products: List[Dict[str, str]] = []
    if not CSV_DIR.exists():
        print(f"Warning: CSV directory not found at {CSV_DIR}")
        return []
        
    for csv_file in sorted(CSV_DIR.glob("*.csv")):
        print(f"Processing {csv_file.name}...")
        all_products.extend(read_csv_file(csv_file))
    return all_products


def ensure_dirs():
    PRODUCT_PAGES_DIR.mkdir(parents=True, exist_ok=True)
    QRCODE_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def generate_qr(url: str, out_path: Path):
    if not url:
        return
    img = qrcode.make(url)
    img.save(out_path)


def create_placeholder_image():
    placeholder_path = ASSETS_DIR / "placeholder.jpg"
    if not placeholder_path.exists():
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (400, 400), color='#e1e1e1')
            d = ImageDraw.Draw(img)
            # Draw a simple cross or text if font is available, otherwise just a colored box
            d.rectangle([100, 180, 300, 220], fill='#999999')
            d.rectangle([180, 100, 220, 300], fill='#999999')
            img.save(placeholder_path)
            print(f"Created placeholder image at {placeholder_path}")
        except ImportError:
            print("Warning: Pillow not installed. Cannot create placeholder image.")
        except Exception as e:
            print(f"Warning: Could not create placeholder image: {e}")


def product_page_html(product: Dict[str, str], page_url: str) -> str:
    name = product.get(NAME_FIELD, "Unnamed Product")
    img_url = product.get(IMAGE_URL_FIELD, "")
    product_url = product.get(PRODUCT_URL_FIELD, "")
    label = product.get(LABEL_FIELD, "")
    category = product.get("Category Name", "")
    description = product.get("Description", "")
    weight = product.get("Weight (gm)", "")
    price = product.get("Cost Price (Nrs)", "")
    processes = product.get("Processes", "")
    attributes = product.get("Attributes", "")
    
    # Use placeholder if no image link
    display_img_url = img_url if img_url else f"../{PLACEHOLDER_IMAGE_PATH}"
    
    img_block = f"<img src='{display_img_url}' alt='{name}' class='product-image' onerror=\"this.src='../{PLACEHOLDER_IMAGE_PATH}'\">"
    
    info_rows = []
    if label:
        info_rows.append(f"<div class='info-row'><span class='label'>Product Code:</span><span class='value'>{label}</span></div>")
    if category:
        info_rows.append(f"<div class='info-row'><span class='label'>Category:</span><span class='value'>{category}</span></div>")
    if weight:
        info_rows.append(f"<div class='info-row'><span class='label'>Weight:</span><span class='value'>{weight}g</span></div>")
    if price:
        info_rows.append(f"<div class='info-row'><span class='label'>Price:</span><span class='value'>Rs. {price}</span></div>")
    if processes:
        info_rows.append(f"<div class='info-row'><span class='label'>Process:</span><span class='value'>{processes}</span></div>")
    if attributes:
        info_rows.append(f"<div class='info-row'><span class='label'>Attributes:</span><span class='value'>{attributes}</span></div>")
    
    desc_block = f"<p class='description'>{description}</p>" if description else ""
    
    return f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>{name} - Felt & Yarn</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.container {{
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    max-width: 600px;
    width: 100%;
    overflow: hidden;
}}
.header {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    text-align: center;
}}
.header h1 {{
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 8px;
}}
.header .subtitle {{
    font-size: 14px;
    opacity: 0.9;
}}
.content {{
    padding: 30px;
}}
.product-image {{
    width: 100%;
    max-height: 400px;
    object-fit: contain;
    background-color: #f8f9fa;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}
.description {{
    color: #444;
    line-height: 1.6;
    margin-bottom: 24px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}}
.info-grid {{
    display: grid;
    gap: 12px;
    margin-bottom: 24px;
}}
.info-row {{
    display: flex;
    justify-content: space-between;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 8px;
    transition: transform 0.2s;
}}
.info-row:hover {{
    transform: translateX(4px);
    background: #e9ecef;
}}
.info-row .label {{
    font-weight: 600;
    color: #667eea;
}}
.info-row .value {{
    color: #333;
}}
.cta-button {{
    display: block;
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    text-decoration: none;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-top: 24px;
}}
.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}}
.footer {{
    padding: 20px;
    text-align: center;
    background: #f8f9fa;
    color: #666;
    font-size: 12px;
}}
@media (max-width: 640px) {{
    .header h1 {{ font-size: 22px; }}
    .content {{ padding: 20px; }}
}}
</style>
</head>
<body>
<div class='container'>
    <div class='header'>
        <h1>{name}</h1>
        <div class='subtitle'>Felt & Yarn Handmade Products</div>
    </div>
    <div class='content'>
        {img_block}
        {desc_block}
        <div class='info-grid'>
            {''.join(info_rows)}
        </div>
        {f"<a href='{product_url}' class='cta-button' target='_blank'>🛒 View Full Details & Purchase</a>" if product_url else "<div class='cta-button' style='background:#ccc; cursor:not-allowed;'>Link Not Available</div>"}
    </div>
    <div class='footer'>
        Scanned from Felt & Yarn QR Code
    </div>
</div>
</body>
</html>"""


def index_html(products_meta: List[Dict[str, str]]) -> str:
    rows = []
    for p in products_meta:
        if p['url']:
            link_cell = f"<a href='{p['url']}' target='_blank'>Link</a>"
        else:
            link_cell = "<span style='color:#888;'>No URL</span>"
        rows.append(f"<tr><td>{p['sn']}</td><td><a href='products/{p['slug']}.html'>{p['name']}</a></td><td>{p['label']}</td><td>{p['category']}</td><td>{link_cell}</td></tr>")
    return f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Products QR Index</title>
<style>
body {{ font-family: Arial, sans-serif; margin:24px; }}
input[type=search] {{ padding:8px; width:320px; margin-bottom:16px; }}
th, td {{ padding:6px 8px; border-bottom:1px solid #eee; text-align:left; }}
th {{ background:#f4f4f4; }}
.table-wrapper {{ overflow-x:auto; }}
</style>
</head>
<body>
<h1>Products QR Index</h1>
<p>Search and open a product page to view details and QR code.</p>
<input type='search' id='search' placeholder='Search by name, label, category...'>
<div class='table-wrapper'>
<table id='products' style='border-collapse:collapse; width:100%;'>
<thead><tr><th>SN</th><th>Name</th><th>Label</th><th>Category</th><th>URL</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</div>
<script>
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', () => {{
  const term = searchInput.value.toLowerCase();
  for (const row of document.querySelectorAll('#products tbody tr')) {{
    const text = row.innerText.toLowerCase();
    row.style.display = text.includes(term) ? '' : 'none';
  }}
}});
</script>
<footer style='margin-top:40px; font-size:12px; color:#666;'>Generated static index - Felt & Yarn QR System</footer>
</body>
</html>"""


def main():
    print("Starting site generation...")
    ensure_dirs()
    create_placeholder_image()
    
    products = gather_products()
    if not products:
        print("No products found in CSV files.")
        return

    products_meta = []
    
    # Deployment Configuration
    # For Netlify, we want to use the environment variable if available, otherwise default
    NETLIFY_SITE = os.environ.get("URL", "https://feltandyarn-qr.netlify.app")
    BASE_URL = f"{NETLIFY_SITE}/products/"
    
    print(f"Using Base URL for QR Codes: {BASE_URL}")

    count = 0
    for product in products:
        name = product.get(NAME_FIELD, "").strip()
        if not name:
            continue
        product_url = product.get(PRODUCT_URL_FIELD, "").strip()
        label = product.get(LABEL_FIELD, "").strip()
        sn = product.get(SN_FIELD, "").strip()
        category = product.get("Category Name", "").strip()
        base_slug_source = label or name
        slug = slugify(base_slug_source)
        
        # Guarantee uniqueness
        original_slug = slug
        counter = 1
        while any(p['slug'] == slug for p in products_meta):
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # QR points to OUR page
        page_url = f"{BASE_URL}{slug}.html"
        qr_filename = f"{slug}.png"
        qr_path = QRCODE_DIR / qr_filename
        
        # Generate QR
        generate_qr(page_url, qr_path)
        
        page_html = product_page_html(product, page_url)
        (PRODUCT_PAGES_DIR / f"{slug}.html").write_text(page_html, encoding="utf-8")
        
        products_meta.append({
            'slug': slug,
            'name': name,
            'label': label,
            'sn': sn,
            'category': category,
            'url': product_url,
        })
        count += 1
        if count % 100 == 0:
            print(f"Generated {count} pages...")

    (SITE_DIR / "index.html").write_text(index_html(products_meta), encoding="utf-8")
    print(f"Successfully generated {len(products_meta)} product pages in {SITE_DIR}")
    print(f"Ready for Netlify deployment.")

if __name__ == "__main__":
    main()
