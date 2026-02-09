# Database Schema Specification

**Author**: Asif Ali AstolixGen
**Phase**: Phase II
**Database**: Neon Serverless PostgreSQL

## Overview

The database consists of two main tables: `users` and `tasks`. Each user can have multiple tasks, establishing a one-to-many relationship.

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│            users                     │
├─────────────────────────────────────┤
│ id           VARCHAR PRIMARY KEY     │
│ email        VARCHAR UNIQUE NOT NULL │
│ name         VARCHAR NOT NULL        │
│ hashed_password VARCHAR NOT NULL     │
│ created_at   TIMESTAMP NOT NULL      │
│ updated_at   TIMESTAMP NOT NULL      │
└──────────────┬──────────────────────┘
               │
               │ 1:N
               │
┌──────────────▼──────────────────────┐
│            tasks                     │
├─────────────────────────────────────┤
│ id           SERIAL PRIMARY KEY      │
│ user_id      VARCHAR FK → users.id   │
│ title        VARCHAR(200) NOT NULL   │
│ description  TEXT                    │
│ completed    BOOLEAN DEFAULT FALSE   │
│ created_at   TIMESTAMP NOT NULL      │
│ updated_at   TIMESTAMP NOT NULL      │
└─────────────────────────────────────┘
```

## Table: users

### Purpose
Store user account information for authentication and authorization.

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | VARCHAR(255) | PRIMARY KEY | Unique user identifier (UUID) |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (login credential) |
| `name` | VARCHAR(100) | NOT NULL | User's full name |
| `hashed_password` | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes

```sql
CREATE INDEX idx_users_email ON users(email);
```

**Purpose**: Fast lookup during login (email is used frequently for authentication)

### Constraints

```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Security Notes
- Password is **never** stored in plaintext
- Use bcrypt hash with salt rounds = 10
- Email is stored in lowercase for case-insensitive comparison

## Table: tasks

### Purpose
Store todo tasks for each user.

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL (INT) | PRIMARY KEY | Auto-incrementing task ID |
| `user_id` | VARCHAR(255) | FOREIGN KEY → users.id, NOT NULL | Owner of the task |
| `title` | VARCHAR(200) | NOT NULL | Task title |
| `description` | TEXT | NULLABLE | Optional task description (max 1000 chars in app) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes

```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

**Purpose**:
- `idx_tasks_user_id`: Fast filtering by user (main query pattern)
- `idx_tasks_user_completed`: Fast filtering by user + completion status

### Constraints

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Cascade Rules
- **ON DELETE CASCADE**: When a user is deleted, all their tasks are automatically deleted
- **ON UPDATE CASCADE**: If user_id changes (unlikely), tasks update automatically

## SQLModel Definitions

### User Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Database Connection

### Connection String Format

```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require
```

### Neon Connection String Example

```
postgresql://user:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Environment Variable

Store in `.env` file:
```
DATABASE_URL=postgresql://user:pass@host/database?sslmode=require
```

## Migration Strategy

### Initial Setup (Phase II)

Use SQLModel's `create_all()` for automatic table creation:

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

### Future (Phase III+)

Use Alembic for database migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Sample Data (for testing)

```sql
-- Insert test user
INSERT INTO users (id, email, name, hashed_password, created_at, updated_at)
VALUES (
    'test_user_123',
    'asif@example.com',
    'Asif Ali AstolixGen',
    '$2b$10$hashed_password_here',
    NOW(),
    NOW()
);

-- Insert test tasks
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES
    ('test_user_123', 'Complete Phase II', 'Implement full-stack web app', false, NOW(), NOW()),
    ('test_user_123', 'Deploy to Vercel', 'Deploy frontend', true, NOW(), NOW()),
    ('test_user_123', 'Set up Neon DB', 'Configure database', true, NOW(), NOW());
```

## Query Patterns

### Get all tasks for a user
```sql
SELECT * FROM tasks
WHERE user_id = 'user_123'
ORDER BY created_at DESC;
```

### Get incomplete tasks
```sql
SELECT * FROM tasks
WHERE user_id = 'user_123' AND completed = false
ORDER BY created_at DESC;
```

### Create task
```sql
INSERT INTO tasks (user_id, title, description, completed)
VALUES ('user_123', 'New task', 'Description', false)
RETURNING *;
```

### Update task
```sql
UPDATE tasks
SET title = 'Updated title',
    description = 'Updated description',
    updated_at = NOW()
WHERE id = 1 AND user_id = 'user_123'
RETURNING *;
```

### Toggle completion
```sql
UPDATE tasks
SET completed = NOT completed,
    updated_at = NOW()
WHERE id = 1 AND user_id = 'user_123'
RETURNING *;
```

### Delete task
```sql
DELETE FROM tasks
WHERE id = 1 AND user_id = 'user_123';
```

## Performance Considerations

### Indexes
- Index on `user_id` ensures fast filtering (most common query)
- Composite index on `(user_id, completed)` optimizes filtered views
- Index on `email` speeds up login lookups

### Connection Pooling
- Neon handles connection pooling automatically
- Set max connections in SQLModel engine (default: 20)

### Query Optimization
- Always filter by `user_id` first (indexed)
- Use `ORDER BY` with indexed columns when possible
- Limit query results for large datasets

## Data Integrity

### User Deletion
- When user is deleted, all tasks automatically deleted (CASCADE)
- Consider soft delete in future (add `deleted_at` column)

### Concurrent Updates
- Use database transactions for complex operations
- `updated_at` timestamp helps track changes

### Validation
- Database enforces NOT NULL constraints
- App layer validates max lengths (title: 200, description: 1000)
- App layer validates email format

## Backup & Recovery

### Neon Features
- Automatic backups (Neon handles this)
- Point-in-time recovery
- High availability

### Best Practices
- Regularly export data for local backups
- Test restore procedures
- Monitor database size

## Future Schema Changes (Phase III+)

Planned additions for future phases:

### Phase III (AI Chatbot)
```sql
-- Conversation history
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Phase V (Advanced Features)
```sql
-- Add to tasks table
ALTER TABLE tasks
ADD COLUMN priority VARCHAR(20) DEFAULT 'medium',
ADD COLUMN tags TEXT[],
ADD COLUMN due_date TIMESTAMP,
ADD COLUMN recurring_pattern VARCHAR(20);
```

## Summary

This schema provides:
- ✅ User authentication support
- ✅ Task ownership and isolation
- ✅ Efficient querying with indexes
- ✅ Data integrity with foreign keys
- ✅ Automatic timestamps
- ✅ Scalable design for future features
