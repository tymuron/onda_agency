# 🚀 Complete Cloud Deployment Guide for Onda

This guide walks you through deploying your Onda website to the cloud and connecting it to a custom domain. Follow these steps carefully!

---

## ✅ Before You Start

Make sure you have:
- An OpenAI API key (starts with `sk-...`)
- A GitHub account
- Access to your project folder: `/Users/annaromeo/.gemini/antigravity/scratch/ai_vibe_agency`

---

## Step 1: Upload Your Code to GitHub 🐙

### Part A: Create a New Repository

1. Go to [github.com](https://github.com) and log in
2. Click the **+** icon (top-right) → **New repository**
3. Repository name: `onda-agency`
4. Select **Public**
5. **Do NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Part B: Upload Your Files

**Important:** We'll upload files carefully to avoid errors with hidden files and large folders.

1. **Open your project folder:**
   ```bash
   cd ~/.gemini/antigravity/scratch/ai_vibe_agency
   open .
   ```

2. **On the GitHub page**, click the link that says **"uploading an existing file"**

3. **Upload in this order:**

   **First: Frontend folder**
   - Drag the entire `frontend` folder to the GitHub page
   - Wait for upload to complete

   **Second: Backend files (NOT the folder!)**
   - Open the `backend` folder on your computer
   - Select these files ONLY:
     - `main.py`
     - `lead_qualifier.py`
     - `rag_chat.py`
     - `requirements.txt`
     - `env.example`
   - **Skip:** `.env` (this contains your secret API key!)
   - Drag the selected files to GitHub
   
   **Note:** Don't upload `.env` because it contains your secret API key!

4. **Commit the upload:**
   - Scroll down to "Commit changes"
   - Message: `Initial upload`
   - Click **Commit changes**

5. **Create backend folder structure:**
   - After upload completes, click **Add file** → **Create new file**
   - Name it: `backend/.env.example`
   - Copy this content:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Click **Commit changes**
   
   This creates the `backend` folder. Now we need to move our files:
   - For each backend file you uploaded earlier (`main.py`, `lead_qualifier.py`, etc.):
     - Click on the file → Click the pencil icon (Edit)
     - Change the filename to `backend/filename.py` (add `backend/` at the start)
     - Click **Commit changes**

✅ Your code is now on GitHub!

---

## Step 2: Deploy to Render ☁️

### Part A: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **Get Started**
3. Sign up using your **GitHub account** (easiest option)

### Part B: Create Web Service

1. On the Render dashboard, click **New +** → **Web Service**
2. You'll see your `onda-agency` repository listed
3. Click **Connect** next to it
4. Configure your service:

   **Basic Info:**
   - Name: `onda-agency` (or your choice)
   - Region: Choose closest to you (e.g., `Frankfurt` for Europe, `Oregon` for US)
   - Branch: `main`
   
   **Build & Deploy:**
   - Runtime: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `python backend/main.py`
   
   **Instance Type:**
   - Select **Free**

5. **Add Environment Variable** (CRITICAL!)
   - Scroll down to **Environment Variables**
   - Click **Add Environment Variable**
   - Key: `OPENAI_API_KEY`
   - Value: Your actual OpenAI API key (starts with `sk-...`)
   - Click **Add**

6. Click **Create Web Service**

### Part C: Wait for Deployment

1. Render will now build and deploy your app
2. Watch the logs scroll by - this takes 2-5 minutes
3. Wait for this message: **"Application startup complete"**
4. At the top of the page, you'll see a URL like: `https://onda-agency.onrender.com`
5. **Click it!** Your website is LIVE! 🎉

**Troubleshooting:**
- If you see errors, check the logs at the bottom
- Common issue: Make sure `OPENAI_API_KEY` is set correctly
- The free tier sleeps after 15 minutes of inactivity (first load after sleep takes ~30 seconds)

---

## Step 3: Connect Your Custom Domain (Optional) 🌐

If you own a domain like `onda.agency` or `myagency.com`:

### Option A: Using a Subdomain (Recommended for beginners)

**On Render:**
1. Go to your Web Service → **Settings** tab
2. Scroll to **Custom Domains**
3. Click **Add Custom Domain**
4. Enter: `www.yourdomain.com` (or `app.yourdomain.com`)
5. Render will show you a CNAME record to add

**In Your Domain Provider (GoDaddy/Namecheap/etc):**
1. Log in to your domain provider
2. Find **DNS Settings** or **DNS Management**
3. Click **Add Record** or **Add New Record**
4. Select type: **CNAME**
5. Settings:
   - Name/Host: `www` (or `app`)
   - Value/Points to: `onda-agency.onrender.com` (from Render)
   - TTL: `3600` (or Auto)
6. Save the record
7. Wait 5-60 minutes for DNS to update

### Option B: Using Root Domain (Advanced)

For `yourdomain.com` without `www`:

1. In Render, add custom domain: `yourdomain.com`
2. Render provides IP addresses
3. In your domain provider:
   - Add **A Record**:
     - Name/Host: `@`
     - Value: IP address from Render
     - TTL: `3600`
   - Add **AAAA Record** (if Render provides IPv6):
     - Name/Host: `@`
     - Value: IPv6 address from Render
     - TTL: `3600`

**Note:** Some providers don't support CNAME flattening for root domains. Check Render's documentation for your specific provider.

---

## Step 4: Enable HTTPS (Free & Automatic!) 🔒

Once your custom domain is connected:

1. In Render Settings → **Custom Domains**
2. Wait for the green checkmark next to your domain (DNS verified)
3. Render automatically provisions a free SSL certificate
4. Your site will be accessible via `https://yourdomain.com` within 1 hour

---

## 🎯 Quick Reference

**Your URLs:**
- Render default: `https://onda-agency.onrender.com`
- Custom domain: `https://www.yourdomain.com`

**Important Files on GitHub:**
- Frontend code: `/frontend/`
- Backend code: `/backend/`
- Requirements: `/backend/requirements.txt`

**Updating Your Site:**
1. Make changes to your code locally
2. Upload new files to GitHub (replace existing ones)
3. Render auto-deploys within 2-3 minutes

**Render Dashboard:**
- View logs: Click your service → **Logs** tab
- Environment variables: **Settings** → **Environment**
- Redeploy: **Manual Deploy** → **Deploy latest commit**

---

## 🆘 Common Issues

**Issue: "Application failed to start"**
- Check logs for Python errors
- Verify `OPENAI_API_KEY` is set
- Ensure all files are in correct folders (`backend/` and `frontend/`)

**Issue: "502 Bad Gateway"**
- Service is still starting (wait 30 seconds)
- Or service crashed (check logs)

**Issue: "Domain not connecting"**
- DNS can take up to 48 hours (usually 5-30 minutes)
- Verify DNS records match exactly what Render shows
- Try `www.yourdomain.com` instead of bare domain

**Issue: Website works but AI features don't**
- Check browser console for errors (F12)
- Verify API key has credits on OpenAI
- Check Render logs for API errors

---

## ✅ Success Checklist

- [ ] Code uploaded to GitHub
- [ ] Render service created and deployed
- [ ] Environment variable `OPENAI_API_KEY` added
- [ ] Website loads at Render URL
- [ ] Lead qualifier demo works
- [ ] Chat demo works
- [ ] Contact form submits successfully
- [ ] Custom domain connected (optional)
- [ ] HTTPS enabled (automatic with custom domain)

---

🎉 **Congratulations!** Your Onda agency website is now live on the internet!
