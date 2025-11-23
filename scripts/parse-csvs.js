const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");

const CSVS_DIR = path.join(__dirname, "../csvs");
const OUTPUT_DIR = path.join(__dirname, "../data");
const OUTPUT_FILE = path.join(OUTPUT_DIR, "products.json");
// Public data directory for frontend consumption
const PUBLIC_DATA_DIR = path.join(__dirname, "../public/data");
const PUBLIC_OUTPUT_FILE = path.join(PUBLIC_DATA_DIR, "products.json");

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const allProducts = [];
let productIdCounter = 1;

// Helper function to clean and validate data
function cleanString(str) {
  if (!str || typeof str !== "string") return "";
  return str.trim().replace(/\r/g, "");
}

function isValidProduct(row) {
  // Product must have at least a name to be valid
  const productName = cleanString(row["Product Name"]);
  return productName && productName.length > 0;
}

// Generate a URL-safe product ID
function generateProductId(productName, category, productLabel) {
  const safeName = productName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  const safeCategory = category
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  const label = cleanString(productLabel)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-");

  return `${safeCategory}-${label || safeName}-${productIdCounter++}`;
}

// Process a single CSV file
function processCSV(csvPath, categoryName) {
  return new Promise((resolve, reject) => {
    const products = [];

    fs.createReadStream(csvPath)
      .pipe(csv())
      .on("data", (row) => {
        if (isValidProduct(row)) {
          const productName = cleanString(row["Product Name"]);
          const category = cleanString(row["Category Name"]) || categoryName;
          const productLabel = cleanString(
            row["Product label\n(3-5 Characters)"]
          );

          const product = {
            id: generateProductId(productName, category, productLabel),
            sn: cleanString(row["SN"]),
            name: productName,
            label: productLabel,
            category: category,
            categoryFile: categoryName,
            imageLink: cleanString(row["Image Link"]),
            photo: cleanString(row["Photo"]),
            processes: cleanString(row["Processes"]),
            weight: cleanString(row["Weight \n(gm)"]),
            costPrice: cleanString(row["Cost Price\n(Nrs)"]),
            hsCode: cleanString(row["HS CODE"]),
            description: cleanString(row["Description"]),
            variations: cleanString(row["Variations\nColor Code"]),
            tags: cleanString(row["Tags"]),
            websiteLink:
              cleanString(row["Product Image\nWebsite Link"]) ||
              cleanString(row["Product Image Website Link"]),
            driveLink: cleanString(row["Product_image\n(Drive Link)"]),
            attributes: cleanString(row["Attributes"]),
            additionalCategory: cleanString(row["Additional Category"]),
            occasion: cleanString(row["Occassion"]),
            type: cleanString(row["Type"]),
            stock: cleanString(row["stock"]),
          };

          products.push(product);
          allProducts.push(product);
        }
      })
      .on("end", () => {
        console.log(
          `✓ Processed ${csvPath}: ${products.length} valid products`
        );
        resolve(products);
      })
      .on("error", reject);
  });
}

// Main execution
async function main() {
  console.log("🔍 Starting CSV parsing...\n");

  // Get all CSV files
  const csvFiles = fs.readdirSync(CSVS_DIR).filter((f) => f.endsWith(".csv"));
  console.log(`Found ${csvFiles.length} CSV files\n`);

  // Process all CSV files
  for (const csvFile of csvFiles) {
    const csvPath = path.join(CSVS_DIR, csvFile);
    const categoryName = csvFile
      .replace("Products for New ERP - ", "")
      .replace(".csv", "")
      .trim();

    try {
      await processCSV(csvPath, categoryName);
    } catch (error) {
      console.error(`✗ Error processing ${csvFile}:`, error.message);
    }
  }

  // Save all products to JSON
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allProducts, null, 2));
  // Mirror into public/data for static site fetches
  if (!fs.existsSync(PUBLIC_DATA_DIR)) {
    fs.mkdirSync(PUBLIC_DATA_DIR, { recursive: true });
  }
  fs.writeFileSync(PUBLIC_OUTPUT_FILE, JSON.stringify(allProducts, null, 2));

  console.log(
    `\n✅ Successfully parsed ${allProducts.length} products from ${csvFiles.length} CSV files`
  );
  console.log(`📄 Product data saved to: ${OUTPUT_FILE}`);
  console.log(`📄 Frontend copy saved to: ${PUBLIC_OUTPUT_FILE}`);

  // Generate summary statistics
  const categoryCounts = {};
  allProducts.forEach((p) => {
    categoryCounts[p.categoryFile] = (categoryCounts[p.categoryFile] || 0) + 1;
  });

  console.log("\n📊 Products by category:");
  Object.entries(categoryCounts)
    .sort((a, b) => b[1] - a[1])
    .forEach(([cat, count]) => {
      console.log(`   ${cat}: ${count}`);
    });
}

main().catch(console.error);
