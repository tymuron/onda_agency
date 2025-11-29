# How to Deploy Onda Agency

## 1. Update GitHub

**First, check if you are connected to the right repository:**
Run this in your terminal:
```bash
git remote -v
```
*   **If you see your repository URL:** Great! Proceed to step 2.
*   **If you see "fatal: not a git repository" or nothing:** You need to link it first. Run these commands (replace `YOUR_USERNAME`):
    ```bash
    git init
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/onda-agency.git
    ```

**Step 2: Save and Push Changes**
Once connected, run:
```bash
git add .
git commit -m "Update portfolio, branding, and add AI Copywriter demo"
git push -u origin main
```

> [!IMPORTANT]
> **If you see `remote: Repository not found`:**
> This means you haven't created the empty repository on GitHub.com yet.
> 1. Go to [github.com/new](https://github.com/new).
> 2. Name it `onda-agency`.
> 3. Click **Create repository**.
> 4. **Do not** initialize with README, .gitignore, or License (keep it empty).
> 5. Run `git push -u origin main` again.

> [!TIP]
> **Made a mistake with the name?**
> If you created the repo with a different name (e.g., `my-agency`), just update your local link:
> 1. Remove the old link: `git remote remove origin`
> 2. Add the new one: `git remote add origin https://github.com/YOUR_USERNAME/ACTUAL_NAME.git`
> 3. Push again: `git push -u origin main`

> [!WARNING]
> **Error: `! [rejected] ... (fetch first)`?**
> This happens if the GitHub repository already has files (like an old version of the site, or a README).
> Since you want to **replace** the old version with this new one, force the upload:
> ```bash
> git push -f origin main
> ```

## 2. Deploy on Render
*   **If you already have Render connected:** It will automatically detect the push and start redeploying.
*   **If not:** Go to [dashboard.render.com](https://dashboard.render.com), create a new **Web Service**, and connect your existing repository.

### Configuration
Render needs to know how to build and run your app.
*   **Build Command:** `pip install -r backend/requirements.txt`
*   **Start Command:** `python backend/main.py`

### Environment Variables
Don't forget to check your Environment Variables in the Render Dashboard:
*   `OPENAI_API_KEY`: Your OpenAI API Key.
*   `RESEND_API_KEY`: Your Resend API Key.
*   `NOTIFICATION_EMAIL`: Your email address.

## 3. Done!
Your site will be live in a few minutes.
