# 🚀 Quick Deploy to Vercel

## Run These Commands Now:

```bash
# 1. Add movies.csv (it's small, safe to commit)
git add -f backend/movies.csv

# 2. Add all deployment files
git add vercel.json api/ .gitignore frontend/src/js/main.js frontend/package.json

# 3. Add deployment docs (optional)
git add DEPLOY.md DEPLOY_CHECKLIST.md VERCEL_SETUP.md

# 4. Commit
git commit -m "Configure Vercel deployment"

# 5. Push to GitHub
git push
```

## Then Deploy:

### Option 1: Vercel Dashboard (Easiest) ⭐

1. Go to: https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repo: `Movie_AI`
4. Click "Deploy"
5. Wait ~2 minutes
6. ✅ Done! Your app is live!

### Option 2: Vercel CLI

```bash
npm install -g vercel
vercel login
vercel --prod
```

## That's It! 🎉

Your app will be live at: `https://your-project.vercel.app`

### Test It:
- Frontend: `https://your-project.vercel.app/`
- API Docs: `https://your-project.vercel.app/api/docs`

---

**Need help?** See `DEPLOY_CHECKLIST.md` for detailed troubleshooting.

