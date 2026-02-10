# MCP Server Specification

**Component**: MCP (Model Context Protocol) Server
**Purpose**: Expose task operations as tools for Claude AI
**Phase**: III - AI Integration

---

## Overview

The MCP server acts as a bridge between Claude AI and the TaskFlow backend, exposing task management operations as callable tools that the AI can use in response to user requests.

## Architecture

```
Claude AI ← MCP Protocol → MCP Server → FastAPI Backend → Database
```

## MCP Server Location

```
backend/
└── mcp/
    ├── __init__.py
    ├── server.py          # Main MCP server
    ├── tools.py           # Tool definitions
    ├── handlers.py        # Tool handlers
    └── config.py          # Configuration
```

## Tools to Implement

### Tool 1: create_task
**Purpose**: Create a new task from natural language

**Input Schema**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "string (optional: low|medium|high)"
}
```

**Example Usage**:
- User: "Add a task to buy groceries"
- AI calls: `create_task(title="Buy groceries")`

**Response**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "title": "Buy groceries",
    "completed": false,
    "created_at": "timestamp"
  }
}
```

---

### Tool 2: list_tasks
**Purpose**: Retrieve user's tasks with optional filters

**Input Schema**:
```json
{
  "status": "string (optional: all|active|completed)",
  "limit": "integer (optional, default: 50)"
}
```

**Example Usage**:
- User: "What tasks do I have?"
- AI calls: `list_tasks(status="active")`

**Response**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": "uuid",
      "title": "Buy groceries",
      "description": "",
      "completed": false,
      "created_at": "timestamp"
    }
  ],
  "count": 1
}
```

---

### Tool 3: update_task
**Purpose**: Update an existing task

**Input Schema**:
```json
{
  "task_id": "string (required)",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Example Usage**:
- User: "Change the groceries task to buy milk"
- AI calls: `update_task(task_id="123", title="Buy milk")`

**Response**:
```json
{
  "success": true,
  "task": {
    "id": "123",
    "title": "Buy milk",
    "updated_at": "timestamp"
  }
}
```

---

### Tool 4: delete_task
**Purpose**: Delete a task

**Input Schema**:
```json
{
  "task_id": "string (required)"
}
```

**Example Usage**:
- User: "Remove the meeting task"
- AI calls: `delete_task(task_id="456")`

**Response**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

---

### Tool 5: mark_task_complete
**Purpose**: Toggle task completion status

**Input Schema**:
```json
{
  "task_id": "string (required)",
  "completed": "boolean (default: true)"
}
```

**Example Usage**:
- User: "I finished the report"
- AI calls: `mark_task_complete(task_id="789")`

**Response**:
```json
{
  "success": true,
  "task": {
    "id": "789",
    "title": "Write report",
    "completed": true
  }
}
```

---

### Tool 6: get_task_stats
**Purpose**: Get summary statistics about user's tasks

**Input Schema**:
```json
{}
```

**Example Usage**:
- User: "How am I doing with my tasks?"
- AI calls: `get_task_stats()`

**Response**:
```json
{
  "success": true,
  "stats": {
    "total": 10,
    "active": 6,
    "completed": 4,
    "completion_rate": 40,
    "created_today": 2
  }
}
```

---

## Authentication & Security

### User Context
- MCP server must know which user is making requests
- Pass user_id from chat session
- Validate JWT token for each request

### Permission Checks
- Users can only access their own tasks
- MCP tools enforce user isolation
- No admin/cross-user operations

### API Security
- MCP server calls backend API with authentication
- Use service account or user token
- Secure communication (HTTPS)

---

## Implementation Details

### MCP Server Setup

```python
# backend/mcp/server.py
from mcp import MCPServer
from mcp.types import Tool, TextContent

server = MCPServer("taskflow-mcp")

@server.tool()
async def create_task(title: str, description: str = "", user_id: str = None):
    """Create a new task"""
    # Call backend API to create task
    # Return formatted response
    pass

@server.tool()
async def list_tasks(status: str = "all", user_id: str = None):
    """List user's tasks"""
    # Call backend API to fetch tasks
    # Return formatted response
    pass

# ... more tools

if __name__ == "__main__":
    server.run()
```

### Backend API Integration

```python
# backend/mcp/handlers.py
import httpx

async def call_backend_api(endpoint: str, method: str, data: dict, user_id: str):
    """Call TaskFlow backend API"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {get_user_token(user_id)}"}
        response = await client.request(
            method=method,
            url=f"http://localhost:8000{endpoint}",
            json=data,
            headers=headers
        )
        return response.json()
```

---

## Configuration

### Environment Variables
```bash
# MCP Server
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3000
MCP_LOG_LEVEL=info

# Backend API
BACKEND_API_URL=http://localhost:8000
BACKEND_API_KEY=your-api-key

# Claude AI
ANTHROPIC_API_KEY=your-anthropic-key
```

---

## Deployment

### Local Development
```bash
cd backend/mcp
python server.py
```

### Production
- Deploy alongside backend API
- Use same hosting (Hugging Face or Railway)
- Or separate service (dedicated MCP host)

### Port Configuration
- MCP Server: Port 3000 (or 5000)
- Backend API: Port 8000
- Frontend: Port 3000 (dev), Vercel (prod)

---

## Error Handling

### Tool Errors
```json
{
  "success": false,
  "error": "Task not found",
  "error_code": "TASK_NOT_FOUND"
}
```

### Common Errors
- `TASK_NOT_FOUND`: Task ID doesn't exist
- `UNAUTHORIZED`: Invalid user or token
- `VALIDATION_ERROR`: Invalid input parameters
- `BACKEND_ERROR`: Backend API failure

---

## Testing

### Unit Tests
Test each tool independently:
- Tool input validation
- Backend API calls
- Response formatting
- Error handling

### Integration Tests
Test with Claude AI:
- Send natural language requests
- Verify correct tool is called
- Check responses are accurate
- Test error scenarios

### Test Data
Create test user with sample tasks:
```python
test_user_id = "test-user-123"
test_tasks = [
    {"id": "1", "title": "Buy groceries", "completed": False},
    {"id": "2", "title": "Write report", "completed": True},
]
```

---

## Monitoring

### Logs
- Log all tool calls
- Log user_id and parameters
- Log response times
- Log errors and failures

### Metrics
- Tools calls per minute
- Average response time
- Error rate
- Popular tools

---

## Future Enhancements

### Phase IV Additions
- `search_tasks(query)` - Full-text search
- `set_task_priority(task_id, priority)` - Priority management
- `add_task_tag(task_id, tag)` - Tagging system

### Phase V Additions
- `create_recurring_task()` - Recurring tasks
- `set_reminder()` - Reminders
- `get_analytics()` - Advanced analytics

---

## References

- MCP Spec: https://modelcontextprotocol.io/spec
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Tool Definition Best Practices: MCP docs

---

**Status**: 📝 Specification Complete
**Next**: Implementation
