# 🧪 Quick Test Guide - AI Chatbot

## Step 1: Update .env File (2 minutes)

Open: `D:\hakathon\asif_todo_app_phase2\backend\.env`

You need to replace TWO things:

### 1. DATABASE_URL
Get from: https://console.neon.tech/app/projects/solitary-art-70032711
- Copy your Neon connection string
- Replace the DATABASE_URL line

### 2. OPENAI_API_KEY
- Add your OpenAI API key (the one you mentioned you have)
- Replace: `sk-proj-your-openai-key-here` with your actual key

Example of how it should look:
```
DATABASE_URL=postgresql://neondb_owner:npg_abc123...@ep-solitary-art-a12345.us-east-2.aws.neon.tech/neondb?sslmode=require
OPENAI_API_KEY=sk-proj-abc123youractualkeyhere456
```

## Step 2: Install OpenAI Package (1 minute)

```bash
cd backend
pip install openai
```

## Step 3: Start Backend (1 minute)

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Should see: "Application startup complete"

## Step 4: Start Frontend (1 minute)

Open NEW terminal:
```bash
cd frontend
npm run dev
```

Should see: "Ready on http://localhost:3000"

## Step 5: Test Chat! (5 minutes)

1. **Open browser**: http://localhost:3000
2. **Login** to your account
3. **Look for chat button** (bottom-right corner, purple gradient)
4. **Click it** to open chat
5. **Try these messages**:

### Test 1: Greeting
```
You: "Hi there!"
Expected: Friendly greeting from AI
```

### Test 2: Create Task
```
You: "Add a task to buy groceries"
Expected: "Got it! I've added 'Buy groceries' to your list 🛒"
```

### Test 3: List Tasks
```
You: "What tasks do I have?"
Expected: Lists all your active tasks
```

### Test 4: Complete Task
```
You: "I finished buying groceries"
Expected: "Awesome! Marked as complete"
```

### Test 5: Get Stats
```
You: "How am I doing?"
Expected: Shows your task statistics
```

## ✅ Success Indicators

Chat is working if:
- ✅ Chat button appears
- ✅ Chat window opens
- ✅ AI responds to messages
- ✅ Tasks are created when asked
- ✅ AI uses emojis and friendly tone
- ✅ Context is maintained in conversation

## ❌ Troubleshooting

**"AI service not configured"**
→ Check OPENAI_API_KEY is set in .env

**"Failed to send message"**
→ Make sure you're logged in
→ Check backend is running on port 8000

**Chat button not showing**
→ Clear browser cache
→ Check browser console (F12)

**AI not responding**
→ Check backend logs for errors
→ Verify API key is valid
→ Check OpenAI account has credits

## 🎉 If Everything Works

You should see:
- Friendly, conversational AI responses
- Tasks created/updated through chat
- Emojis and warm personality
- Smooth, human-like conversation

---

**Ready? Update your .env file and let's test!** 🚀
