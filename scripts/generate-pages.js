const fs = require("fs");
const path = require("path");

const PRODUCTS_FILE = path.join(__dirname, "../data/products.json");
const OUTPUT_DIR = path.join(__dirname, "../public/product");
const BASE_URL = process.env.SITE_URL || "https://your-site.netlify.app";

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Helper to get image URL or placeholder
function getImageURL(product) {
  if (product.imageLink && product.imageLink.trim()) {
    return product.imageLink;
  }
  // Return null to use placeholder
  return null;
}

// Generate HTML for a single product
function generateProductHTML(product) {
  const imageURL = getImageURL(product);
  const imageHTML = imageURL
    ? `<img src="${imageURL}" alt="${product.name}" class="product-image-large" loading="lazy">`
    : `<div class="product-image-large placeholder-image">
             <span>📦 ${product.name}</span>
           </div>`;

  const websiteLink = product.websiteLink
    ? `<a href="${product.websiteLink}" target="_blank" class="btn btn-outline">
             View on Feltandyarn.com
           </a>`
    : "";

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${
      product.description || product.name + " - Felt and Yarn Product"
    }">
    <title>${product.name} | Felt and Yarn</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <nav>
        <div class="container">
            <a href="../index.html" class="logo">Felt & Yarn</a>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../qr-index.html">QR Codes</a></li>
            </ul>
        </div>
    </nav>

    <main class="product-detail">
        <div class="container">
            <div class="product-detail-container animate-in">
                <div class="product-image-section">
                    ${imageHTML}
                </div>

                <div class="product-info">
                    <div>
                        <span class="badge">${product.category}</span>
                        <h1>${product.name}</h1>
                        ${
                          product.description
                            ? `<p class="hero-subtitle">${product.description}</p>`
                            : ""
                        }
                    </div>

                    <div class="card">
                        <h3>Product Details</h3>
                        <div class="info-grid">
                            ${
                              product.label
                                ? `
                            <div class="info-item">
                                <span class="info-label">Product Code:</span>
                                <span class="info-value">${product.label}</span>
                            </div>`
                                : ""
                            }
                            
                            ${
                              product.category
                                ? `
                            <div class="info-item">
                                <span class="info-label">Category:</span>
                                <span class="info-value">${product.category}</span>
                            </div>`
                                : ""
                            }
                            
                            ${
                              product.weight
                                ? `
                            <div class="info-item">
                                <span class="info-label">Weight:</span>
                                <span class="info-value">${product.weight} gm</span>
                            </div>`
                                : ""
                            }
                            
                            ${
                              product.processes
                                ? `
                            <div class="info-item">
                                <span class="info-label">Processes:</span>
                                <span class="info-value">${product.processes}</span>
                            </div>`
                                : ""
                            }
                            
                            ${
                              product.hsCode
                                ? `
                            <div class="info-item">
                                <span class="info-label">HS Code:</span>
                                <span class="info-value">${product.hsCode}</span>
                            </div>`
                                : ""
                            }
                            
                            ${
                              product.tags
                                ? `
                            <div class="info-item">
                                <span class="info-label">Tags:</span>
                                <span class="info-value">${product.tags}</span>
                            </div>`
                                : ""
                            }
                            
                            ${
                              product.occasion
                                ? `
                            <div class="info-item">
                                <span class="info-label">Occasion:</span>
                                <span class="info-value">${product.occasion}</span>
                            </div>`
                                : ""
                            }
                        </div>
                    </div>

                    <div class="qr-section">
                        <h3>Scan to Share</h3>
                        <p class="text-muted mb-2">Share this product with others</p>
                        <img src="../qr-codes/${
                          product.id
                        }.png" alt="QR Code" class="qr-code-img">
                        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                            <a href="../qr-codes/${
                              product.id
                            }.png" download class="btn btn-primary">Download QR PNG</a>
                        </div>
                    </div>

                    ${
                      websiteLink
                        ? `<div class="mt-3">${websiteLink}</div>`
                        : ""
                    }
                </div>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 Felt and Yarn. All rights reserved.</p>
            <p><a href="${BASE_URL}/product/${
    product.id
  }.html">Share this product</a></p>
        </div>
    </footer>
</body>
</html>`;
}

// Main execution
async function main() {
  console.log("📄 Starting page generation...\n");

  // Load products
  if (!fs.existsSync(PRODUCTS_FILE)) {
    console.error(
      '❌ Products file not found. Please run "npm run parse-csv" first.'
    );
    process.exit(1);
  }

  const products = JSON.parse(fs.readFileSync(PRODUCTS_FILE, "utf-8"));
  console.log(`Found ${products.length} products\n`);

  // Generate individual product pages
  for (let i = 0; i < products.length; i++) {
    const product = products[i];
    process.stdout.write(`\rGenerating pages... ${i + 1}/${products.length}`);

    const html = generateProductHTML(product);
    const filePath = path.join(OUTPUT_DIR, `${product.id}.html`);
    fs.writeFileSync(filePath, html);
  }

  console.log(`\n\n✅ Successfully generated ${products.length} product pages`);
  console.log(`📁 Pages saved to: ${OUTPUT_DIR}`);
}

main().catch(console.error);
