# Feature: Task CRUD Operations

**Author**: Asif Ali AstolixGen
**Phase**: Phase II
**Priority**: High (Required for Basic Level)

## Overview

Users must be able to create, read, update, and delete their tasks. Each user can only access their own tasks.

## User Stories

### US-1: Create Task
**As a logged-in user**, I want to create a new task so that I can track things I need to do.

**Acceptance Criteria**:
- User can enter task title (required, 1-200 characters)
- User can enter task description (optional, max 1000 characters)
- Task is automatically associated with logged-in user
- Task is created with `completed = false` by default
- Success message is shown after creation
- New task appears at top of task list

### US-2: View Task List
**As a logged-in user**, I want to view all my tasks so that I can see what I need to do.

**Acceptance Criteria**:
- User sees only their own tasks (not other users' tasks)
- Tasks are displayed in a list format
- Each task shows:
  - Title
  - Description (if provided)
  - Completion status (✓ or ○)
  - Created date
- Empty state message if no tasks exist
- List is automatically refreshed after any change

### US-3: Update Task
**As a logged-in user**, I want to update task details so that I can correct mistakes or add information.

**Acceptance Criteria**:
- User can click to edit a task
- User can modify title
- User can modify description
- User cannot change task owner
- Changes are saved to database
- Updated task is reflected immediately in UI
- User can cancel edit without saving

### US-4: Mark Task Complete/Incomplete
**As a logged-in user**, I want to mark tasks as complete/incomplete so that I can track my progress.

**Acceptance Criteria**:
- User can click checkbox to toggle completion status
- Visual indicator changes (✓ vs ○)
- Completed tasks may have strikethrough text
- Status is saved immediately to database
- No page reload required

### US-5: Delete Task
**As a logged-in user**, I want to delete tasks so that I can remove tasks I no longer need.

**Acceptance Criteria**:
- User can click delete button on any task
- Confirmation dialog appears ("Are you sure?")
- Task is permanently removed from database
- Task disappears from UI immediately
- User can cancel deletion

## API Requirements

See `@specs/api/rest-endpoints.md` for detailed endpoint specifications.

**Required Endpoints**:
- `GET /api/tasks` - List all tasks for current user
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

## Database Requirements

See `@specs/database/schema.md` for schema details.

**Task Model Fields**:
- `id`: Integer, primary key, auto-increment
- `user_id`: String, foreign key to users table
- `title`: String, not null, max 200 chars
- `description`: Text, nullable, max 1000 chars
- `completed`: Boolean, default false
- `created_at`: Timestamp, auto-set on creation
- `updated_at`: Timestamp, auto-update on modification

## UI Requirements

See `@specs/ui/pages.md` and `@specs/ui/components.md` for UI details.

**Required Components**:
- Task Form (for create/edit)
- Task List (displays all tasks)
- Task Item (single task display)
- Delete Confirmation Dialog

## Business Rules

### BR-1: User Isolation
- Users can only see, edit, and delete their own tasks
- API must verify ownership before any operation
- Attempting to access another user's task returns 403 Forbidden

### BR-2: Title Validation
- Title is required (cannot be empty)
- Title must be 1-200 characters
- Leading/trailing whitespace is trimmed

### BR-3: Description Validation
- Description is optional
- If provided, max 1000 characters
- Can be empty string or null

### BR-4: Completion Toggle
- Any task can be marked complete/incomplete
- Multiple toggles allowed (can change back and forth)
- Completion status has no effect on other operations

### BR-5: Soft Delete Option (Future)
- Current implementation: Hard delete (permanent)
- Future: Consider soft delete (mark as deleted, keep in DB)

## Error Handling

### Frontend Errors
- Empty title: "Title is required"
- Title too long: "Title must be 200 characters or less"
- Description too long: "Description must be 1000 characters or less"
- Network error: "Failed to save. Please try again."
- Unauthorized: Redirect to login

### Backend Errors
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing or invalid JWT token
- 403 Forbidden: Attempting to access another user's task
- 404 Not Found: Task ID doesn't exist
- 500 Internal Server Error: Database or server error

## Testing Scenarios

### Happy Path
1. Create task with valid title → Success
2. View task list → Shows new task
3. Update task title → Task updated
4. Mark task complete → Checkbox checked
5. Delete task → Task removed

### Edge Cases
1. Create task with max-length title (200 chars) → Success
2. Create task with max-length description (1000 chars) → Success
3. Create task with only title (no description) → Success
4. Update task to empty description → Success
5. Toggle completion multiple times → Each toggle persists

### Error Cases
1. Create task with empty title → Error: "Title is required"
2. Create task with 201-char title → Error: "Title too long"
3. Update another user's task → Error: 403 Forbidden
4. Delete non-existent task → Error: 404 Not Found

## Performance Requirements

- Task list loads in < 2 seconds
- Create/Update/Delete operations complete in < 1 second
- UI updates without page reload (SPA behavior)
- Database queries use indexes for fast filtering by user_id

## Security Requirements

- All API calls require valid JWT token
- Backend verifies task ownership before any operation
- SQL injection prevented by using ORM (SQLModel)
- Input sanitization on both frontend and backend

## Dependencies

- Authentication system must be implemented first
- Database schema must exist
- Frontend must have JWT token management

## Future Enhancements (Not Phase II)

- Undo delete
- Bulk operations (delete multiple, mark multiple complete)
- Task search and filtering
- Task sorting
- Task categories/tags
- Due dates
- Priority levels

## Acceptance Testing

**Definition of Done**:
- [ ] All 5 user stories implemented
- [ ] All API endpoints working
- [ ] Database schema created
- [ ] UI components functional
- [ ] Error handling implemented
- [ ] User isolation verified
- [ ] Demo video shows all CRUD operations
