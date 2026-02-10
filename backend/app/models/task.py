"""
Task model for todo items
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurrenceType(str, Enum):
    """Recurrence pattern types"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Task(SQLModel, table=True):
    """Task/Todo item model with Phase V features"""

    __tablename__ = "tasks"

    # Core fields
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

    # Phase V: Advanced features
    priority: str = Field(default="medium", max_length=20)  # high, medium, low
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    due_date: Optional[datetime] = Field(default=None)
    reminder_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    parent_task_id: Optional[int] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for task creation - Phase V enhanced"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default="medium")
    tags: Optional[List[str]] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    reminder_date: Optional[datetime] = Field(default=None)
    is_recurring: Optional[bool] = Field(default=False)
    recurrence_pattern: Optional[dict] = Field(default=None)


class TaskUpdate(SQLModel):
    """Schema for task update - Phase V enhanced"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[dict] = None


class TaskResponse(SQLModel):
    """Schema for task response - Phase V enhanced"""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: Optional[List[str]]
    due_date: Optional[datetime]
    reminder_date: Optional[datetime]
    is_recurring: bool
    recurrence_pattern: Optional[dict]
    parent_task_id: Optional[int]
    created_at: datetime
    updated_at: datetime
