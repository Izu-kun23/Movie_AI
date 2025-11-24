# Vercel Deployment Guide

## Configuration Files

### `vercel.json`
This file tells Vercel:
- To use `@vercel/python` for the `api/index.py` file
- To route all requests to the FastAPI app

### `api/index.py`
This is the entry point that Vercel will use. It:
- Adds the `backend/` directory to Python path
- Imports the FastAPI `app` from `backend/main.py`
- Exports it for Vercel to use

## Important Notes

### 1. CSV File Location
Make sure `backend/movies.csv` exists. If it's in `.gitignore`, you may need to:
- Commit it (if it's small enough)
- Or upload it to Vercel environment variables
- Or use Vercel's file system (note: serverless functions have a read-only filesystem except `/tmp`)

### 2. Environment Variables
You may need to set environment variables in Vercel dashboard if your app uses any (like API keys).

### 3. Requirements
The `requirements.txt` file should be at the root of your project (which it is).

### 4. File Size Limits
- Vercel serverless functions have limits on file size
- If `movies.csv` is too large, consider:
  - Using a database instead (e.g., Vercel Postgres)
  - Loading data from an external source
  - Splitting into smaller files

## Deployment Steps

1. **Commit and push your code:**
   ```bash
   git add vercel.json api/index.py
   git commit -m "Add Vercel deployment configuration"
   git push
   ```

2. **Deploy on Vercel:**
   - Connect your GitHub repository to Vercel
   - Vercel should auto-detect the configuration
   - Or deploy via Vercel CLI: `vercel --prod`

3. **Check deployment:**
   - Your API will be available at: `https://your-project.vercel.app`
   - Test endpoints like: `https://your-project.vercel.app/docs`

## Troubleshooting

### CSV Not Found
If you get errors about `movies.csv` not found:
- Check that it's committed to git (if small enough)
- Or update paths in `backend/model.py` to use absolute paths
- Or load from an external URL/database

### Import Errors
If you get import errors:
- Ensure `backend/` has `__init__.py`
- Check that all dependencies are in `requirements.txt`
- Verify Python path is set correctly in `api/index.py`

### Timeout Issues
- Vercel serverless functions have execution time limits
- If loading CSV is slow, consider pre-processing or using a database

