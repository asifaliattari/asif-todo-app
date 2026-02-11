# OpenAI Agents SDK Integration Specification

**Component**: OpenAI Agents SDK Integration
**Purpose**: Natural language understanding and MCP tool orchestration
**Phase**: III - AI Integration

---

## Overview

Use OpenAI's Agents SDK (via Chat Completions API with function calling) to power the conversational interface. The agent understands natural language, decides which MCP tools to call, and generates human-friendly responses.

## Why OpenAI Agents SDK?

**Hackathon Requirement**: Phase III specifically requires "OpenAI Agents SDK" for AI logic.

**Capabilities**:
- Natural language understanding
- Function/tool calling
- Multi-turn conversations
- Context management
- Streaming responses

---

## Architecture

```
User Message
    ↓
Chat Endpoint
    ↓
Fetch Conversation History from DB
    ↓
Build Messages Array
    ↓
OpenAI Agents SDK (GPT-4)
    ↓
Decide which MCP tools to call
    ↓
Execute MCP Tools
    ↓
Generate Response
    ↓
Store in Database
    ↓
Return to User
```

---

## OpenAI Setup

### Install SDK

```bash
cd backend
uv add openai
```

Or via pip:
```bash
pip install openai
```

### Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-...your-api-key
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-4, gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
```

---

## Implementation

### 1. Initialize OpenAI Client

```python
# backend/app/ai/openai_client.py
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
```

### 2. Define System Prompt

```python
# backend/app/ai/prompts.py

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural language.

You have access to the following tools:
- create_task: Create a new task with a title and optional description
- list_tasks: View tasks (optionally filter by status: active, completed, or all)
- update_task: Modify an existing task's title or description
- delete_task: Remove a task permanently
- mark_task_complete: Toggle a task's completion status
- get_task_stats: Get summary statistics about tasks

Guidelines:
1. Be friendly, conversational, and helpful
2. Always confirm actions after executing them
3. If you need a task ID (for update/delete/complete), use list_tasks first to find it
4. Handle errors gracefully with clear explanations
5. Suggest task organization tips when appropriate
6. Use markdown formatting for better readability
7. Be proactive - if the user's task list is messy, offer to help organize it

Examples:
- User: "Add buy milk" → Call create_task(title="Buy milk")
- User: "What's pending?" → Call list_tasks(status="active")
- User: "I finished the groceries" → Call list_tasks() to find it, then mark_task_complete()
- User: "Change meeting to 3pm" → Call list_tasks() to find it, then update_task()

Remember: You're not just a command executor, you're a helpful assistant!
"""
```

### 3. Convert MCP Tools to OpenAI Format

```python
# backend/app/ai/tools.py
from backend.mcp.tools import TOOL_DEFINITIONS

def get_openai_tools():
    """Convert MCP tool definitions to OpenAI function calling format"""
    openai_tools = []

    for mcp_tool in TOOL_DEFINITIONS:
        openai_tool = {
            "type": "function",
            "function": {
                "name": mcp_tool["name"],
                "description": mcp_tool["description"],
                "parameters": mcp_tool["input_schema"]
            }
        }
        openai_tools.append(openai_tool)

    return openai_tools

# Example output:
# [
#     {
#         "type": "function",
#         "function": {
#             "name": "create_task",
#             "description": "Create a new task. Use this when the user wants to add a task.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "title": {"type": "string", "description": "The title of the task"},
#                     "description": {"type": "string", "description": "Optional description"}
#                 },
#                 "required": ["title"]
#             }
#         }
#     }
# ]
```

### 4. Agent Execution Logic

```python
# backend/app/ai/agent.py
from openai import AsyncOpenAI
from backend.mcp.tools import TaskTools
from backend.app.ai.tools import get_openai_tools
from backend.app.ai.prompts import SYSTEM_PROMPT
import json

client = AsyncOpenAI()

async def run_agent(
    messages: list[dict],
    user_id: str,
    user_token: str
) -> tuple[str, list[dict]]:
    """
    Run OpenAI agent with MCP tools

    Args:
        messages: Conversation history (list of {"role": "user/assistant", "content": "..."})
        user_id: User ID for tool execution
        user_token: JWT token for backend API calls

    Returns:
        (response_text, tool_calls_list)
    """

    # Initialize MCP tools
    tools_handler = TaskTools()

    # Get OpenAI-formatted tools
    tools = get_openai_tools()

    # Add system message
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    # Call OpenAI API
    response = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=full_messages,
        tools=tools,
        tool_choice="auto",  # Let model decide when to call tools
        temperature=0.7,
        max_tokens=1000
    )

    assistant_message = response.choices[0].message
    tool_calls = assistant_message.tool_calls or []

    # Execute tool calls if any
    tool_results = []
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # Add user token for authentication
            tool_args["user_token"] = user_token

            # Execute tool via MCP
            result = await execute_mcp_tool(tools_handler, tool_name, tool_args)

            tool_results.append({
                "tool": tool_name,
                "parameters": tool_args,
                "result": result
            })

        # If tools were called, make a second API call to get final response
        # Add tool results to conversation
        full_messages.append({
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                }
                for tc in tool_calls
            ]
        })

        # Add tool results
        for i, tool_call in enumerate(tool_calls):
            full_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_results[i]["result"])
            })

        # Get final response
        final_response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1000
        )

        response_text = final_response.choices[0].message.content
    else:
        # No tools called, just return the response
        response_text = assistant_message.content
        tool_results = []

    return response_text, tool_results


async def execute_mcp_tool(tools_handler: TaskTools, tool_name: str, args: dict):
    """Execute MCP tool and return result"""
    try:
        if tool_name == "create_task":
            return await tools_handler.create_task(**args)
        elif tool_name == "list_tasks":
            return await tools_handler.list_tasks(**args)
        elif tool_name == "update_task":
            return await tools_handler.update_task(**args)
        elif tool_name == "delete_task":
            return await tools_handler.delete_task(**args)
        elif tool_name == "mark_task_complete":
            return await tools_handler.mark_task_complete(**args)
        elif tool_name == "get_task_stats":
            return await tools_handler.get_task_stats(**args)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 5. Integrate with Chat Endpoint

```python
# backend/app/routers/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.app.database import get_session
from backend.app.auth import get_current_user_id
from backend.app.models.conversation import Conversation, Message
from backend.app.ai.agent import run_agent
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]
    timestamp: datetime

@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
    user_token: str = Depends(get_current_user_token)  # New dependency for JWT token
):
    # Validate user
    if user_id != current_user_id:
        raise HTTPException(403, "Not authorized")

    # Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(404, "Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Fetch message history
    messages_db = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()

    # Convert to OpenAI format
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in messages_db
    ]

    # Add new user message
    messages.append({"role": "user", "content": request.message})

    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()

    # Run OpenAI agent
    response_text, tool_calls = await run_agent(
        messages=messages,
        user_id=user_id,
        user_token=user_token
    )

    # Store assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text,
        tool_calls=tool_calls if tool_calls else None
    )
    session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=tool_calls,
        timestamp=datetime.utcnow()
    )
```

---

## Example Conversation Flow

### User: "Add a task to buy groceries"

**Step 1**: OpenAI receives:
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful task management assistant..."},
    {"role": "user", "content": "Add a task to buy groceries"}
  ],
  "tools": [...]
}
```

**Step 2**: OpenAI response:
```json
{
  "message": {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "create_task",
          "arguments": "{\"title\": \"Buy groceries\"}"
        }
      }
    ]
  }
}
```

**Step 3**: Execute tool:
```python
result = await tools_handler.create_task(
    title="Buy groceries",
    user_token="..."
)
# Returns: {"success": True, "task": {"id": 456, "title": "Buy groceries", ...}}
```

**Step 4**: Send tool result back to OpenAI:
```json
{
  "messages": [
    ...previous messages...,
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [...]
    },
    {
      "role": "tool",
      "tool_call_id": "call_abc123",
      "content": "{\"success\": true, \"task\": {\"id\": 456, ...}}"
    }
  ]
}
```

**Step 5**: OpenAI final response:
```json
{
  "message": {
    "role": "assistant",
    "content": "I've added 'Buy groceries' to your task list! You now have a new task to work on."
  }
}
```

---

## Streaming Responses (Optional Enhancement)

For better UX, stream responses token by token:

```python
async def run_agent_streaming(messages: list, user_id: str, user_token: str):
    """Stream OpenAI responses for real-time feel"""
    tools = get_openai_tools()
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    stream = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=full_messages,
        tools=tools,
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

---

## Error Handling

### OpenAI API Errors

```python
from openai import OpenAIError, RateLimitError, APIError

try:
    response = await client.chat.completions.create(...)
except RateLimitError:
    raise HTTPException(429, "AI service is busy. Please try again.")
except APIError as e:
    raise HTTPException(500, f"AI service error: {str(e)}")
except Exception as e:
    raise HTTPException(500, "Unexpected error occurred")
```

### Tool Execution Errors

```python
# In agent.py
try:
    result = await execute_mcp_tool(...)
except Exception as e:
    result = {
        "success": False,
        "error": str(e),
        "error_code": "TOOL_EXECUTION_ERROR"
    }
```

---

## Cost Management

### Token Usage Tracking

```python
response = await client.chat.completions.create(...)

# Log usage
usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Store in database for billing
await log_api_usage(
    user_id=user_id,
    model="gpt-4-turbo-preview",
    prompt_tokens=usage.prompt_tokens,
    completion_tokens=usage.completion_tokens
)
```

### Cost Optimization

1. **Use GPT-3.5-Turbo for testing** (cheaper)
2. **Limit max_tokens** to reasonable values
3. **Implement caching** for common queries
4. **Rate limiting** per user
5. **Truncate long conversation history** (keep last 20 messages)

### Estimated Costs (GPT-4-Turbo)

- Input: $0.01 / 1K tokens
- Output: $0.03 / 1K tokens
- Average chat: 500 tokens = ~$0.02 per message

**Budget for testing**: $50 = ~2,500 chat messages

---

## Testing

### Unit Tests

```python
# tests/test_agent.py
import pytest
from backend.app.ai.agent import run_agent

@pytest.mark.asyncio
async def test_create_task():
    messages = [{"role": "user", "content": "Add buy milk"}]
    response, tools = await run_agent(messages, "test-user", "test-token")

    assert len(tools) == 1
    assert tools[0]["tool"] == "create_task"
    assert "milk" in tools[0]["parameters"]["title"].lower()
    assert "added" in response.lower()
```

### Integration Tests

Test full chat flow with mock OpenAI:

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_chat_endpoint(client, mock_openai):
    response = await client.post(
        "/api/user123/chat",
        json={"message": "Add task to buy groceries"},
        headers={"Authorization": "Bearer token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["response"]
    assert data["conversation_id"]
```

---

## Deployment Considerations

### Environment Variables

```bash
# Production .env
OPENAI_API_KEY=sk-prod-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Hugging Face Spaces
HF_TOKEN=hf_...
```

### Performance

- OpenAI API latency: ~1-3 seconds
- Add loading states in frontend
- Consider request timeout (30 seconds)
- Implement retry logic for transient errors

---

## Alternative: Claude via Anthropic SDK

If switching to Claude (per hackathon doc which mentions both):

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = await client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=get_openai_tools(),  # Same format!
    messages=messages
)
```

**Note**: Tool calling format is similar between OpenAI and Anthropic.

---

## Future Enhancements

- Multi-model support (GPT-4, Claude, Llama)
- Conversation memory optimization
- Custom fine-tuned models
- Retrieval-Augmented Generation (RAG) for task search
- Voice-to-text integration
- Multi-language support

---

**Status**: 📝 Specification Complete
**Next**: Begin implementation with OpenAI SDK setup
