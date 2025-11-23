# Felt and Yarn QR Code System

A complete QR code generation system for Felt and Yarn products. Each product gets a unique QR code linking to a beautifully designed product detail page.

## Features

- ✨ **Automated CSV Processing**: Parses 34 product category CSV files
- 🔲 **QR Code Generation**: Creates unique QR codes for every product
- 🎨 **Premium Design**: Modern, attractive product pages with glassmorphism effects
- 📱 **Fully Responsive**: Beautiful on mobile, tablet, and desktop
- 🚀 **Netlify Ready**: One-command deployment

## Project Structure

```
QR-system/
├── csvs/                    # Source CSV files (34 category files)
├── scripts/                 # Build scripts
│   ├── parse-csvs.js       # CSV parser
│   ├── generate-qr-codes.js # QR code generator
│   └── generate-pages.js   # Page builder
├── public/                  # Generated static site
│   ├── css/                # Stylesheets
│   ├── product/            # Individual product pages
│   ├── qr-codes/           # Generated QR codes
│   ├── index.html          # Homepage
│   └── qr-index.html       # QR code gallery
├── data/                    # Generated product data
│   └── products.json       # Unified product database
├── package.json
├── netlify.toml
└── README.md
```

## Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Build the Site**
   ```bash
   npm run build
   ```

   This will:
   - Parse all CSV files into `data/products.json`
   - Generate QR codes in `public/qr-codes/`
   - Create individual product pages in `public/product/`

3. **Preview Locally**
   ```bash
   npm run dev
   ```
   Visit `http://localhost:8080`

## Individual Scripts

- **Parse CSVs Only**: `npm run parse-csv`
- **Generate QR Codes Only**: `npm run generate-qr`
- **Generate Pages Only**: `npm run generate-pages`

## Deployment to Netlify

### Option 1: Netlify CLI
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Option 2: Netlify Dashboard
1. Push this repository to GitHub
2. Connect repository to Netlify
3. Netlify will automatically detect `netlify.toml` and build

### Option 3: Drag & Drop
1. Run `npm run build`
2. Drag the `public/` folder to Netlify drop zone

## QR Code Usage

After deployment, each QR code will link to:
```
https://your-site.netlify.app/product/[product-id].html
```

**Note**: After first deployment, you may want to update the base URL in `scripts/generate-qr-codes.js` and rebuild to use your actual Netlify domain instead of a placeholder.

## Product Data Structure

Each product includes:
- Product Name
- Category and Subcategory
- Description
- Image (high-quality or placeholder)
- Weight, Processes, HS Code
- Original website link
- Tags and attributes
- Downloadable QR code

## Tech Stack

- **Vanilla JavaScript** for build scripts
- **HTML/CSS** for the static site
- **QRCode.js** for QR generation
- **CSV Parser** for data extraction
- **Netlify** for hosting

## License

MIT
