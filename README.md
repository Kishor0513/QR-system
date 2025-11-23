# Felt & Yarn QR Static Site

Generates a static site (`site/`) with:

- `index.html`: searchable table of all products from all CSVs in `csvs/`.
- Individual product pages: details + image + link + QR code PNG.
- `qrcodes/`: PNG QR codes pointing to the product web URL.

## Requirements

- Python 3.8+
- Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the build script from the project root:

```powershell
python build_site.py
```

This will create / update the `site/` directory.
Open `site/index.html` in a browser (double-click or drag into browser).

## Notes

- Rows without a product name and URL are skipped.
- If `qrcode` is not installed, pages are generated but QR images are missing.
- Slugs are based on product label or name; uniqueness ensured by appending SN if needed.

## Regenerate After CSV Change

Just rerun:

```powershell
python build_site.py
```

## Printing Single Product Pages

Each product page hides navigation when printing for clean QR + details output.
