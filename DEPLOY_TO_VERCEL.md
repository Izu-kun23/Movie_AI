# 🚀 Deploy to Vercel - Step by Step Guide

## Quick Deploy (Recommended - Dashboard)

### Step 1: Push to GitHub
```bash
cd /Users/admin/Desktop/Movie_AI
git add .
git commit -m "Add Next.js frontend"
git push
```

### Step 2: Deploy on Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub

2. **Click "Add New Project"**

3. **Import your GitHub repository:**
   - Select `Movie_AI` repository
   - Set **Root Directory** to: `nextjs`
   - Vercel will auto-detect Next.js! ✨

4. **Configure Project:**
   - Framework Preset: Next.js (auto-detected)
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)
   - Install Command: `npm install` (default)

5. **Set Environment Variable:**
   - Add: `BACKEND_URL`
   - Value: Your backend URL (e.g., `https://your-backend.railway.app`)
   - ⚠️ **Important:** You'll need to deploy the backend first (see below)

6. **Click "Deploy"** 🎉

### Step 3: Deploy Backend (If not done yet)

The Python backend must be deployed separately. Choose one:

#### Option A: Railway (Recommended)
```bash
# 1. Go to railway.app
# 2. New Project → Deploy from GitHub
# 3. Select Movie_AI repo
# 4. Set Root Directory: backend
# 5. Add Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 6. Copy the URL (e.g., https://movie-ai-backend.railway.app)
```

#### Option B: Render
```bash
# 1. Go to render.com
# 2. New → Web Service
# 3. Connect GitHub repo
# 4. Root Directory: backend
# 5. Build: pip install -r requirements.txt
# 6. Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 4: Update Vercel Environment Variable

1. Go to your Vercel project dashboard
2. Settings → Environment Variables
3. Edit `BACKEND_URL` with your deployed backend URL
4. Redeploy

---

## Alternative: Deploy via CLI

### Install Vercel CLI
```bash
npm install -g vercel
```

### Deploy
```bash
cd nextjs
vercel --prod
```

### Set Environment Variable
```bash
vercel env add BACKEND_URL
# Enter your backend URL when prompted
vercel --prod  # Redeploy
```

---

## Testing After Deployment

1. **Frontend:** `https://your-app.vercel.app`
2. **Test the chat interface**
3. **Check browser console** for any API errors

---

## Troubleshooting

### Backend Connection Issues
- Verify `BACKEND_URL` is set correctly in Vercel
- Check backend is running and accessible
- Test backend URL directly: `https://your-backend.railway.app/api/chat`

### Build Errors
- Check Next.js build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`
- Try building locally first: `cd nextjs && npm run build`

---

## Architecture

```
User → Vercel (Next.js Frontend) 
     → /api/chat route 
     → BACKEND_URL (Python FastAPI)
```

The Next.js `/api/chat` route proxies requests to your Python backend!

