# Hugging Face Spaces Deployment Guide

## 🚀 Quick Deployment

### Option 1: Using Git (Recommended)

1. **Create a Hugging Face Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `taskflow-api`
   - SDK: Docker
   - Hardware: CPU basic (free)

2. **Clone your Space**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/taskflow-api
   cd taskflow-api
   ```

3. **Copy backend files**
   ```bash
   # Copy all backend files to the Space directory
   cp -r D:/hakathon/asif_todo_app_phase2/backend/* .

   # Move README_HF.md to README.md
   mv README_HF.md README.md
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

5. **Configure Secrets**
   - Go to your Space settings
   - Add secrets:
     - `DATABASE_URL`: Your Neon PostgreSQL URL
     - `SECRET_KEY`: Generate with `openssl rand -base64 32`
     - `FRONTEND_URL`: Your Vercel URL (or leave blank for now)

### Option 2: Using Hugging Face CLI

1. **Install Hugging Face CLI**
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   ```

2. **Create and upload Space**
   ```bash
   cd D:/hakathon/asif_todo_app_phase2/backend
   huggingface-cli upload-space . YOUR_USERNAME/taskflow-api --repo-type space
   ```

## 🔧 Environment Variables

Add these in Space Settings → Variables and secrets:

| Variable | Value | Required |
|----------|-------|----------|
| `DATABASE_URL` | `postgresql://user:pass@host/db?sslmode=require` | ✅ Yes |
| `SECRET_KEY` | Generate: `openssl rand -base64 32` | ✅ Yes |
| `FRONTEND_URL` | Your Vercel frontend URL | ❌ Optional |

## 🧪 Testing Deployment

Once deployed, your API will be at:
```
https://YOUR_USERNAME-taskflow-api.hf.space
```

Test endpoints:
- Health: `https://YOUR_USERNAME-taskflow-api.hf.space/api/health`
- Docs: `https://YOUR_USERNAME-taskflow-api.hf.space/docs`
- Root: `https://YOUR_USERNAME-taskflow-api.hf.space/`

## 📝 Post-Deployment Checklist

- [ ] Space is running (green status)
- [ ] `/api/health` returns healthy status
- [ ] `/docs` shows Swagger UI
- [ ] Can signup a new user
- [ ] Can login and get JWT token
- [ ] Database connection works

## 🐛 Troubleshooting

### Build fails
- Check Dockerfile syntax
- Ensure requirements.txt has all dependencies
- Check Space logs for errors

### Database connection error
- Verify DATABASE_URL is set correctly
- Ensure Neon database is active
- Check SSL mode: `?sslmode=require`

### CORS errors
- CORS is set to allow all origins (`*`)
- If issues persist, check browser console

## 🔄 Updating Deployment

To update your deployed Space:
```bash
cd /path/to/space/clone
# Make changes
git add .
git commit -m "Update: description"
git push
```

Space will automatically rebuild and redeploy.
