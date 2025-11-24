# Fix: Vercel Deployment Error

## Problem
Vercel was trying to deploy the Python backend instead of the Next.js frontend because it detected Python files in the root directory.

## Solution
Created `vercel.json` in the root directory that tells Vercel to:
1. Deploy from the `nextjs/` directory
2. Build the Next.js app
3. Use Next.js framework

## Configuration
The `vercel.json` file specifies:
- `rootDirectory`: "nextjs" - Deploy from nextjs folder
- `framework`: "nextjs" - Use Next.js framework
- `buildCommand`: Build Next.js app
- `outputDirectory`: Next.js build output

## Alternative: Set Root Directory in Vercel Dashboard

If the config file doesn't work, you can set it manually:

1. Go to Vercel Dashboard → Your Project
2. Settings → General
3. Under "Root Directory", change from `./` to `nextjs`
4. Save and redeploy

## After Fix

Once configured, Vercel will:
- ✅ Detect Next.js in the `nextjs/` folder
- ✅ Build and deploy the frontend correctly
- ✅ Ignore the Python backend in the root directory

