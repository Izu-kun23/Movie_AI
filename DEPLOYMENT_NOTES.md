# Deployment Notes for Vercel

## Important: movies.csv File

The `backend/movies.csv` file is currently in `.gitignore` (because it can be large). 

### For Vercel Deployment:

**Option 1: Commit movies.csv (if small enough)**
```bash
# Remove from .gitignore temporarily, commit, then add back
git rm --cached .gitignore  # Edit to remove backend/movies.csv line
git add backend/movies.csv
git commit -m "Add movies.csv for deployment"
```

**Option 2: Use Environment Variable or External Storage**
- Store movies.csv in a cloud storage (S3, etc.)
- Or use a database instead of CSV
- Or load from an external URL

**Option 3: Generate on First Request (Not Recommended)**
- This will be slow and hit rate limits

## File Structure for Vercel

```
Movie_AI/
├── api/
│   ├── __init__.py
│   └── index.py          # Vercel entry point
├── backend/
│   ├── main.py           # FastAPI app
│   ├── model.py
│   └── movies.csv        # Must be committed or handled differently
├── vercel.json           # Vercel configuration
└── requirements.txt      # Python dependencies
```

## Deployment Checklist

- [ ] `vercel.json` configured
- [ ] `api/index.py` created
- [ ] `backend/movies.csv` available (committed or external)
- [ ] `requirements.txt` includes all dependencies
- [ ] Environment variables set in Vercel dashboard (if needed)
- [ ] CORS configured for your frontend domain

## Testing Locally

You can test the Vercel setup locally:
```bash
# Install Vercel CLI
npm i -g vercel

# Test deployment
vercel dev
```

This will run your app in a Vercel-like environment.

