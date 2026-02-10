# 🚀 Phase III Setup Guide

## ✅ What's Been Done

I've set up the foundation for Phase III! Here's what's ready:

### Backend
- ✅ MCP Tools created (`backend/mcp/tools.py`)
- ✅ Chat API router (`backend/app/routers/chat.py`)
- ✅ 6 AI tools defined:
  - create_task
  - list_tasks
  - update_task
  - delete_task
  - mark_task_complete
  - get_task_stats
- ✅ Claude AI integration ready
- ✅ Dependencies updated (anthropic, httpx)

### Frontend
- ✅ Chatbot component created (`frontend/components/Chatbot.tsx`)
- ✅ Floating chat button
- ✅ Beautiful chat interface
- ✅ Message history
- ✅ Loading states
- ✅ Added to layout (available on all pages)

### Configuration
- ✅ New git branch: `phase-3-ai-chatbot`
- ✅ Environment example updated
- ✅ All files committed

---

## 🔧 What You Need To Do Next

### Step 1: Get Anthropic API Key (5 minutes)

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Click "API Keys" in sidebar
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)

### Step 2: Install Backend Dependencies (2 minutes)

```bash
cd backend
pip install -r requirements.txt
```

Or with uv:
```bash
cd backend
uv sync
```

### Step 3: Add API Key Locally (1 minute)

```bash
cd backend
# Add to your .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env
```

### Step 4: Test Locally (5 minutes)

**Terminal 1 - Backend:**
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Test Chat:**
1. Open http://localhost:3000
2. Login to your account
3. Look for floating chat button (bottom-right corner)
4. Click to open chat
5. Try: "Add a task to buy milk"
6. Try: "What are my tasks?"
7. Try: "Mark my first task as complete"

---

##  Example Conversations

**Creating Tasks:**
```
You: "Add a task to buy groceries"
AI: "I've created a task for you: 'Buy groceries'. Anything else?"

You: "Add finish hackathon to my list"
AI: "Done! Added 'Finish hackathon' to your tasks."
```

**Viewing Tasks:**
```
You: "What are my tasks?"
AI: "You have 2 active tasks:
1. Buy groceries
2. Finish hackathon"

You: "Show me completed tasks"
AI: "You don't have any completed tasks yet. Get started!"
```

**Completing Tasks:**
```
You: "I finished buying groceries"
AI: "Awesome! I've marked 'Buy groceries' as complete. 1 task remaining."
```

---

## 🚀 Ready to Deploy!

Once testing works locally, you're ready to deploy!

**See PHASE_3_DEPLOYMENT.md for deployment steps**

---

## 🆘 Troubleshooting

**Chat button not appearing?**
- Clear browser cache
- Check browser console for errors
- Verify Chatbot component is imported

**AI not responding?**
- Check ANTHROPIC_API_KEY is set
- Check backend logs
- Verify API key is valid

**Tools not working?**
- Check you're logged in
- Verify JWT token in localStorage
- Check backend /api/tasks endpoints work

---

**You're ready to test! Get your API key and start chatting!** 🤖✨
