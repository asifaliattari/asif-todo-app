# Phase V - Advanced Features & Cloud Native

**Author**: Asif Ali AstolixGen
**Phase**: V - Enterprise Features + Kafka + Dapr
**Goal**: Add advanced task management features and cloud-native event-driven architecture

---

## Overview

Transform TaskFlow into an enterprise-grade application with advanced features and cloud-native patterns using Kafka for event streaming and Dapr for microservices patterns.

## Objectives

### Part A: Advanced Task Management Features

1. **Priorities & Tags**
   - Assign priority levels (High, Medium, Low)
   - Add multiple tags per task
   - Filter by priority and tags

2. **Search & Filter**
   - Full-text search across task titles and descriptions
   - Filter by status, priority, tags, dates
   - Combine multiple filters

3. **Sort Tasks**
   - Sort by creation date, due date, priority, title
   - Ascending/descending order
   - Save sort preferences

4. **Recurring Tasks**
   - Daily, weekly, monthly patterns
   - Auto-create next occurrence when completed
   - Skip/modify specific occurrences

5. **Due Dates & Reminders**
   - Set due dates for tasks
   - Email/push notifications before due date
   - Overdue task highlighting
   - Snooze reminders

### Part B: Cloud-Native Architecture

1. **Apache Kafka Integration**
   - Event streaming for task operations
   - Topics: task-created, task-updated, task-deleted, task-completed
   - Event-driven microservices architecture
   - Event sourcing pattern

2. **Dapr Integration**
   - Service-to-service invocation
   - Pub/Sub messaging
   - State management
   - Secrets management
   - Observability

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Frontend (Next.js)                  │
│          Priorities│Tags│Search│Filters│Recurring    │
└───────────────┬──────────────────────────────────────┘
                │
                │ REST API + WebSocket
                │
┌───────────────▼──────────────────────────────────────┐
│            API Gateway (FastAPI + Dapr)              │
└───────────┬────────────────────┬──────────────────────┘
            │                    │
    ┌───────▼───────┐    ┌──────▼──────────┐
    │ Task Service  │    │ Notification Svc │
    │   (FastAPI)   │    │    (FastAPI)    │
    │   + Dapr      │    │    + Dapr       │
    └───┬───────┬───┘    └────────┬────────┘
        │       │                  │
        │       │    ┌─────────────▼──────────┐
        │       │    │    Apache Kafka        │
        │       │    │  ┌──────────────────┐  │
        │       │    │  │ task-events      │  │
        │       │    │  │ notifications    │  │
        │       │    │  │ task-completed   │  │
        │       │    │  └──────────────────┘  │
        │       │    └────────────────────────┘
        │       │                  │
        │       └──────────────────┤
        │                          │
   ┌────▼────┐              ┌─────▼─────┐
   │  Neon   │              │   Redis   │
   │PostgreSQL│             │  (Dapr)   │
   └─────────┘              └───────────┘
```

---

## New Database Schema

### Tasks Table (Extended)

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    
    -- NEW FIELDS
    priority VARCHAR(20) DEFAULT 'medium',  -- high, medium, low
    tags TEXT[],  -- Array of tags
    due_date TIMESTAMP WITH TIME ZONE,
    reminder_date TIMESTAMP WITH TIME ZONE,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern JSONB,  -- {type: 'daily'|'weekly'|'monthly', interval: 1}
    parent_task_id UUID REFERENCES tasks(id),  -- For recurring tasks
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes
    INDEX idx_user_priority (user_id, priority),
    INDEX idx_user_tags (user_id, tags),
    INDEX idx_due_date (due_date),
    INDEX idx_tags USING GIN(tags)
);
```

### Task Events Table

```sql
CREATE TABLE task_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL,
    user_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- created, updated, deleted, completed
    event_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_task_events (task_id, created_at)
);
```

---

## API Endpoints (Extended)

### Task Management

```
GET    /api/tasks?priority=high&tags=work&search=meeting
POST   /api/tasks
PUT    /api/tasks/{id}
DELETE /api/tasks/{id}
PATCH  /api/tasks/{id}/complete
PATCH  /api/tasks/{id}/priority
PATCH  /api/tasks/{id}/tags
POST   /api/tasks/{id}/recurrence
```

### Search & Filter

```
GET /api/tasks/search?q=meeting
GET /api/tasks/filter?status=active&priority=high&tags=work,urgent
GET /api/tasks/overdue
GET /api/tasks/due-today
```

### Recurring Tasks

```
POST   /api/tasks/{id}/recurrence
GET    /api/tasks/recurring
DELETE /api/tasks/{id}/recurrence
PATCH  /api/tasks/{id}/occurrence/{date}/skip
```

### Events (Kafka)

```
POST   /api/events/publish
GET    /api/events/stream  # WebSocket
```

---

## Kafka Topics

1. **task-created**: When a task is created
2. **task-updated**: When task details change
3. **task-deleted**: When a task is deleted
4. **task-completed**: When a task is marked complete
5. **task-reminder**: Reminder notifications

---

## Dapr Components

### 1. Pub/Sub (Kafka)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskflow-pubsub
spec:
  type: pubsub.kafka
  metadata:
  - name: brokers
    value: "localhost:9092"
```

### 2. State Store (Redis)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskflow-statestore
spec:
  type: state.redis
  metadata:
  - name: redisHost
    value: "localhost:6379"
```

### 3. Secrets (Local File)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskflow-secrets
spec:
  type: secretstores.local.file
```

---

## Frontend Features

### 1. Priority Selector

```tsx
<PriorityBadge priority="high" />
<PrioritySelect onChange={setPriority} />
```

### 2. Tag Manager

```tsx
<TagInput tags={tags} onChange={setTags} />
<TagFilter availableTags={tags} onFilter={handleFilter} />
```

### 3. Search Bar

```tsx
<SearchBar 
  onSearch={handleSearch}
  filters={['status', 'priority', 'tags', 'date']}
/>
```

### 4. Recurring Task Modal

```tsx
<RecurringTaskForm
  pattern="weekly"
  interval={1}
  endDate={endDate}
/>
```

### 5. Due Date Picker

```tsx
<DatePicker
  value={dueDate}
  onChange={setDueDate}
  enableReminder={true}
/>
```

---

## Success Criteria

### Part A: Features
- [ ] Priority levels work (High/Medium/Low)
- [ ] Tags can be added, removed, filtered
- [ ] Search returns relevant results
- [ ] Multi-filter combinations work
- [ ] Sort by multiple fields
- [ ] Recurring tasks auto-create
- [ ] Due dates display correctly
- [ ] Reminders send notifications

### Part B: Cloud Native
- [ ] Kafka broker running
- [ ] Events published to Kafka
- [ ] Dapr sidecars deployed
- [ ] Pub/sub working
- [ ] State managed via Dapr
- [ ] Observability enabled

---

## Implementation Order

1. Database schema migration
2. Backend API for priorities & tags
3. Frontend UI for priorities & tags
4. Search & filter implementation
5. Recurring tasks logic
6. Due dates & reminders
7. Kafka setup
8. Dapr integration
9. Event-driven architecture
10. Testing & optimization

---

**Next**: See individual feature specs in `phase5/features/` directory
