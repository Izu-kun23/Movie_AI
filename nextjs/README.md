# Movie AI - Next.js Frontend

Next.js frontend for the Movie Recommendation API, optimized for Vercel deployment.

## Features

- ⚡ Next.js 15 with App Router
- 💬 AI chat interface
- 🎨 Sass styling (converted from original frontend)
- 📱 Responsive design
- 🖼️ Movie poster support
- 🔄 API proxy routes

## Setup

```bash
cd nextjs
npm install
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Backend Configuration

The frontend proxies API requests to your Python backend. Set the backend URL:

**Local Development:**
```bash
# Create .env.local
echo "BACKEND_URL=http://127.0.0.1:8000" > .env.local
```

**Production (Vercel):**
Set environment variable in Vercel dashboard:
- `BACKEND_URL` = Your deployed backend URL (e.g., `https://your-backend.railway.app`)

## Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Or connect your GitHub repo to Vercel - it will auto-detect Next.js!

## Project Structure

```
nextjs/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts      # API proxy to backend
│   ├── styles/               # Sass files
│   ├── page.tsx              # Main chat interface
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
└── package.json
```

## Environment Variables

- `BACKEND_URL` - Backend API URL (server-side)
- `NEXT_PUBLIC_BACKEND_URL` - Backend API URL (client-side, optional)
