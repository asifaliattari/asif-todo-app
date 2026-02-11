# Chat API Endpoint Specification

**Component**: Chat API Endpoint
**Purpose**: Stateless conversational interface for task management
**Phase**: III - AI Integration

---

## Overview

The chat endpoint provides a stateless REST API for conversational task management. All conversation state is persisted to the database, allowing any backend instance to handle any request.

## Architecture Principle: Stateless Server

```
Request → Fetch History from DB → Build Context → Call Agent → Store Response → Return
```

**Key Benefits**:
- Any server instance can handle any request
- Horizontal scaling
- Server restarts don't lose conversation state
- Resilient to failures

---

## Endpoint Specification

### POST /api/{user_id}/chat

Send a message and receive AI assistant response.

**Authentication**: Required (JWT token)

**Request Body**:
```json
{
  "message": "string (required)",
  "conversation_id": "integer (optional)"
}
```

**Response**:
```json
{
  "conversation_id": 123,
  "response": "string",
  "tool_calls": [
    {
      "tool": "create_task",
      "parameters": {"title": "Buy groceries"},
      "result": {"task_id": 456, "status": "created"}
    }
  ],
  "timestamp": "2026-02-11T10:30:00Z"
}
```

---

## Request Flow (Stateless Cycle)

### Step 1: Receive User Message
```python
@router.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user_id)
):
    # Validate user matches authenticated user
    if user_id != current_user:
        raise HTTPException(403, "Not authorized")
```

### Step 2: Fetch Conversation History
```python
# Get or create conversation
if request.conversation_id:
    conversation = session.get(Conversation, request.conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(404, "Conversation not found")
else:
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()

# Fetch message history
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation.id)
    .order_by(Message.created_at)
).all()
```

### Step 3: Build Message Array for Agent
```python
# Convert DB messages to agent format
agent_messages = [
    {"role": msg.role, "content": msg.content}
    for msg in messages
]

# Add new user message
agent_messages.append({
    "role": "user",
    "content": request.message
})
```

### Step 4: Store User Message
```python
user_message = Message(
    conversation_id=conversation.id,
    role="user",
    content=request.message
)
session.add(user_message)
session.commit()
```

### Step 5: Run Agent with MCP Tools
```python
# Initialize agent with tools and context
from openai import OpenAI
from backend.mcp.tools import TaskTools

client = OpenAI()
tools = TaskTools(backend_url=BACKEND_API_URL)

# Run agent
response = await client.chat.completions.create(
    model="gpt-4",
    messages=agent_messages,
    tools=tools.get_tool_definitions(),
    user=user_id
)

# Extract response and tool calls
assistant_message = response.choices[0].message
tool_calls = assistant_message.tool_calls or []
```

### Step 6: Execute Tool Calls (if any)
```python
tool_results = []
for tool_call in tool_calls:
    tool_name = tool_call.function.name
    tool_params = json.loads(tool_call.function.arguments)

    # Add user_id to parameters
    tool_params["user_id"] = user_id

    # Execute tool via MCP
    result = await tools.execute_tool(tool_name, tool_params)
    tool_results.append({
        "tool": tool_name,
        "parameters": tool_params,
        "result": result
    })
```

### Step 7: Store Assistant Response
```python
assistant_msg = Message(
    conversation_id=conversation.id,
    role="assistant",
    content=assistant_message.content,
    tool_calls=json.dumps(tool_results) if tool_results else None
)
session.add(assistant_msg)
session.commit()
```

### Step 8: Return Response
```python
return ChatResponse(
    conversation_id=conversation.id,
    response=assistant_message.content,
    tool_calls=tool_results,
    timestamp=datetime.utcnow()
)
```

### Step 9: Server State Reset
```python
# Server holds NO state after response is sent
# Next request can be handled by any server instance
# All context is in database
```

---

## Data Models

### Request Model
```python
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
```

### Response Model
```python
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]
    timestamp: datetime
```

---

## Error Handling

### User Not Found (403)
```json
{
  "detail": "Not authorized to access this conversation"
}
```

### Conversation Not Found (404)
```json
{
  "detail": "Conversation not found"
}
```

### Invalid Message (400)
```json
{
  "detail": "Message cannot be empty"
}
```

### Agent Failure (500)
```json
{
  "detail": "AI service temporarily unavailable",
  "error_code": "AGENT_ERROR"
}
```

### Tool Execution Error (200 with error in response)
```json
{
  "conversation_id": 123,
  "response": "I tried to create the task but encountered an error: Task title is required",
  "tool_calls": [
    {
      "tool": "create_task",
      "parameters": {"title": ""},
      "result": {"success": false, "error": "Title is required"}
    }
  ]
}
```

---

## Natural Language Examples

### Creating Tasks
**User**: "Add a task to buy groceries"
**Agent**: Calls `create_task(title="Buy groceries")`
**Response**: "I've added 'Buy groceries' to your task list."

### Listing Tasks
**User**: "What do I need to do today?"
**Agent**: Calls `list_tasks(status="active")`
**Response**: "You have 3 active tasks: 1. Buy groceries, 2. Call mom, 3. Finish report"

### Completing Tasks
**User**: "I finished the groceries"
**Agent**: Calls `list_tasks()` then `mark_task_complete(task_id=1)`
**Response**: "Great! I've marked 'Buy groceries' as complete."

### Updating Tasks
**User**: "Change the meeting to 3pm"
**Agent**: Calls `list_tasks()` then `update_task(task_id=5, title="Meeting at 3pm")`
**Response**: "Updated! Your meeting task now says 'Meeting at 3pm'."

### Deleting Tasks
**User**: "Remove the old task"
**Agent**: Calls `list_tasks()` then `delete_task(task_id=2)`
**Response**: "Done! I've removed that task from your list."

---

## Agent System Prompt

```python
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural language.

Available tools:
- create_task: Create new tasks
- list_tasks: View tasks (filter by status)
- update_task: Modify task details
- delete_task: Remove tasks
- mark_task_complete: Toggle completion status
- get_task_stats: Get task statistics

Guidelines:
1. Be friendly and conversational
2. Confirm actions after executing them
3. If a task ID is needed, list tasks first to find it
4. Handle errors gracefully with helpful messages
5. Proactively suggest task organization tips
6. Use markdown for formatting responses

Examples:
- User: "Add buy milk" → create_task(title="Buy milk")
- User: "What's pending?" → list_tasks(status="active")
- User: "Done with groceries" → list_tasks() then mark_task_complete()
"""
```

---

## Performance Requirements

- Response time: < 3 seconds (including AI call)
- Database query time: < 100ms
- Tool execution time: < 500ms each
- Support 100 concurrent users
- Handle conversation history up to 100 messages

---

## Security Considerations

### User Isolation
- Always validate `user_id` matches authenticated user
- Filter conversations by user_id
- Pass user_id to all MCP tool calls

### Input Validation
- Sanitize user messages
- Limit message length (max 2000 characters)
- Validate conversation_id belongs to user

### Rate Limiting
- Max 10 requests per minute per user
- Max 100 requests per hour per user
- Prevent abuse of AI API

### API Key Security
- Store OpenAI API key in environment variables
- Never expose in responses
- Rotate keys periodically

---

## Testing Scenarios

### New Conversation
```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### Continue Conversation
```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{"message": "What tasks do I have?", "conversation_id": 123}'
```

### Error Handling
```bash
# Empty message
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

---

## Monitoring & Logging

### Log Events
- Chat request received
- Conversation fetched/created
- Agent invoked
- Tool calls executed
- Response stored
- Error occurred

### Metrics to Track
- Average response time
- Tool call success rate
- Error rate
- Conversations per user
- Messages per conversation

---

## Future Enhancements (Phase IV/V)

- WebSocket support for real-time chat
- Streaming responses (token by token)
- Voice input/output
- Multi-language support
- Conversation export
- Chat analytics

---

**Status**: 📝 Specification Complete
**Next**: Database schema for conversations
