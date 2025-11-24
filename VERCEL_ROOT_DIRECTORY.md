# ⚠️ Important: Set Root Directory in Vercel Dashboard

The `rootDirectory` property is **not supported** in `vercel.json`. 

## Solution: Set Root Directory in Vercel Dashboard

You **must** set the Root Directory manually in the Vercel Dashboard:

### Steps:

1. Go to your Vercel project: https://vercel.com/izuchukwus-projects-5c276343/nextjs

2. Click **Settings** (top menu)

3. Go to **General** section

4. Scroll down to **Root Directory**

5. Click **Edit** and change it from `./` to `nextjs`

6. Click **Save**

7. **Redeploy** your project (or push a new commit to trigger auto-deploy)

---

## Alternative: Deploy from nextjs folder via CLI

When using CLI, deploy directly from the nextjs folder:

```bash
cd /Users/admin/Desktop/Movie_AI/nextjs
vercel --prod --yes
```

This way Vercel will detect the Next.js project in that directory.

---

## Why?

The `rootDirectory` property was removed from `vercel.json` configuration. It can only be set through:
- Vercel Dashboard (Settings → General → Root Directory)
- Or by deploying from the correct directory via CLI

