# Deployment Guide

## Deploy to Vercel (Recommended)

### Quick Deploy

1. **Push to GitHub** (complete the GitHub setup first)

2. **Go to Vercel**: https://vercel.com/new

3. **Import Your Repository**:
   - Click "Import Project"
   - Select your GitHub repository: `asifaliattari/asif-todo-app`
   - Vercel will auto-detect Next.js

4. **Configure Project**:
   - **Project Name**: `asif-todo-app` (or your preferred name)
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `./` (default)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

5. **Environment Variables** (Optional):
   - Add any environment variables from `.env.example`
   - For now, you can skip this as the app works without them

6. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for the build to complete
   - You'll get a live URL like: `https://asif-todo-app.vercel.app`

### Auto-Deployment

Once connected, Vercel will automatically deploy:
- **Production**: Every push to `main` branch
- **Preview**: Every pull request

### Custom Domain (Optional)

1. Go to your project settings on Vercel
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Alternative: Deploy to Netlify

1. Go to https://app.netlify.com/
2. Click "Add new site" → "Import existing project"
3. Select your GitHub repository
4. Build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
5. Click "Deploy"

## Alternative: Deploy to GitHub Pages

GitHub Pages doesn't support server-side Next.js features, so you'll need to export as a static site:

1. Update `next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
};
```

2. Build and export:
```bash
npm run build
```

3. Deploy the `out` folder to GitHub Pages

## Local Development

```bash
npm install
npm run dev
```

Open http://localhost:3002

## Production Build (Local)

```bash
npm run build
npm start
```

---

**Created by Asif Ali AstolixGen for PIAIC Hackathon 2026**
