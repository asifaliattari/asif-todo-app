# Conversations Database Schema

**Component**: Conversations & Messages Tables
**Purpose**: Store chat history for stateless server architecture
**Phase**: III - AI Integration

---

## Overview

To enable stateless server architecture, all conversation state must be persisted in the database. This allows any backend instance to handle any request by fetching conversation history from the database.

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│            users                     │
├─────────────────────────────────────┤
│ id           VARCHAR PRIMARY KEY     │
│ email        VARCHAR UNIQUE NOT NULL │
│ name         VARCHAR NOT NULL        │
│ ...                                  │
└──────────────┬──────────────────────┘
               │
               │ 1:N
               │
┌──────────────▼──────────────────────┐
│         conversations                │
├─────────────────────────────────────┤
│ id           SERIAL PRIMARY KEY      │
│ user_id      VARCHAR FK → users.id   │
│ title        VARCHAR(200)            │ (optional: first message summary)
│ created_at   TIMESTAMP NOT NULL      │
│ updated_at   TIMESTAMP NOT NULL      │
└──────────────┬──────────────────────┘
               │
               │ 1:N
               │
┌──────────────▼──────────────────────┐
│           messages                   │
├─────────────────────────────────────┤
│ id             SERIAL PRIMARY KEY    │
│ conversation_id INT FK → convs.id    │
│ role           VARCHAR(20) NOT NULL  │ ("user" or "assistant")
│ content        TEXT NOT NULL         │
│ tool_calls     JSONB                 │ (nullable, stores tool execution data)
│ created_at     TIMESTAMP NOT NULL    │
└─────────────────────────────────────┘
```

---

## Table: conversations

### Purpose
Track individual chat conversations for each user. Each conversation contains multiple messages.

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL (INT) | PRIMARY KEY | Auto-incrementing conversation ID |
| `user_id` | VARCHAR(255) | FOREIGN KEY → users.id, NOT NULL | Owner of the conversation |
| `title` | VARCHAR(200) | NULLABLE | Optional title (auto-generated from first message) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation start time |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

### Indexes

```sql
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);
```

**Purpose**:
- `idx_conversations_user_id`: Fast filtering by user
- `idx_conversations_updated_at`: Sort conversations by recency

### Constraints

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Cascade Rules
- **ON DELETE CASCADE**: When a user is deleted, all their conversations are automatically deleted

---

## Table: messages

### Purpose
Store individual messages within conversations, including both user messages and assistant responses.

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL (INT) | PRIMARY KEY | Auto-incrementing message ID |
| `conversation_id` | INT | FOREIGN KEY → conversations.id, NOT NULL | Parent conversation |
| `role` | VARCHAR(20) | NOT NULL | Message sender ("user" or "assistant") |
| `content` | TEXT | NOT NULL | Message text content |
| `tool_calls` | JSONB | NULLABLE | Tool execution data (only for assistant messages) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

### Indexes

```sql
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

**Purpose**:
- `idx_messages_conversation_id`: Fast retrieval of conversation history
- `idx_messages_created_at`: Chronological ordering

### Constraints

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Cascade Rules
- **ON DELETE CASCADE**: When a conversation is deleted, all its messages are automatically deleted

---

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Dict, Any

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str  # Message text
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"type_": "JSONB"})
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

### Pydantic Schemas (for API)

```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    tool_calls: Optional[Dict[str, Any]]
    created_at: datetime

class ConversationResponse(BaseModel):
    id: int
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int

class ConversationWithMessages(BaseModel):
    id: int
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
```

---

## Sample Data

### Create Test Conversation

```sql
-- Insert conversation
INSERT INTO conversations (user_id, title, created_at, updated_at)
VALUES (
    'user-123',
    'Task Management Chat',
    NOW(),
    NOW()
)
RETURNING id; -- Returns: conversation_id = 1

-- Insert user message
INSERT INTO messages (conversation_id, role, content, created_at)
VALUES (
    1,
    'user',
    'Add a task to buy groceries',
    NOW()
);

-- Insert assistant message with tool call
INSERT INTO messages (conversation_id, role, content, tool_calls, created_at)
VALUES (
    1,
    'assistant',
    'I''ve added "Buy groceries" to your task list.',
    '{"tool": "create_task", "parameters": {"title": "Buy groceries"}, "result": {"task_id": 456, "status": "created"}}'::jsonb,
    NOW()
);
```

---

## Query Patterns

### Get Conversation History

```sql
SELECT m.id, m.role, m.content, m.tool_calls, m.created_at
FROM messages m
WHERE m.conversation_id = 1
ORDER BY m.created_at ASC;
```

### List User's Conversations

```sql
SELECT
    c.id,
    c.title,
    c.updated_at,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_message_at
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
WHERE c.user_id = 'user-123'
GROUP BY c.id, c.title, c.updated_at
ORDER BY c.updated_at DESC
LIMIT 20;
```

### Create New Conversation

```sql
INSERT INTO conversations (user_id, created_at, updated_at)
VALUES ('user-123', NOW(), NOW())
RETURNING id;
```

### Add Message to Conversation

```sql
INSERT INTO messages (conversation_id, role, content, created_at)
VALUES (1, 'user', 'Show me my tasks', NOW())
RETURNING id;
```

### Update Conversation Timestamp

```sql
UPDATE conversations
SET updated_at = NOW()
WHERE id = 1;
```

### Delete Conversation (with messages)

```sql
-- CASCADE will automatically delete all messages
DELETE FROM conversations WHERE id = 1;
```

---

## tool_calls JSONB Structure

When the assistant calls MCP tools, store the execution data in JSONB format:

### Single Tool Call

```json
{
  "tool": "create_task",
  "parameters": {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  },
  "result": {
    "success": true,
    "task_id": 456,
    "status": "created"
  }
}
```

### Multiple Tool Calls

```json
[
  {
    "tool": "list_tasks",
    "parameters": {"status": "active"},
    "result": {"success": true, "tasks": [...], "count": 3}
  },
  {
    "tool": "mark_task_complete",
    "parameters": {"task_id": 123},
    "result": {"success": true, "task_id": 123, "status": "completed"}
  }
]
```

### Tool Call with Error

```json
{
  "tool": "delete_task",
  "parameters": {"task_id": 999},
  "result": {
    "success": false,
    "error": "Task not found",
    "error_code": "TASK_NOT_FOUND"
  }
}
```

---

## Auto-Generate Conversation Title

Optionally generate a title from the first user message:

```python
def generate_conversation_title(first_message: str) -> str:
    """Generate a short title from the first message"""
    # Truncate to 50 characters
    title = first_message[:50]
    if len(first_message) > 50:
        title += "..."
    return title
```

Example:
- User: "Add a task to buy groceries" → Title: "Add a task to buy groceries"
- User: "I need to remember to call mom tomorrow and also buy milk..." → Title: "I need to remember to call mom tomorrow and also..."

---

## Performance Considerations

### Indexes
- Index on `conversation_id` ensures fast message retrieval
- Index on `user_id` enables fast filtering of user's conversations
- Composite index on `(user_id, updated_at)` for recent conversations query

### Pagination
For conversations with many messages:
```sql
-- Get messages with pagination
SELECT * FROM messages
WHERE conversation_id = 1
ORDER BY created_at ASC
LIMIT 50 OFFSET 0;
```

### Message Limit
Consider limiting conversation length:
- Keep last 100 messages per conversation
- Archive or compress older messages
- Implement message pruning strategy

---

## Data Retention

### Strategy Options

1. **Keep Forever**: Simple, no data loss, may grow large
2. **Archive After 90 Days**: Move old conversations to archive table
3. **Delete After 1 Year**: Automatically clean up old data
4. **User Choice**: Let users decide retention per conversation

### Implementation (Archive Strategy)

```sql
-- Create archive table
CREATE TABLE conversations_archive (
    LIKE conversations INCLUDING ALL
);

-- Move old conversations
INSERT INTO conversations_archive
SELECT * FROM conversations
WHERE updated_at < NOW() - INTERVAL '90 days';

DELETE FROM conversations
WHERE updated_at < NOW() - INTERVAL '90 days';
```

---

## Migration Script

```python
# alembic/versions/xxx_add_conversations.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('title', sa.String(200), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSONB, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')")
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

## Security Considerations

### User Isolation
- Always filter conversations by user_id
- Validate user owns conversation before accessing messages
- Never expose other users' conversation data

### Data Privacy
- Encrypt sensitive message content (optional)
- Implement user data export (GDPR compliance)
- Provide conversation deletion endpoint

### Input Sanitization
- Validate message length (max 2000 chars)
- Sanitize content to prevent XSS
- Validate tool_calls JSON structure

---

## API Endpoints for Conversations

### List User's Conversations

```
GET /api/{user_id}/conversations
```

Response:
```json
{
  "conversations": [
    {
      "id": 1,
      "title": "Task Management Chat",
      "message_count": 12,
      "last_message_at": "2026-02-11T10:30:00Z",
      "created_at": "2026-02-10T09:00:00Z"
    }
  ],
  "total": 5
}
```

### Get Conversation History

```
GET /api/{user_id}/conversations/{conversation_id}
```

Response:
```json
{
  "id": 1,
  "title": "Task Management Chat",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2026-02-11T10:00:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I've added 'Buy groceries' to your task list.",
      "tool_calls": {...},
      "created_at": "2026-02-11T10:00:05Z"
    }
  ]
}
```

### Delete Conversation

```
DELETE /api/{user_id}/conversations/{conversation_id}
```

---

## Future Enhancements (Phase IV/V)

- Conversation search (full-text search on messages)
- Conversation tags/categories
- Shared conversations (team features)
- Export conversation as PDF/Markdown
- Message reactions/feedback
- Conversation templates
- Voice message storage (audio files)

---

**Status**: 📝 Specification Complete
**Next**: OpenAI Agents SDK integration specification
