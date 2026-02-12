# 📧 SendGrid Email Setup Guide

## Why SendGrid?

SendGrid works on **all platforms** including Hugging Face Spaces because it uses HTTPS API instead of SMTP (which is often blocked).

---

## 🚀 Quick Setup (5 minutes)

### **Step 1: Create SendGrid Account**

1. Go to: https://signup.sendgrid.com/
2. Sign up with your email (FREE tier: 100 emails/day)
3. Verify your email address
4. Complete the setup wizard

### **Step 2: Get API Key**

1. Login to SendGrid dashboard
2. Go to: **Settings** → **API Keys** (left sidebar)
3. Click **"Create API Key"** button
4. Settings:
   - **Name:** TaskFlow
   - **Type:** Full Access (or "Restricted Access" with Mail Send permission)
5. Click **"Create & View"**
6. **📋 COPY THE API KEY** (shown only once!)
   - Example: `SG.xxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`

### **Step 3: Verify Sender Email**

1. Go to: **Settings** → **Sender Authentication**
2. Click **"Verify a Single Sender"**
3. Fill form:
   - **From Name:** TaskFlow
   - **From Email Address:** your-email@gmail.com (or any email you own)
   - **Reply To:** same as above
   - **Company details:** (fill as needed)
4. Click **"Create"**
5. **Check your email** and click verification link
6. ✅ Sender verified!

---

## 🔧 Configure Hugging Face Spaces

### **Add Secrets to HF Space:**

1. Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api/settings
2. Scroll to **"Repository secrets"**
3. Add these secrets:

```
Name: SENDGRID_API_KEY
Value: SG.xxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

Name: SENDER_EMAIL
Value: your-verified-email@gmail.com
```

4. Click **"Add secret"** for each
5. Click **"Factory reboot"** to restart Space

---

## ✅ Test Email Notifications

Wait 2 minutes for rebuild, then test:

```bash
# 1. Login
curl -X POST https://asifaliastolixgen-taskflow-api.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your-email@gmail.com","password":"your-password"}' \
  > token.json

# 2. Extract token
TOKEN=$(cat token.json | jq -r '.token')

# 3. Send test email
curl -X POST https://asifaliastolixgen-taskflow-api.hf.space/api/notifications/test-email \
  -H "Authorization: Bearer $TOKEN"
```

**Expected response:**
```json
{
  "message": "Test email sent successfully to your-email@gmail.com",
  "status": "success"
}
```

---

## 📊 Check Logs

### **HF Space Logs:**
1. Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api
2. Click **"Logs"** tab
3. Look for:
   - `Sending email to ... via SendGrid...`
   - `✅ Email sent successfully! Status code: 202`

### **SendGrid Dashboard:**
1. Go to: https://app.sendgrid.com/
2. Click **"Activity"** (left sidebar)
3. See all sent emails with delivery status

---

## 🎯 Benefits Over Gmail SMTP

| Feature | Gmail SMTP | SendGrid API |
|---------|------------|--------------|
| **Works on HF Spaces** | ❌ Blocked | ✅ Yes |
| **Free Tier** | ✅ Unlimited | ✅ 100/day |
| **Delivery Tracking** | ❌ No | ✅ Yes |
| **Spam Score** | ⚠️ High | ✅ Low |
| **Setup Time** | 10 min | 5 min |

---

## 📝 Environment Variables

### **Local Development (backend/.env):**
```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
SENDER_EMAIL=your-verified-email@gmail.com
```

### **Production (HF Secrets):**
Same variables added as secrets in HF Space settings.

---

## 🐛 Troubleshooting

### **"SendGrid API key not configured"**
- Check `SENDGRID_API_KEY` is set in HF secrets
- Restart HF Space after adding secrets

### **"403 Forbidden" or "401 Unauthorized"**
- API key is incorrect
- Regenerate API key in SendGrid dashboard

### **"The from email does not match a verified Sender Identity"**
- `SENDER_EMAIL` must be verified in SendGrid
- Go to Settings → Sender Authentication → Verify

### **Emails not arriving:**
- Check spam folder
- Check SendGrid Activity dashboard for delivery status
- Verify recipient email is correct

---

## 🎬 Next Steps

After setup:
1. ✅ Test email endpoint works
2. ✅ Create a task with reminder date
3. ✅ Wait 10 minutes (scheduler runs)
4. ✅ Check email inbox for reminder!

---

**Created by Asif Ali AstolixGen | GIAIC Hackathon 2026**
