# 📧 Email Notifications Setup Guide

## Overview

TaskFlow now supports **automated email reminders** for tasks! You'll receive emails when:
- ⏰ Task is due in 1 hour
- 🔔 Task is due now
- ⚠️ Task is overdue

---

## 🔧 Setup Instructions

### **Step 1: Enable Gmail App Password**

1. **Go to Google Account Settings:**
   - Visit: https://myaccount.google.com/security
   - Login with your Gmail account

2. **Enable 2-Step Verification:**
   - Scroll to "Signing in to Google"
   - Click "2-Step Verification"
   - Follow the setup wizard
   - ✅ Verify with your phone

3. **Create App Password:**
   - After enabling 2-Step, go back to Security
   - Click "App passwords" (or visit: https://myaccount.google.com/apppasswords)
   - Select app: **Mail**
   - Select device: **Other** (enter "TaskFlow")
   - Click **Generate**
   - 📋 **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

---

### **Step 2: Configure Environment Variables**

#### **For Local Development:**

Edit `backend/.env` file:

```env
# Email Configuration
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop

# Existing variables
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
OPENAI_API_KEY=...
```

#### **For Hugging Face Deployment:**

1. Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api/settings
2. Scroll to **"Repository secrets"**
3. Add these secrets:

```
Name: SMTP_EMAIL
Value: your-email@gmail.com

Name: SMTP_PASSWORD
Value: abcd efgh ijkl mnop
```

4. Click **"Restart Space"** to apply changes

---

### **Step 3: Test Email Notifications**

#### **Option A: Test via API**

```bash
# Login first
curl -X POST https://asifaliastolixgen-taskflow-api.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your-email@gmail.com","password":"your-password"}' \
  > token.json

# Extract token
TOKEN=$(cat token.json | jq -r '.token')

# Send test email
curl -X POST https://asifaliastolixgen-taskflow-api.hf.space/api/notifications/test-email \
  -H "Authorization: Bearer $TOKEN"
```

#### **Option B: Test via Frontend**

1. Go to: https://asif-todo-app.vercel.app
2. Login with your account
3. Create a task with:
   - Title: "Test Email Reminder"
   - Due Date: 30 minutes from now
   - Priority: High
4. Wait 20 minutes
5. Check your email inbox! 📧

---

## 📅 How Email Reminders Work

### **Automatic Checks:**
- Scheduler runs **every 10 minutes**
- Checks all tasks with `reminder_date` set
- Sends emails if reminder time has passed

### **Email Types:**

#### **1. Due Soon (1 hour before)**
- Subject: ⏰ Reminder: [Task Title]
- Sent: 1 hour before due date
- Color: Yellow

#### **2. Due Now**
- Subject: 🔔 Reminder: [Task Title]
- Sent: When due date is reached
- Color: Blue

#### **3. Overdue**
- Subject: ⚠️ Reminder: [Task Title]
- Sent: After due date has passed
- Color: Red

---

## 🎨 Email Template Features

### **Beautiful HTML Emails:**
- ✅ Gradient header (purple theme)
- ✅ Task card with priority badge
- ✅ Tags displayed
- ✅ Due date highlighted
- ✅ "View Task in App" button
- ✅ Mobile-responsive design

### **Example Email:**

```
┌─────────────────────────────────┐
│  🔔 TaskFlow                     │
│  Task Due Now!                  │
├─────────────────────────────────┤
│ Hi Asif Ali! 👋                 │
│                                 │
│ This task is due now:           │
│                                 │
│ ┌─────────────────────────────┐│
│ │ Pakistan Independence Day   ││
│ │ [🔴 HIGH]                   ││
│ │                             ││
│ │ Celebrate Pakistan's 79th   ││
│ │ Independence Day            ││
│ │                             ││
│ │ #pakistan #holiday          ││
│ │                             ││
│ │ 📅 Due: August 14, 2026     ││
│ │        12:00 PM             ││
│ └─────────────────────────────┘│
│                                 │
│      [View Task in App]         │
│                                 │
└─────────────────────────────────┘
```

---

## 🔐 Security Notes

### **App Password vs Regular Password:**
- ✅ **Use App Password** (16 characters)
- ❌ **Don't use your regular Gmail password**
- App passwords are safer and can be revoked anytime

### **Environment Variables:**
- Stored securely on Hugging Face (encrypted)
- Never committed to Git
- Only accessible to your Space

---

## 🐛 Troubleshooting

### **"Failed to send email" Error:**

**Check:**
1. ✅ SMTP_EMAIL is correct Gmail address
2. ✅ SMTP_PASSWORD is the App Password (16 chars)
3. ✅ 2-Step Verification is enabled
4. ✅ Environment variables are set on HF
5. ✅ Space has been restarted

**Solution:**
```bash
# Test credentials locally first
cd backend
uv run python -c "
from app.email_service import email_service
print('Sending test...')
result = email_service.send_email(
    'your-email@gmail.com',
    'Test Subject',
    '<h1>Test Email</h1>'
)
print(f'Result: {result}')
"
```

### **Not Receiving Emails:**

**Check:**
1. ✅ Spam/Junk folder
2. ✅ Gmail filters
3. ✅ Email address is correct
4. ✅ Reminder date is set correctly
5. ✅ Task is not already completed

---

## 📊 Scheduler Status

### **Check if Scheduler is Running:**

```bash
# View HF Space logs
# Go to: https://huggingface.co/spaces/AsifAliAstolixgen/taskflow-api
# Click "Logs" tab
# Look for:
# "Scheduler started - checking reminders every 10 minutes"
```

### **Manually Trigger Reminder Check:**

```bash
# (Admin only)
curl -X POST https://asifaliastolixgen-taskflow-api.hf.space/api/notifications/trigger-reminders \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎯 Best Practices

### **Setting Reminders:**
- Set `reminder_date` 1 hour before `due_date`
- Use high priority for important tasks
- Add descriptive tags for context

### **Email Management:**
- Check email regularly
- Mark task as complete to stop reminders
- Create Gmail filter for TaskFlow emails

---

## 📈 Usage Statistics

After setup, you'll have:
- ✅ Automated email reminders
- ✅ No manual checking needed
- ✅ Never miss a deadline
- ✅ Beautiful HTML emails
- ✅ Mobile-friendly notifications

---

## 🎬 Demo Video Tip

**Show email notification in demo:**
1. Create task with due date 2 minutes from now
2. While recording, check email
3. Show the email arriving
4. Click "View Task in App" button
5. Shows integration works! 🎥

---

**Created by Asif Ali AstolixGen | GIAIC Hackathon 2026**
