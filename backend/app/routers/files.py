"""
File upload and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user_id
from app.models.user import User
from app.models.file import (
    FileUpload,
    FilePermission,
    PermissionRequest,
    FileUploadResponse,
    FileListResponse,
    PermissionGrantRequest,
    PermissionResponse,
    PermissionRequestResponse,
)
from app.file_utils import (
    validate_file_type,
    get_file_extension,
    extract_text_from_file,
)
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/files", tags=["Files"])

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_EMAIL = "asif.alimusharaf@gmail.com"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes


def get_user_permission(user_id: str, session: Session) -> Optional[FilePermission]:
    """Get user's file upload permission"""
    statement = select(FilePermission).where(FilePermission.user_id == user_id)
    return session.exec(statement).first()


def is_admin(user_id: str, session: Session) -> bool:
    """Check if user is admin"""
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user and user.role == "admin"


def get_user_file_count(user_id: str, session: Session) -> int:
    """Get number of files uploaded by user"""
    statement = select(FileUpload).where(FileUpload.user_id == user_id)
    files = session.exec(statement).all()
    return len(files)


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Upload a file (PDF, DOC, DOCX)

    Admin users have unlimited access.
    Regular users need permission.
    """
    # Check if admin
    admin = is_admin(user_id, session)

    if not admin:
        # Check permission
        permission = get_user_permission(user_id, session)

        if not permission or not permission.can_upload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to upload files. Please request permission from admin."
            )

        # Check expiry
        if permission.expires_at and permission.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your file upload permission has expired."
            )

        # Check file count limit
        file_count = get_user_file_count(user_id, session)
        if file_count >= permission.max_files:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You have reached your file limit ({permission.max_files} files)."
            )

    # Validate file type
    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF, DOC, and DOCX files are allowed."
        )

    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)

    if not admin:
        permission = get_user_permission(user_id, session)
        max_size_bytes = permission.max_file_size_mb * 1024 * 1024

        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds limit ({permission.max_file_size_mb}MB)."
            )
    else:
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit (100MB)."
            )

    # Generate unique filename
    file_ext = get_file_extension(file.filename)
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file
    with open(file_path, 'wb') as f:
        f.write(content)

    # Create database record
    db_file = FileUpload(
        user_id=user_id,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_ext,
        processed=False
    )

    session.add(db_file)
    session.commit()
    session.refresh(db_file)

    # Extract text in background (async processing)
    # For now, we'll do it synchronously
    extracted_text = extract_text_from_file(file_path, file_ext)
    if extracted_text:
        db_file.processed_content = extracted_text
        db_file.processed = True
        session.add(db_file)
        session.commit()
        session.refresh(db_file)

    return FileUploadResponse(
        id=db_file.id,
        filename=db_file.original_filename,
        file_size=db_file.file_size,
        file_type=db_file.file_type,
        upload_date=db_file.upload_date,
        processed=db_file.processed
    )


@router.get("", response_model=FileListResponse)
def get_my_files(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get all files uploaded by current user"""
    statement = select(FileUpload).where(FileUpload.user_id == user_id)
    files = session.exec(statement).all()

    file_responses = [
        FileUploadResponse(
            id=f.id,
            filename=f.original_filename,
            file_size=f.file_size,
            file_type=f.file_type,
            upload_date=f.upload_date,
            processed=f.processed
        )
        for f in files
    ]

    return FileListResponse(files=file_responses, total=len(file_responses))


@router.get("/{file_id}", response_model=FileUploadResponse)
def get_file(
    file_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get file details"""
    statement = select(FileUpload).where(
        FileUpload.id == file_id,
        FileUpload.user_id == user_id
    )
    file = session.exec(statement).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileUploadResponse(
        id=file.id,
        filename=file.original_filename,
        file_size=file.file_size,
        file_type=file.file_type,
        upload_date=file.upload_date,
        processed=file.processed
    )


@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a file"""
    statement = select(FileUpload).where(
        FileUpload.id == file_id,
        FileUpload.user_id == user_id
    )
    file = session.exec(statement).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Delete physical file
    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    # Delete database record
    session.delete(file)
    session.commit()

    return {"message": "File deleted successfully"}


@router.post("/request-permission")
def request_permission(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Request file upload permission from admin"""
    # Get user details
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if already has permission
    perm_statement = select(FilePermission).where(FilePermission.user_id == user_id)
    existing_perm = session.exec(perm_statement).first()

    if existing_perm:
        return {"message": "You already have file upload permission"}

    # Check if already requested
    req_statement = select(PermissionRequest).where(
        PermissionRequest.user_id == user_id,
        PermissionRequest.status == "pending"
    )
    existing_req = session.exec(req_statement).first()

    if existing_req:
        return {"message": "Permission request already pending"}

    # Create permission request
    request = PermissionRequest(
        user_id=user_id,
        user_email=user.email,
        user_name=user.name,
        status="pending"
    )

    session.add(request)
    session.commit()

    return {"message": "Permission request sent to admin"}


@router.get("/permission/status")
def get_permission_status(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get current user's permission status"""
    # Check if admin
    if is_admin(user_id, session):
        return {
            "has_permission": True,
            "is_admin": True,
            "max_files": "unlimited",
            "max_file_size_mb": 100
        }

    # Check permission
    statement = select(FilePermission).where(FilePermission.user_id == user_id)
    permission = session.exec(statement).first()

    if not permission:
        return {
            "has_permission": False,
            "is_admin": False,
            "message": "No upload permission. Please request permission."
        }

    # Check expiry
    expired = permission.expires_at and permission.expires_at < datetime.utcnow()

    return {
        "has_permission": permission.can_upload and not expired,
        "is_admin": False,
        "max_files": permission.max_files,
        "max_file_size_mb": permission.max_file_size_mb,
        "current_file_count": get_user_file_count(user_id, session),
        "expires_at": permission.expires_at,
        "expired": expired
    }
