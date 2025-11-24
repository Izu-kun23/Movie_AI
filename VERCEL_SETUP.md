# Complete Vercel Deployment Guide

## 🚀 Quick Start

### Step 1: Prepare Your Files

1. **Ensure movies.csv is committed** (or handle it differently - see below)
   ```bash
   # Check if movies.csv exists
   ls -lh backend/movies.csv
   
   # If it's large, you may want to:
   # - Use a database instead
   # - Load from external storage
   # - Or commit it anyway if under 50MB
   ```

2. **Build the frontend** (if not already built):
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

### Step 2: Deploy to Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/login
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live! 🎉

#### Option B: Via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   # Test deployment
   vercel
   
   # Production deployment
   vercel --prod
   ```

## 📁 Project Structure for Vercel

```
Movie_AI/
├── api/
│   ├── __init__.py
│   └── index.py          # Vercel serverless entry point
├── backend/
│   ├── main.py           # FastAPI app
│   ├── model.py          # ML model
│   └── movies.csv        # ⚠️ Must be available
├── frontend/
│   ├── index.html
│   ├── dist/             # Built files
│   └── package.json
├── vercel.json           # Vercel configuration
└── requirements.txt      # Python dependencies
```

## 🔧 Configuration Details

### vercel.json
- Routes `/api/*` to Python backend
- Serves frontend static files from `/frontend/*`
- Handles rewrites for proper routing

### api/index.py
- Entry point for Vercel serverless functions
- Sets up Python paths correctly
- Imports FastAPI app from backend

### Frontend API URL
- Automatically detects localhost vs production
- Uses same-origin requests in production
- No manual configuration needed!

## ⚠️ Important: movies.csv File

### Problem:
The `movies.csv` file is in `.gitignore`, so it won't be deployed by default.

### Solutions:

#### Solution 1: Commit the CSV (If Small)
```bash
# Remove from .gitignore temporarily
# Edit .gitignore and comment out: backend/movies.csv

git add backend/movies.csv
git commit -m "Add movies.csv for deployment"
git push
```

#### Solution 2: Use Environment Variables
For small datasets, you could store as an environment variable, but this is not recommended for large files.

#### Solution 3: External Storage (Recommended for Production)
1. Upload `movies.csv` to:
   - Google Cloud Storage
   - AWS S3
   - Or any public URL
2. Update `backend/model.py` to load from URL:
   ```python
   import requests
   import pandas as pd
   
   # In load_data method:
   csv_url = os.getenv('MOVIES_CSV_URL', 'movies.csv')
   if csv_url.startswith('http'):
       response = requests.get(csv_url)
       self.df = pd.read_csv(StringIO(response.text))
   else:
       self.df = pd.read_csv(self.csv_path)
   ```

#### Solution 4: Database (Best for Production)
- Use Vercel Postgres or another database
- Store movies in database instead of CSV
- Update model to load from database

## 🔍 Testing Your Deployment

After deployment, test these endpoints:

1. **Health Check:**
   ```
   https://your-project.vercel.app/api/health
   ```

2. **API Docs:**
   ```
   https://your-project.vercel.app/api/docs
   ```

3. **Test Chat:**
   ```
   https://your-project.vercel.app/
   ```
   Try: "I like The Matrix"

## 🐛 Troubleshooting

### Error: "No fastapi entrypoint found"
- ✅ Fixed: We created `api/index.py`

### Error: "movies.csv not found"
- Check if file is committed
- Or implement one of the solutions above

### Error: "Module not found"
- Ensure `requirements.txt` includes all dependencies
- Check that `backend/__init__.py` exists

### Frontend not loading
- Ensure `frontend/dist/` files are built
- Check browser console for errors
- Verify API routes are working

### CORS Errors
- Backend already allows all origins (`allow_origins=["*"]`)
- If issues persist, update `backend/main.py` CORS settings

## 📊 Environment Variables (Optional)

If you need environment variables:

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Add variables like:
   - `MOVIES_CSV_URL` (if using external storage)
   - `API_KEY` (for external APIs)
   - etc.

## 🎯 Next Steps After Deployment

1. **Update Frontend URL** (if needed):
   - The frontend automatically detects production
   - No changes needed!

2. **Monitor Logs:**
   - Check Vercel dashboard for function logs
   - Debug any runtime errors

3. **Optimize:**
   - Consider caching responses
   - Use CDN for static assets
   - Monitor function execution time

## 📝 Deployment Checklist

- [ ] `vercel.json` created
- [ ] `api/index.py` created
- [ ] `backend/movies.csv` available (committed or external)
- [ ] Frontend built (`npm run build` in frontend/)
- [ ] `requirements.txt` up to date
- [ ] All files committed to git
- [ ] Repository connected to Vercel
- [ ] Deployment successful
- [ ] Test endpoints working
- [ ] Frontend loads correctly

## 🎉 Success!

Once deployed, you'll get a URL like:
- `https://movie-ai.vercel.app`
- Or a custom domain if configured

Your Movie AI is now live! 🚀

