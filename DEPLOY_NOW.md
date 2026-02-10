# 🚀 DEPLOY NOW - Step by Step Guide

Follow these exact steps to deploy your project in 20 minutes!

---

## ✅ Pre-Deployment Checklist

- [x] Code committed to GitHub: YES
- [x] All features working locally: YES
- [x] Environment variables documented: YES
- [x] Ready to deploy: YES

---

## 📝 What You'll Need

**From your .env files:**
1. `DATABASE_URL` (from backend/.env)
2. `BETTER_AUTH_SECRET` (from backend/.env)
3. `OPENAI_API_KEY` (from backend/.env)

**Accounts needed:**
1. Vercel account (free): vercel.com
2. Railway account (free): railway.app

---

## STEP 1: Deploy Frontend to Vercel (5 minutes)

### 1.1 Go to Vercel
```
Open: https://vercel.com/new
```

### 1.2 Import GitHub Repository
- Click "Import Git Repository"
- Select: `asifaliattari/asif-todo-app`
- Click "Import"

### 1.3 Configure Project
**IMPORTANT: Set these exactly:**
- Project Name: `taskflow` (or your choice)
- Framework Preset: Next.js (auto-detected)
- Root Directory: `frontend` ⚠️ CRITICAL
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)

### 1.4 Environment Variables
Click "Environment Variables" and add:

```
NEXT_PUBLIC_API_URL=https://asifaliastolixgen-taskflow-api.hf.space
NEXT_PUBLIC_APP_NAME=TaskFlow
NEXT_PUBLIC_AUTHOR=Asif Ali AstolixGen
NEXT_PUBLIC_HACKATHON=GIAIC Hackathon 2026
```

**Note:** We'll update NEXT_PUBLIC_API_URL after deploying backend

### 1.5 Deploy!
- Click "Deploy"
- Wait 2-3 minutes for build
- You'll get a URL like: `https://taskflow.vercel.app`

### 1.6 Save Your URL
```
Frontend URL: ___________________________
```

---

## STEP 2: Update Backend on Hugging Face Spaces (5 minutes)

**Good news!** Your backend is already deployed at:
```
https://asifaliastolixgen-taskflow-api.hf.space
```

### 2.1 Verify Latest Code is Deployed
```bash
# Check current backend version
curl https://asifaliastolixgen-taskflow-api.hf.space/api/health
```

### 2.2 Update Environment Variables (if needed)
Go to your Hugging Face Space settings:
```
Open: https://huggingface.co/spaces/asifaliastolixgen/taskflow-api/settings
```

Ensure these variables are set:
```env
DATABASE_URL=postgresql://neondb_owner:npg_KXME4ua0Cnvo@ep-snowy-hill-ai5atl3i-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

BETTER_AUTH_SECRET=EW1LZCuWtQ2RUzAWJ3GSptFVmALU+owmwOjFvl06Dco=

OPENAI_API_KEY=<YOUR_OPENAI_KEY>

OPENAI_MODEL=gpt-4o-mini

FRONTEND_URL=<YOUR_VERCEL_URL>

ENVIRONMENT=production
```

### 2.3 Push Latest Changes (if needed)
If you've made changes to the backend:
```bash
# Hugging Face Spaces automatically redeploys on git push
git push origin main
```

### 2.4 Test Backend
```bash
curl https://asifaliastolixgen-taskflow-api.hf.space/api/health
```

Should return: `{"status":"healthy"}`

### 2.5 Your Backend URL
```
Backend URL: https://asifaliastolixgen-taskflow-api.hf.space
```

---

## STEP 3: Connect Frontend to Backend (2 minutes)

### 3.1 Update Vercel Environment Variable
- Go to your Vercel project dashboard
- Click "Settings" → "Environment Variables"
- Find `NEXT_PUBLIC_API_URL`
- Click "Edit"
- Set to: `https://asifaliastolixgen-taskflow-api.hf.space`
- Save

### 3.2 Redeploy Frontend
- Go to "Deployments" tab
- Click "..." menu on latest deployment
- Click "Redeploy"
- Wait 2 minutes

---

## STEP 4: Update Backend CORS (2 minutes)

### 4.1 Update backend/app/main.py locally

Find the CORS middleware section and update:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-app.vercel.app",  # Your Vercel URL
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 Commit and Push
```bash
git add backend/app/main.py
git commit -m "Update CORS for production"
git push origin main
```

Hugging Face Spaces will auto-deploy the update.

---

## ✅ STEP 5: Test Everything!

### 5.1 Test Frontend
```
Open: https://your-vercel-app.vercel.app
```

Should see: TaskFlow login page

### 5.2 Test Signup
- Click "Sign Up"
- Create test account
- Should redirect to dashboard

### 5.3 Test CRUD
- Create a task
- Mark it complete
- Delete it

### 5.4 Test Chatbot
- Click chatbot icon (bottom right)
- Type: "Create a task to test deployment"
- Should create the task!

### 5.5 Test API
```bash
curl https://asifaliastolixgen-taskflow-api.hf.space/api/health
curl https://asifaliastolixgen-taskflow-api.hf.space/docs
```

---

## 🎉 SUCCESS CHECKLIST

- [ ] Frontend deployed to Vercel
- [ ] Backend updated on Hugging Face Spaces
- [ ] Frontend connects to backend
- [ ] Can signup/login
- [ ] Can create/edit/delete tasks
- [ ] Chatbot works
- [ ] API accessible

---

## 🎬 Record Demo Video

Now that everything is live, record your demo:

### Recording Steps:
1. Open your Vercel URL
2. Start screen recording (Windows: Win+G, Mac: Cmd+Shift+5)
3. Follow demo script
4. Save video (should be 60-90 seconds)

### Demo Script:
1. Show login page (3s)
2. Sign up new user (7s)
3. Create 2-3 tasks (10s)
4. Mark one complete (3s)
5. Open chatbot (2s)
6. Say "Create a task to prepare hackathon demo" (5s)
7. Show task appears (5s)
8. Say "What are my tasks?" (5s)
9. Show AI lists them (5s)
10. Show the URL (show it's live!) (5s)
11. Close with "TaskFlow - All 5 Phases Complete" (5s)

---

## 📊 Your Live URLs

```
Frontend: https://_________________.vercel.app
Backend:  https://asifaliastolixgen-taskflow-api.hf.space
API Docs: https://asifaliastolixgen-taskflow-api.hf.space/docs
GitHub:   https://github.com/asifaliattari/asif-todo-app
```

---

## 🆘 Troubleshooting

### Frontend shows "Network Error"
- Check NEXT_PUBLIC_API_URL in Vercel
- Make sure it's set to: `https://asifaliastolixgen-taskflow-api.hf.space`
- Redeploy frontend

### Backend issues on Hugging Face Spaces
- Check logs in Hugging Face Spaces dashboard
- Verify all environment variables are set in Space settings
- Check DATABASE_URL is correct

### Chatbot doesn't work
- Check OPENAI_API_KEY in Hugging Face Space settings
- Check browser console for errors
- Verify backend logs in Hugging Face Spaces

### CORS errors
- Update main.py CORS origins
- Add your Vercel URL
- Commit and push

---

## 📞 Need Help?

If stuck, check:
1. Hugging Face Spaces logs (Space dashboard → Logs)
2. Vercel logs (Vercel dashboard → Deployments → View Function Logs)
3. Browser console (F12)

---

## 🏆 You're Done!

Once everything works:
1. ✅ Note your live URLs
2. ✅ Record demo video
3. ✅ Submit to hackathon
4. ✅ Celebrate! 🎉

---

**Your project is LIVE and ready to win!** 🚀
