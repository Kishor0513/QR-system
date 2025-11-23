# Deployment Guide

## Step 1: Update Your GitHub Username

Edit `build_site.py` line 322:

```python
GITHUB_USERNAME = "your-actual-github-username"
```

## Step 2: GitHub Setup

### Option A: Using GitHub Desktop (Easiest)

1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. Click "Add" → "Add Existing Repository"
4. Select this folder
5. Click "Publish repository"
6. Name it: `qr-system`
7. Uncheck "Keep this code private" (or keep private if you prefer)
8. Click "Publish repository"

### Option B: Using Command Line

```powershell
# Initialize git
git init
git add .
git commit -m "Initial commit - QR system for Felt & Yarn"

# Create repo on GitHub.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/qr-system.git
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repo: https://github.com/YOUR_USERNAME/qr-system
2. Click "Settings" tab
3. Click "Pages" in left sidebar
4. Under "Source": Select branch `main`
5. Under folder: Select `/ (root)`
6. Click "Save"
7. Wait 2-3 minutes

Your site will be live at: `https://YOUR_USERNAME.github.io/qr-system/`

## Step 4: Regenerate QR Codes

After GitHub Pages is live:

```powershell
# Make sure DEPLOY_MODE = "github" in build_site.py
python build_site.py

# Commit and push updated QR codes
git add site/qrcodes/*
git commit -m "Update QR codes with GitHub Pages URL"
git push
```

Wait 1-2 minutes for deployment.

## Netlify Deployment (Alternative)

1. Go to https://app.netlify.com/
2. Sign up/login (can use GitHub account)
3. Click "Add new site" → "Import an existing project"
4. Connect to your GitHub repo
5. Build settings:
   - Build command: `python build_site.py`
   - Publish directory: `site`
6. Click "Deploy"
7. After first deploy, copy the Netlify URL (e.g., `random-name.netlify.app`)
8. Update `build_site.py`:
   ```python
   DEPLOY_MODE = "netlify"
   BASE_URL = "https://random-name.netlify.app/products/"
   ```
9. Run `python build_site.py` locally
10. Commit and push changes

## Testing

1. Visit your deployed URL
2. Open any product page
3. Scan QR code with phone
4. Verify it shows product info page
5. Click button to visit feltandyarn.com

## Updating Products

When CSVs change:

```powershell
python build_site.py
git add .
git commit -m "Update product data"
git push
```

GitHub Pages auto-deploys in 1-2 minutes.
