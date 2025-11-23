const fs = require('fs');
const path = require('path');
const QRCode = require('qrcode');

const PRODUCTS_FILE = path.join(__dirname, '../data/products.json');
const OUTPUT_DIR = path.join(__dirname, '../public/qr-codes');

// Base URL for the deployed site (will be updated after Netlify deployment)
// For now using a placeholder - update this after deployment
const BASE_URL = process.env.SITE_URL || 'https://your-site.netlify.app';

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Generate QR code for a single product
async function generateQRCode(product) {
    const productURL = `${BASE_URL}/product/${product.id}.html`;

    try {
        // Generate SVG (scalable, better for print)
        const svgPath = path.join(OUTPUT_DIR, `${product.id}.svg`);
        await QRCode.toFile(svgPath, productURL, {
            type: 'svg',
            width: 400,
            margin: 2,
            color: {
                dark: '#000000',
                light: '#FFFFFF'
            }
        });

        // Generate PNG (for web display)
        const pngPath = path.join(OUTPUT_DIR, `${product.id}.png`);
        await QRCode.toFile(pngPath, productURL, {
            type: 'png',
            width: 400,
            margin: 2,
            color: {
                dark: '#000000',
                light: '#FFFFFF'
            }
        });

        return true;
    } catch (error) {
        console.error(`✗ Failed to generate QR for ${product.name}:`, error.message);
        return false;
    }
}

// Main execution
async function main() {
    console.log('🔲 Starting QR code generation...\n');

    // Load products
    if (!fs.existsSync(PRODUCTS_FILE)) {
        console.error('❌ Products file not found. Please run "npm run parse-csv" first.');
        process.exit(1);
    }

    const products = JSON.parse(fs.readFileSync(PRODUCTS_FILE, 'utf-8'));
    console.log(`Found ${products.length} products\n`);

    let successCount = 0;
    let failCount = 0;

    // Generate QR codes
    for (let i = 0; i < products.length; i++) {
        const product = products[i];
        process.stdout.write(`\rGenerating QR codes... ${i + 1}/${products.length}`);

        const success = await generateQRCode(product);
        if (success) {
            successCount++;
        } else {
            failCount++;
        }
    }

    console.log(`\n\n✅ Successfully generated ${successCount} QR codes`);
    if (failCount > 0) {
        console.log(`⚠️  Failed to generate ${failCount} QR codes`);
    }
    console.log(`📁 QR codes saved to: ${OUTPUT_DIR}`);
    console.log(`\n💡 Note: QR codes currently point to: ${BASE_URL}`);
    console.log(`   Update BASE_URL in this script after deploying to Netlify.`);
}

main().catch(console.error);
