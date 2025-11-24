# 🚀 Deploy to Vercel - Step by Step

## Quick Deployment Guide

### ✅ Step 1: Prepare movies.csv

Your `movies.csv` is small (49 lines), so it's safe to commit:

```bash
# Make sure movies.csv is not ignored
git add -f backend/movies.csv
git commit -m "Add movies.csv for deployment"
```

### ✅ Step 2: Build Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### ✅ Step 3: Commit All Files

```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push
```

### ✅ Step 4: Deploy to Vercel

#### Option A: Via GitHub (Easiest)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository `Movie_AI`
4. Vercel will auto-detect the configuration
5. Click "Deploy"
6. Wait ~2-3 minutes
7. ✨ Your app is live!

#### Option B: Via CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

## 📋 What's Configured

✅ **API Routes**: `/api/*` → Python FastAPI backend  
✅ **Frontend**: All other routes → Static frontend files  
✅ **Auto API URL**: Frontend automatically detects production  
✅ **Python Dependencies**: From `requirements.txt`  

## 🎯 After Deployment

Your app will be available at:
- `https://your-project-name.vercel.app`
- Frontend: `https://your-project-name.vercel.app/`
- API: `https://your-project-name.vercel.app/api/docs`

## 🧪 Test It

1. Visit your deployment URL
2. Try: "I like The Matrix"
3. Check API docs: `/api/docs`

## 🐛 Common Issues

**Issue**: "movies.csv not found"  
**Fix**: Make sure you committed it with `git add -f backend/movies.csv`

**Issue**: Frontend shows "Connection Error"  
**Fix**: Check browser console. API should auto-detect production URL.

**Issue**: Build fails  
**Fix**: Check Vercel build logs. Make sure `requirements.txt` has all dependencies.

## 📞 Need Help?

Check the detailed guide: `VERCEL_SETUP.md`

