# ✅ Vercel Deployment Checklist

## Pre-Deployment Steps

### 1. Files Ready ✅
- [x] `vercel.json` created
- [x] `api/index.py` entry point created
- [x] Frontend built (`frontend/dist/` exists)
- [x] `backend/movies.csv` is small (13KB) - safe to commit

### 2. Commit movies.csv
```bash
# Remove it from .gitignore or force add it
git add -f backend/movies.csv
git status  # Verify it's staged
```

### 3. Commit Everything
```bash
git add vercel.json api/ frontend/dist/ DEPLOY.md
git commit -m "Add Vercel deployment configuration"
git push
```

## Deploy on Vercel

### Quick Method (GitHub Integration)

1. **Go to Vercel:**
   - Visit: https://vercel.com
   - Sign in with GitHub

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Select your `Movie_AI` repository
   - Click "Import"

3. **Configure (if needed):**
   - Framework Preset: **Other** (or leave default)
   - Root Directory: **./** (root)
   - Build Command: (leave empty - frontend is pre-built)
   - Output Directory: (leave empty)

4. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - ✅ Done!

### Alternative: CLI Method

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy (will ask questions first time)
vercel

# Production deploy
vercel --prod
```

## After Deployment

### Test These URLs:

1. **Frontend:**
   ```
   https://your-project.vercel.app/
   ```

2. **API Health:**
   ```
   https://your-project.vercel.app/api/health
   ```

3. **API Docs:**
   ```
   https://your-project.vercel.app/api/docs
   ```

4. **Test Chat:**
   - Go to frontend URL
   - Try: "I like The Matrix"
   - Should get recommendations!

## 🎯 Expected Results

✅ Frontend loads at root URL  
✅ API works at `/api/*` routes  
✅ Chat interface connects to backend  
✅ Movie recommendations work  
✅ Posters display (if available)  

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `movies.csv not found` | Commit it: `git add -f backend/movies.csv` |
| `Module not found` | Check `requirements.txt` has all packages |
| `404 on frontend` | Ensure `frontend/dist/` is committed |
| CORS errors | Already configured in backend, check browser console |
| API timeout | Normal for first request (cold start) |

## 📊 Deployment Summary

- **Backend**: Python FastAPI serverless function
- **Frontend**: Static files served from `frontend/dist/`
- **Routing**: `/api/*` → Backend, everything else → Frontend
- **Auto-config**: Frontend auto-detects API URL

## ✨ Next Steps

Once deployed:
1. Test all functionality
2. Monitor Vercel dashboard for logs
3. Set up custom domain (optional)
4. Configure environment variables if needed

---

**Ready to deploy? Run the commands above and you're done!** 🚀

