# How to Host Your QR System on the Internet (GitHub Pages)

This guide will show you how to host your website for free using **GitHub Pages**.

## Step 1: Create a GitHub Repository
1.  Go to [github.com](https://github.com) and sign in (or create an account).
2.  Click the **+** icon in the top-right and select **New repository**.
3.  Name it something simple, like `qr-system`.
4.  Make sure it is **Public**.
5.  Click **Create repository**.

## Step 2: Upload Your Code
You can use the "Upload files" button on GitHub or use Git commands if you know them.
**Easiest way (Upload files):**
1.  In your new repository, click the link **uploading an existing file**.
2.  Drag and drop the **entire contents** of your project folder into the browser window.
    *   **Important**: Make sure you include the `site` folder!
3.  Wait for the files to upload.
4.  Click **Commit changes**.

## Step 3: Enable GitHub Pages
1.  Go to your repository's **Settings** tab.
2.  On the left sidebar, click **Pages**.
3.  Under **Build and deployment** > **Source**, select **Deploy from a branch**.
4.  Under **Branch**, select `main` (or `master`) and for the folder select `/ (root)`.
    *   *Note: If your `index.html` is inside the `site` folder, you might need to configure this differently. See below.*

**Recommended Setup for this Project:**
Since your website files are inside the `site` folder, we need to tell GitHub to look there.
*   **Option A (Easiest)**: Move the contents of `site/` to the root folder before uploading.
*   **Option B (Better)**: Configure GitHub Actions (Advanced).

**Let's go with Option A (Move files to root) for simplicity:**
1.  On your computer, move `index.html`, `style.css`, `app.js`, `products.json`, and the `qrcodes` folder **OUT** of `site` and into the main folder.
2.  Delete the empty `site` folder.
3.  Update `data_builder.py`: Change `SITE_DIR = ROOT / "site"` to `SITE_DIR = ROOT`.
4.  Run `python data_builder.py` to make sure everything works.
5.  Upload these files to GitHub.

## Step 4: Get Your Website URL
Once enabled, GitHub will give you a URL like:
`https://your-username.github.io/qr-system/`

## Step 5: Update QR Codes for the Public Web
Now that you have a real URL, you need to update your QR codes to point to it instead of your local computer.

1.  Open `data_builder.py` in a text editor.
2.  Find the line:
    ```python
    PUBLIC_BASE_URL = None
    ```
3.  Change it to your new GitHub URL:
    ```python
    PUBLIC_BASE_URL = "https://your-username.github.io/qr-system/"
    ```
4.  Run the build script:
    ```powershell
    python data_builder.py
    ```
5.  This will regenerate all QR codes in the `qrcodes` folder.
6.  **Upload the new QR codes** to GitHub (Commit changes).

## Step 6: Done!
*   Your website is now online at your GitHub URL.
*   The new QR codes will open that URL on any phone (no WiFi needed).
