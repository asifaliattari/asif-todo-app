# 🔧 Hugging Face Space Environment Setup

## Issue
Backend is deployed but getting 500 errors because environment variables are not configured.

## Solution

### Step 1: Get Your Neon Database URL

1. Go to: https://console.neon.tech/app/projects/solitary-art-70032711
2. Click on your project
3. Click "Connection Details" or "Connection String"
4. Copy the connection string (should look like):
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### Step 2: Add Secrets to Hugging Face

1. **Go to your Space settings:**
   https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api/settings

2. **Find "Variables and secrets" or "Repository secrets" section**

3. **Add Secret #1: DATABASE_URL**
   - Click "+ Add a secret" or "+ New secret"
   - Name: `DATABASE_URL`
   - Value: [Paste your Neon connection string]
   - Click "Save" or "Add"

4. **Add Secret #2: SECRET_KEY**
   - Click "+ Add a secret"
   - Name: `SECRET_KEY`
   - Value: `EW1LZCuWtQ2RUzAWJ3GSptFVmALU+owmwOjFvl06Dco=`
   - Click "Save" or "Add"

### Step 3: Restart the Space

After adding secrets, the Space should automatically restart. If not:
1. Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api
2. Click "⋮" (three dots menu)
3. Click "Restart Space" or "Factory reboot"

### Step 4: Wait for Rebuild

- The Space will rebuild (takes 2-3 minutes)
- Status will show "Building..." then "Running"
- Check logs for any errors

### Step 5: Test Again

Once running, test the health endpoint:
```bash
curl https://asifaliastolixgen-taskflow-api.hf.space/api/health
```

Should return:
```json
{"status":"healthy","timestamp":"...","version":"1.0.0"}
```

## Troubleshooting

### "DATABASE_URL not found" error
- Make sure you saved the secret correctly
- Secret name must be exactly: `DATABASE_URL` (case-sensitive)
- Restart the Space after adding secrets

### Connection refused or timeout
- Check Neon database is active
- Verify connection string format
- Ensure `?sslmode=require` is at the end

### "Secret key must be set" error
- Add `SECRET_KEY` environment variable
- Restart the Space

## Visual Guide

1. **Settings Page:**
   ```
   Hugging Face Space → Settings → Variables and secrets
   ```

2. **Add Secret Button:**
   ```
   [+ Add a secret] or [+ New secret]
   ```

3. **Secret Form:**
   ```
   Name: DATABASE_URL
   Value: postgresql://...
   [Save]
   ```

## Expected Result

After configuration:
✅ Health endpoint returns 200 OK
✅ API docs accessible at /docs
✅ Can create user accounts
✅ Can login and get JWT token
✅ Can perform CRUD operations

---

**Once configured, run the test again and everything should work!**
