# 🔍 Backend Troubleshooting Guide

## Issue
Backend returns "Internal Server Error" (500) even though environment variables are set.

## Diagnostic Steps

### Step 1: Check Hugging Face Space Logs

1. Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api
2. Click on "Logs" tab (usually at the top)
3. Look for error messages, especially:
   - Database connection errors
   - "DATABASE_URL not found"
   - "connection refused"
   - "authentication failed"
   - SSL/TLS errors

### Step 2: Verify Environment Variables

Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api/settings

Check that you have EXACTLY these two secrets:

#### SECRET 1: DATABASE_URL
**Name (case-sensitive)**: `DATABASE_URL`
**Value format should be**:
```
postgresql://username:password@host.region.aws.neon.tech/dbname?sslmode=require
```

Common issues:
- ❌ Missing `?sslmode=require` at the end
- ❌ Wrong username/password
- ❌ Database name is wrong
- ❌ Host URL is incorrect

**How to get correct value:**
1. Go to: https://console.neon.tech/app/projects/solitary-art-70032711
2. Click on your database
3. Look for "Connection Details" or "Connection String"
4. Copy the FULL string (including `?sslmode=require`)

#### SECRET 2: SECRET_KEY
**Name (case-sensitive)**: `SECRET_KEY`
**Value**: `EW1LZCuWtQ2RUzAWJ3GSptFVmALU+owmwOjFvl06Dco=`

### Step 3: Verify Neon Database is Active

1. Go to: https://console.neon.tech/app/projects/solitary-art-70032711
2. Check that project status shows "Active" (not sleeping/paused)
3. If paused, click to wake it up

### Step 4: Test Database Connection

Try to connect to your database using psql or any PostgreSQL client:

```bash
psql "postgresql://username:password@host.region.aws.neon.tech/dbname?sslmode=require"
```

If this fails, the connection string is incorrect.

### Step 5: Force Restart Space

1. Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api
2. Click "⋮" (three dots menu) or Settings
3. Look for "Factory reboot" or "Restart Space"
4. Click to restart
5. Wait 2-3 minutes for rebuild

### Step 6: Check Space Build Status

After restart:
1. Watch the build logs
2. Look for:
   - ✅ "Successfully built"
   - ✅ "Application startup complete"
   - ❌ Any error messages

## Common Errors and Fixes

### Error: "DATABASE_URL environment variable not set"
**Fix**: Secret name must be exactly `DATABASE_URL` (all caps)

### Error: "connection refused" or "could not connect to server"
**Fix**:
- Check Neon database is active
- Verify host URL is correct
- Ensure `?sslmode=require` is included

### Error: "password authentication failed"
**Fix**: Username or password in connection string is wrong

### Error: "database does not exist"
**Fix**: Database name in connection string doesn't match

### Error: "SSL connection required"
**Fix**: Add `?sslmode=require` to end of connection string

## Quick Test Script

Run this to test if backend is working:

```bash
# Test health (should work)
curl https://asifaliastolixgen-taskflow-api.hf.space/api/health

# Test signup (should return user data or specific error)
curl -X POST https://asifaliastolixgen-taskflow-api.hf.space/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!","name":"Test"}'
```

Expected responses:
- ✅ Health: `{"status":"healthy",...}`
- ✅ Signup success: `{"access_token":"...","user":{...}}`
- ✅ Signup duplicate: `{"detail":"Email already registered"}`
- ❌ Signup 500: Database connection issue

## If Still Not Working

### Option 1: Check Neon Connection String Format

Your connection string should look like:
```
postgresql://[username]:[password]@ep-[xxx]-[xxx].us-east-2.aws.neon.tech/[dbname]?sslmode=require
```

Parts:
- `postgresql://` - Protocol
- Username - Usually from Neon
- Password - From Neon (might have special characters)
- Host - Format: `ep-xxx-xxx.region.aws.neon.tech`
- Database name - Usually `neondb`
- `?sslmode=require` - Required for SSL

### Option 2: Recreate the Secret

Sometimes secrets don't update properly:
1. Delete the DATABASE_URL secret
2. Wait 10 seconds
3. Add it again with correct value
4. Restart Space

### Option 3: Check for Special Characters

If your database password has special characters (@, #, $, etc.):
- They might need URL encoding
- Example: `p@ssw0rd` becomes `p%40ssw0rd`
- Or get a new connection string from Neon

### Option 4: Use Connection Pooler

In Neon dashboard:
1. Look for "Connection pooler" or "Pooled connection"
2. Use that URL instead of direct connection
3. Format: `postgresql://...?sslmode=require&pooler=true`

## Still Having Issues?

Share these details:
1. Screenshot of Hugging Face Space logs (last 50 lines)
2. Screenshot of Neon database status
3. First 20 characters of your connection string (hide password)
4. Any specific error messages

---

**Most Common Issue**: Connection string missing `?sslmode=require` at the end!
