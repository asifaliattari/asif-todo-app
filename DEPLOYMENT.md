# TaskFlow - Full Stack Deployment Guide

**Project**: TaskFlow Phase III - AI-Powered Todo App
**Author**: Asif Ali AstolixGen
**Hackathon**: GIAIC Hackathon 2026

---

## 📦 What You're Deploying

- **Frontend**: Next.js app (Vercel)
- **Backend**: FastAPI + OpenAI chatbot (Hugging Face Spaces / Railway / Render)
- **Database**: Neon PostgreSQL (already configured)

---

## ✅ Vercel Deployment Status

Your project is **READY** for Vercel deployment! ✨

### What's Already Configured:
- ✅ `frontend/vercel.json` with build settings
- ✅ Environment variables documented
- ✅ Next.js 15 with App Router
- ✅ TypeScript configuration
- ✅ Tailwind CSS setup
- ✅ API client for backend communication

---

## 🚀 Deploy Frontend to Vercel (Recommended)

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

---

## 🔧 Deploy Backend API

Your backend **MUST** be deployed separately. Choose one option below:

### Option A: Hugging Face Spaces (Current Config)

**Note**: Your `frontend/vercel.json` is already pointing to: `https://asifaliastolixgen-taskflow-api.hf.space`

1. **Create HF Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `taskflow-api`
   - SDK: **Docker**
   - Hardware: CPU Basic (free)

2. **Add Dockerfile to backend/**
   Create `backend/Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   RUN pip install --no-cache-dir -r requirements.txt
   EXPOSE 7860
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
   ```

3. **Upload Files**
   - Upload entire `backend/` directory to the Space
   - Or connect via Git (recommended)

4. **Set Environment Variables (Secrets)**
   In Space Settings → Repository Secrets:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_xxx@ep-xxx.neon.tech/neondb?sslmode=require
   BETTER_AUTH_SECRET=EW1LZCuWtQ2RUzAWJ3GSptFVmALU+owmwOjFvl06Dco=
   OPENAI_API_KEY=sk-proj-xxx
   OPENAI_MODEL=gpt-4o-mini
   FRONTEND_URL=https://your-project.vercel.app
   BACKEND_API_URL=https://your-space-name.hf.space
   ```

5. **Update CORS**
   After deploying frontend, update `backend/app/main.py`:
   ```python
   allow_origins=[
       "https://your-project-name.vercel.app",
       "http://localhost:3000"  # for local dev
   ]
   ```

6. **Test**
   ```bash
   curl https://your-space-name.hf.space/api/health
   ```

### Option B: Railway (Easier)

1. **Push to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Add backend for deployment"
   git push origin main
   ```

2. **Deploy**
   - Go to https://railway.app
   - Sign up with GitHub
   - New Project → "Deploy from GitHub repo"
   - Select your repository
   - Choose `backend` directory as root

3. **Environment Variables**
   Add in Railway dashboard (same as HF Spaces above)

4. **Custom Domain**
   Railway provides: `https://your-app.up.railway.app`
   Or add your own domain in settings

5. **Update Frontend**
   Update `NEXT_PUBLIC_API_URL` in Vercel to Railway URL

### Option C: Render

1. **Create Web Service**
   - Go to https://render.com
   - New → Web Service
   - Connect GitHub repository

2. **Configure**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3

3. **Environment Variables**
   Add all variables (same as above)

---

## 🔐 Critical Environment Variables

### Frontend (Vercel Dashboard)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_APP_NAME=TaskFlow
NEXT_PUBLIC_AUTHOR=Asif Ali AstolixGen
NEXT_PUBLIC_HACKATHON=GIAIC Hackathon 2026
```

### Backend (Platform Secrets)
```bash
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require
BETTER_AUTH_SECRET=your-32-char-secret-here
OPENAI_API_KEY=sk-proj-your-openai-key-here
OPENAI_MODEL=gpt-4o-mini
FRONTEND_URL=https://your-vercel-app.vercel.app
BACKEND_API_URL=https://your-backend.platform.app
ENVIRONMENT=production
```

⚠️ **SECURITY**: Get actual values from your local `.env` file - NEVER commit secrets to Git!

⚠️ **IMPORTANT**: Replace `your-backend-url.com` and `your-vercel-app` with actual URLs!

---

## 📋 Deployment Checklist

### Before Deploying:
- [ ] Git repository is up to date
- [ ] All environment variables documented
- [ ] Database is accessible (Neon)
- [ ] OpenAI API key is valid
- [ ] Frontend builds locally (`npm run build`)
- [ ] Backend runs locally (`uvicorn app.main:app`)

### Deploy Backend First:
- [ ] Choose platform (HF / Railway / Render)
- [ ] Set all environment variables
- [ ] Deploy and get URL
- [ ] Test `/api/health` endpoint
- [ ] Test `/docs` (FastAPI auto docs)

### Then Deploy Frontend:
- [ ] Update `NEXT_PUBLIC_API_URL` to backend URL
- [ ] Push to GitHub
- [ ] Import to Vercel
- [ ] Set environment variables
- [ ] Deploy

### Post-Deployment:
- [ ] Test signup/login
- [ ] Test creating tasks
- [ ] Test AI chatbot
- [ ] Update backend CORS with frontend URL
- [ ] Monitor for errors

---

## 🧪 Testing Your Deployment

1. **Backend Health Check**
   ```bash
   curl https://your-backend.com/api/health
   # Expected: {"status":"healthy"}
   ```

2. **Frontend Load Test**
   - Open `https://your-project.vercel.app`
   - Should load without errors
   - Check browser console for issues

3. **API Integration Test**
   - Sign up for account
   - Create a task
   - Verify task appears in database
   - Test chatbot

---

## 🐛 Common Issues

### CORS Error
**Symptom**: "Access to fetch blocked by CORS policy"
**Fix**: Update `backend/app/main.py` CORS origins with your Vercel URL

### 500 Internal Server Error
**Symptom**: Backend API returns 500
**Fix**: Check platform logs for Python errors, verify DATABASE_URL is correct

### Chatbot Not Working
**Symptom**: Chatbot loads but can't create tasks
**Fix**: Verify OPENAI_API_KEY is set, check backend logs for errors

### Build Fails on Vercel
**Symptom**: Deployment fails during build
**Fix**: Check TypeScript errors, ensure all dependencies in package.json

---

## 📞 Support Resources

- **Vercel**: https://vercel.com/docs
- **Railway**: https://docs.railway.app
- **Render**: https://render.com/docs
- **Hugging Face**: https://huggingface.co/docs/hub/spaces
- **Neon**: https://neon.tech/docs

---

## ✨ Your Project is Ready!

Everything is configured for deployment. Just:
1. Deploy backend to your chosen platform
2. Get backend URL
3. Deploy frontend to Vercel with that URL
4. Test and celebrate! 🎉

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

**Created by Asif Ali AstolixGen for GIAIC Hackathon 2026**
