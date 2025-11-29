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
