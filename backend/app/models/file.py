"""
File upload and permission models
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional


class FileUpload(SQLModel, table=True):
    """Uploaded file model"""

    __tablename__ = "file_uploads"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int  # Size in bytes
    file_type: str = Field(max_length=50)  # pdf, doc, docx
    processed_content: Optional[str] = Field(default=None)  # Extracted text
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)


class FilePermission(SQLModel, table=True):
    """File upload permission model"""

    __tablename__ = "file_permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, unique=True)
    granted_by: str = Field(foreign_key="users.id")  # Admin user ID
    can_upload: bool = Field(default=True)
    max_files: int = Field(default=5)  # Max number of files
    max_file_size_mb: int = Field(default=10)  # Max size per file in MB
    granted_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)  # Optional expiry


class PermissionRequest(SQLModel, table=True):
    """Permission request from users"""

    __tablename__ = "permission_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    user_email: str = Field(max_length=255)
    user_name: str = Field(max_length=100)
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending", max_length=20)  # pending, approved, denied
    reviewed_at: Optional[datetime] = Field(default=None)
    reviewed_by: Optional[str] = Field(default=None)  # Admin user ID


# Request/Response Schemas

class FileUploadResponse(SQLModel):
    """Response schema for file upload"""
    id: int
    filename: str
    file_size: int
    file_type: str
    upload_date: datetime
    processed: bool


class FileListResponse(SQLModel):
    """Response schema for file list"""
    files: list[FileUploadResponse]
    total: int


class PermissionGrantRequest(SQLModel):
    """Schema for granting permission"""
    user_email: str
    max_files: int = Field(default=5, ge=1, le=100)
    max_file_size_mb: int = Field(default=10, ge=1, le=100)
    expires_days: Optional[int] = Field(default=None)  # Optional expiry in days


class PermissionResponse(SQLModel):
    """Response schema for permission"""
    user_id: str
    user_email: str
    can_upload: bool
    max_files: int
    max_file_size_mb: int
    granted_at: datetime
    expires_at: Optional[datetime]


class PermissionRequestResponse(SQLModel):
    """Response schema for permission request"""
    id: int
    user_email: str
    user_name: str
    requested_at: datetime
    status: str
