"""
Task CRUD endpoints - Phase V Enhanced
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from datetime import datetime

from app.database import get_session
from app.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from app.auth import get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", response_model=dict)
def get_tasks(
    # Phase II filters
    completed: Optional[bool] = None,

    # Phase V filters
    priority: Optional[str] = None,
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    overdue_only: Optional[bool] = False,

    # Sorting
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="asc or desc"),

    # Pagination
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),

    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get all tasks for the authenticated user with advanced filtering

    **Query parameters:**
    - completed: Filter by completion status
    - priority: Filter by priority (high, medium, low)
    - tags: Comma-separated tags to filter by
    - search: Search in title and description
    - due_before: Tasks due before this date
    - due_after: Tasks due after this date
    - overdue_only: Show only overdue tasks
    - sort_by: Field to sort by (created_at, due_date, priority, title)
    - sort_order: Sort order (asc or desc)
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return
    """
    # Build base query
    statement = select(Task).where(Task.user_id == user_id)

    # Apply filters
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    if priority:
        statement = statement.where(Task.priority == priority.lower())

    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        # Filter tasks that have any of the specified tags
        for tag in tag_list:
            statement = statement.where(Task.tags.contains([tag]))

    if search:
        search_term = f"%{search}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    if due_before:
        statement = statement.where(Task.due_date <= due_before)

    if due_after:
        statement = statement.where(Task.due_date >= due_after)

    if overdue_only:
        now = datetime.utcnow()
        statement = statement.where(
            Task.due_date < now,
            Task.completed == False
        )

    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order.lower() == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    # Count total (before pagination)
    total_statement = select(Task).where(Task.user_id == user_id)
    total = len(session.exec(total_statement).all())

    # Apply pagination
    statement = statement.offset(skip).limit(limit)

    # Execute query
    tasks = session.exec(statement).all()

    return {
        "tasks": [TaskResponse.model_validate(task) for task in tasks],
        "total": total,
        "count": len(tasks),
        "skip": skip,
        "limit": limit
    }


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Create a new task for the authenticated user (Phase V enhanced)

    **Supports**:
    - Priority levels (high, medium, low)
    - Tags (array of strings)
    - Due dates
    - Reminder dates
    - Recurring patterns
    """
    task = Task(
        user_id=user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        completed=False,
        # Phase V fields
        priority=task_data.priority or "medium",
        tags=task_data.tags or [],
        due_date=task_data.due_date,
        reminder_date=task_data.reminder_date,
        is_recurring=task_data.is_recurring or False,
        recurrence_pattern=task_data.recurrence_pattern
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific task by ID

    Verifies task belongs to authenticated user
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Update an existing task

    Only provided fields are updated
    Verifies task belongs to authenticated user
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    # Update fields
    if task_data.title is not None:
        task.title = task_data.title.strip()
    if task_data.description is not None:
        task.description = task_data.description.strip()
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Toggle task completion status

    Verifies task belongs to authenticated user
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    # Toggle completion
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Delete a task permanently

    Verifies task belongs to authenticated user
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return None
