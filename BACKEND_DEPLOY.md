# 🚀 Quick Start: Deploy Backend to Render

## One-Click Deploy Instructions

### 1. Go to Render Dashboard
👉 https://dashboard.render.com

### 2. Click "New +" → "Web Service"

### 3. Connect Your GitHub Repo
- Select **"Movie_AI"** repository
- Click **"Connect"**

### 4. Fill in These Settings:

```
Name: movie-ai-backend
Region: Oregon (or closest to you)
Branch: main

⚠️ IMPORTANT - Root Directory: backend

Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 5. Click "Create Web Service"

### 6. Wait 5-10 minutes for first deployment

### 7. Copy Your Backend URL
- Format: `https://movie-ai-backend-xxxx.onrender.com`
- **Copy this URL!**

### 8. Update Vercel Frontend
1. Go to Vercel Dashboard
2. Project → Settings → Environment Variables
3. Add: `BACKEND_URL` = `https://your-backend.onrender.com`
4. Redeploy

---

## ✅ Verify It Works

Visit: `https://your-backend.onrender.com/health`

Should return: `{"status": "ok", "model_loaded": true}`

---

## 📝 That's It!

Your backend is now live on Render! 🎉

**Next:** Set `BACKEND_URL` in Vercel and your full app will work!

