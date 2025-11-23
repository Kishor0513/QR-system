# Netlify Deployment Guide - Felt & Yarn QR System

## Quick Deploy (Easiest - 5 Minutes)

### Method 1: Drag & Drop (No Git Required)

1. **First Deploy - Get Your URL:**

   - Visit: https://app.netlify.com/drop
   - Sign up/login (free account)
   - Drag the entire `site` folder onto the page
   - Wait 30 seconds
   - Copy your site URL (e.g., `https://random-name-123.netlify.app`)

2. **Update QR Codes:**

   - Edit `build_site.py` line 340:
     ```python
     NETLIFY_SITE = os.environ.get("NETLIFY_SITE_URL", "https://YOUR-ACTUAL-URL.netlify.app")
     ```
   - Replace with your actual Netlify URL from step 1
   - Run: `python build_site.py`

3. **Re-deploy with Updated QR Codes:**
   - Drag the `site` folder to Netlify drop again
   - Done! QR codes now point to correct URL

### Method 2: GitHub Integration (Auto-Deploy on Changes)

1. **Push to GitHub first:**

   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/Kishor0513/qr-system.git
   git push -u origin main
   ```

2. **Connect to Netlify:**

   - Go to: https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub"
   - Authorize and select `qr-system` repo
   - Build settings (auto-detected from netlify.toml):
     - Build command: `python build_site.py`
     - Publish directory: `site`
   - Click "Deploy site"

3. **Set Environment Variable:**

   - After first deploy, go to: Site settings → Environment variables
   - Add: `NETLIFY_SITE_URL` = your site URL (e.g., `https://your-site.netlify.app`)
   - Trigger redeploy: Deploys → Trigger deploy → Deploy site

4. **Custom Domain (Optional):**
   - Site settings → Domain management → Add custom domain
   - Follow DNS instructions

## Your Site URLs

- **Main site:** `https://your-site.netlify.app/`
- **Index:** `https://your-site.netlify.app/index.html`
- **Products:** `https://your-site.netlify.app/products/`
- **QR codes:** Scan any QR from `site/qrcodes/` folder

## Updating Products

When CSVs change:

**Drag & Drop Method:**

```powershell
python build_site.py
# Drag site folder to Netlify drop
```

**GitHub Method:**

```powershell
python build_site.py
git add .
git commit -m "Update products"
git push
# Auto-deploys in 1-2 minutes
```

## Files Created for Netlify

- `netlify.toml` - Build configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version
- `.gitignore` - Files to exclude

## Troubleshooting

**Build fails:**

- Check build logs in Netlify dashboard
- Verify Python 3.11 is specified in runtime.txt
- Ensure requirements.txt has correct dependencies

**QR codes point to wrong URL:**

- Update NETLIFY_SITE_URL in build_site.py
- Re-run: `python build_site.py`
- Re-deploy

**Products not updating:**

- Make sure you're editing CSVs in `csvs/` folder
- Re-run build script
- Re-deploy

## Cost

Netlify free tier includes:

- 300 build minutes/month
- 100GB bandwidth/month
- Perfect for this project!
