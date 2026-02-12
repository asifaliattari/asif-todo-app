# Deploy TaskFlow Backend to Railway.app

## Step 1: Sign Up for Railway

1. Go to: https://railway.app/
2. Click **"Start a New Project"**
3. Sign in with **GitHub** (recommended)
4. Authorize Railway to access your repositories

## Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose repository: **`asif-todo-app`**
4. Railway will detect it's a monorepo

## Step 3: Configure Backend Service

1. Railway will ask: **"What to deploy?"**
2. Click **"Add Service"** → **"GitHub Repo"**
3. In the configuration:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Step 4: Add Environment Variables

Click on your service → **"Variables"** tab → Add these:

```
DATABASE_URL=postgresql://neondb_owner:YOUR_PASSWORD@ep-xxxxx.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-here
OPENAI_API_KEY=sk-your-openai-key-here
```

**Important:** Use the SAME values you have in your local `backend/.env` file!

## Step 5: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Once deployed, Railway will give you a URL like:
   - `https://your-app-production.up.railway.app`

## Step 6: Get Your Railway URL

1. Click on your service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**
5. Copy the URL (e.g., `https://taskflow-api-production.up.railway.app`)

## Step 7: Update Vercel Frontend

1. Go to Vercel dashboard: https://vercel.com/
2. Select your **"asif-todo-app"** project
3. Go to **"Settings"** → **"Environment Variables"**
4. Update or add:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-url.up.railway.app
   ```
5. **Redeploy** your frontend (Go to Deployments → click ⋯ → Redeploy)

## Step 8: Update Local Code

Update `frontend/vercel.json`:

```json
{
  "buildCommand": "cd frontend && npm run build",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install",
  "framework": "nextjs",
  "outputDirectory": "frontend/.next",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://your-railway-url.up.railway.app",
    "NEXT_PUBLIC_APP_NAME": "TaskFlow",
    "NEXT_PUBLIC_AUTHOR": "Asif Ali AstolixGen",
    "NEXT_PUBLIC_HACKATHON": "GIAIC Hackathon 2026"
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-railway-url.up.railway.app/api/:path*"
    }
  ]
}
```

Commit and push:
```bash
git add frontend/vercel.json
git commit -m "Update backend URL to Railway"
git push origin main
```

## Step 9: Test Your Deployment

```bash
# Test health
curl https://your-railway-url.up.railway.app/api/health

# Test signup
curl -X POST https://your-railway-url.up.railway.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"Test12345678"}'
```

## Troubleshooting

### If deployment fails:

1. **Check Logs**: Railway → Service → "Logs" tab
2. **Verify Environment Variables**: Make sure all 3 are set correctly
3. **Check Build**: Make sure `backend/requirements.txt` has `bcrypt>=4.0.1`

### If database connection fails:

1. Make sure `DATABASE_URL` has `?sslmode=require` at the end
2. Make sure Neon database allows connections from Railway
3. Test the connection string locally first

## Benefits of Railway vs Hugging Face

✅ **Better for FastAPI backends**
✅ **Reliable database connections**
✅ **No cold starts**
✅ **Easier environment variable management**
✅ **Better logs and monitoring**
✅ **Free tier: 500 hours/month**

---

## Need Help?

Railway has great docs: https://docs.railway.app/

Contact: support@railway.app
