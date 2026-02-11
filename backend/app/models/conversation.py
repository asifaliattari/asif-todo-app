"""
Conversation and Message models for AI chatbot
Phase III: AI Integration
"""

from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import JSON, TEXT
from datetime import datetime
from typing import Optional, List, Dict, Any


class Conversation(SQLModel, table=True):
    """Conversation model - holds chat sessions"""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)


class Message(SQLModel, table=True):
    """Message model - individual chat messages"""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(sa_column=Column(TEXT))  # Message text
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))  # Tool execution data
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


# Pydantic schemas for API

class ChatRequest(SQLModel):
    """Schema for chat request"""
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: Optional[int] = None


class ChatResponse(SQLModel):
    """Schema for chat response"""
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]] = []
    timestamp: datetime


class MessageResponse(SQLModel):
    """Schema for message response"""
    id: int
    role: str
    content: str
    tool_calls: Optional[Dict[str, Any]]
    created_at: datetime


class ConversationResponse(SQLModel):
    """Schema for conversation response"""
    id: int
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int


class ConversationWithMessages(SQLModel):
    """Schema for conversation with full message history"""
    id: int
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
