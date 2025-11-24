# 🚀 Deploy Backend to Render

## Quick Deploy Guide

### Step 1: Push to GitHub
Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push
```

### Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign in with GitHub

2. **Click "New +"** → **"Web Service"**

3. **Connect GitHub Repository:**
   - Select `Movie_AI` repository
   - Click "Connect"

4. **Configure Service:**
   - **Name:** `movie-ai-backend` (or any name you prefer)
   - **Region:** Choose closest to you (e.g., Oregon)
   - **Branch:** `main`
   - **Root Directory:** `backend` ⚠️ **IMPORTANT!**
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Advanced Settings (Optional):**
   - **Auto-Deploy:** Yes (auto-deploys on git push)
   - **Plan:** Free (or choose paid if needed)

6. **Click "Create Web Service"**

7. **Wait for deployment** (5-10 minutes on first deploy)

### Step 3: Get Your Backend URL

Once deployed, you'll see your service URL:
- Format: `https://movie-ai-backend.onrender.com` (or similar)
- **Copy this URL!**

### Step 4: Update Vercel Frontend

1. Go to Vercel Dashboard
2. Your Next.js project → Settings → Environment Variables
3. Add/Update: `BACKEND_URL` = `https://your-backend.onrender.com`
4. Redeploy frontend

---

## Manual Configuration (Without render.yaml)

If you prefer to configure manually:

**Settings:**
- **Root Directory:** `backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## Using render.yaml (Automatic)

The `render.yaml` file in the root directory will auto-configure everything when you:
1. Connect repo to Render
2. Select "Apply Render YAML" option
3. Render will read the configuration automatically

---

## Important Notes

### Free Tier Limitations:
- ⏱️ **Sleeps after 15 minutes** of inactivity
- 🐌 **Slower cold starts** (~30 seconds first request)
- 💾 **512MB RAM** limit
- ⏰ **750 hours/month** free (enough for always-on if you monitor usage)

### Keep Service Awake (Optional):
Use a service like [UptimeRobot](https://uptimerobot.com) to ping your service every 5 minutes to prevent sleep.

Add this to your backend `main.py`:
```python
@app.get("/ping")
def ping():
    return {"status": "ok"}
```

Then set UptimeRobot to ping: `https://your-backend.onrender.com/ping`

---

## Verify Deployment

1. Check health endpoint: `https://your-backend.onrender.com/health`
2. Test API: `https://your-backend.onrender.com/api/chat` (POST request)
3. Check logs in Render dashboard

---

## Troubleshooting

### Build Fails:
- Check logs in Render dashboard
- Verify `requirements.txt` is in `backend/` directory
- Ensure Python version matches (3.12.0)

### Service Crashes:
- Check logs for errors
- Verify `movies.csv` exists in `backend/` directory
- Check PORT environment variable is used

### Slow Response:
- First request after sleep takes ~30 seconds (free tier)
- Consider upgrading to paid plan for faster response

---

## Environment Variables (if needed)

Add in Render Dashboard → Environment:
- None required (movies.csv is included in repo)

---

## Success! 🎉

Once deployed, you'll have:
- **Backend:** `https://your-backend.onrender.com`
- **Frontend:** `https://your-app.vercel.app`

Both connected and working together!

