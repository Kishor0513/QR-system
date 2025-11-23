# Felt & Yarn QR Static Site

Static product info site built from CSV files. Current architecture:

- `scripts/build.py`: Aggregates all `csvs/*.csv` -> `site/data/products.json` and pre-generates QR PNGs.
- `site/index.html`: JS-driven searchable grid of products (loads JSON).
- `site/product.html`: Dynamic single product page driven by query param `?p=<slug>`.
- `site/qrcodes/`: PNG QR codes pointing to deployed `product.html?p=<slug>` URLs.

Legacy generator `build_site.py` is deprecated (multi-page HTML approach) and now exits immediately.

## Requirements

- Python 3.8+
- Optional: `qrcode` and `Pillow` for PNG QR generation.

Install (optional dependencies for QR images):

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Build

```powershell
python scripts/build.py
```

Environment override for deployed base URL (recommended before final QR generation):

```powershell
$env:SITE_BASE_URL = "https://your-site.netlify.app"
python scripts/build.py
```

If `SITE_BASE_URL` is unset, a placeholder `https://example.com` is used.

## Using the Site

Open `site/index.html` locally or deploy the entire `site/` folder (Netlify, GitHub Pages, etc.).
Scanning a QR opens `product.html?p=<slug>` showing product details.

## Regenerating After CSV Changes

Run the build again:

```powershell
python scripts/build.py
```

## Notes

- Products without a name are skipped.
- Slug uniqueness ensured by suffix numbering (`slug`, `slug-2`, ...).
- If `qrcode` lib missing, JSON still builds; PNGs are skipped.

## Troubleshooting

- Ensure CSV headers are consistent; unexpected header changes create empty fields.
- Delete stale QR PNGs if removing many products (`Remove-Item site\qrcodes\*.png`). Re-run build.

## Deployment (Netlify)

Set `SITE_BASE_URL` in Netlify environment variables to your public domain (Netlify supplies `URL`).
Deploy the prebuilt `site/` directory; no server-side code required.

## Printing

Use browser print on `product.html?p=<slug>` for a clean QR + details sheet.
