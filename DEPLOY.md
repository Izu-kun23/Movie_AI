# 🚀 Deployment Commands

## Quick Deploy (Recommended)

From the project root directory:

```bash
cd /Users/admin/Desktop/Movie_AI
vercel --prod --yes
```

Or from the nextjs directory:

```bash
cd /Users/admin/Desktop/Movie_AI/nextjs
vercel --prod --yes
```

## Deploy via GitHub (Auto-deploy)

Push to GitHub and Vercel will auto-deploy:

```bash
cd /Users/admin/Desktop/Movie_AI
git add .
git commit -m "Deploy to production"
git push
```

After pushing, Vercel will automatically detect the changes and deploy.

## First Time Setup

If you haven't linked the project yet:

```bash
cd /Users/admin/Desktop/Movie_AI/nextjs
vercel
```

Follow the prompts to link your project.

## Set Backend URL Environment Variable

After deployment, set the backend URL:

**Via Dashboard:**
1. Go to https://vercel.com/izuchukwus-projects-5c276343/nextjs/settings/environment-variables
2. Add: `BACKEND_URL` = Your backend URL

**Via CLI:**
```bash
cd /Users/admin/Desktop/Movie_AI/nextjs
vercel env add BACKEND_URL
# Enter your backend URL when prompted
vercel --prod  # Redeploy
```

## Check Deployment Status

```bash
cd /Users/admin/Desktop/Movie_AI/nextjs
vercel ls
```

## View Logs

```bash
cd /Users/admin/Desktop/Movie_AI/nextjs
vercel logs
```

