"""
Admin endpoints for permission management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user_id
from app.models.user import User
from app.models.task import Task
from app.models.conversation import Conversation, Message
from app.models.file import (
    FileUpload,
    FilePermission,
    PermissionRequest,
    PermissionGrantRequest,
    PermissionResponse,
    PermissionRequestResponse,
    FileUploadResponse,
)
from datetime import datetime, timedelta
from typing import List

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def verify_admin(user_id: str, session: Session):
    """Verify user is admin"""
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


@router.post("/permissions", response_model=PermissionResponse)
def grant_permission(
    request: PermissionGrantRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Grant file upload permission to a user (Admin only)
    """
    # Verify admin
    verify_admin(user_id, session)

    # Find user by email
    statement = select(User).where(User.email == request.user_email.lower())
    target_user = session.exec(statement).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Don't grant permission to admin
    if target_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin users don't need permission grants"
        )

    # Check if permission already exists
    perm_statement = select(FilePermission).where(
        FilePermission.user_id == target_user.id
    )
    existing_perm = session.exec(perm_statement).first()

    # Calculate expiry date
    expires_at = None
    if request.expires_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_days)

    if existing_perm:
        # Update existing permission
        existing_perm.can_upload = True
        existing_perm.max_files = request.max_files
        existing_perm.max_file_size_mb = request.max_file_size_mb
        existing_perm.expires_at = expires_at
        existing_perm.granted_at = datetime.utcnow()
        existing_perm.granted_by = user_id
        session.add(existing_perm)
        permission = existing_perm
    else:
        # Create new permission
        permission = FilePermission(
            user_id=target_user.id,
            granted_by=user_id,
            can_upload=True,
            max_files=request.max_files,
            max_file_size_mb=request.max_file_size_mb,
            expires_at=expires_at
        )
        session.add(permission)

    session.commit()
    session.refresh(permission)

    # Update any pending permission requests
    req_statement = select(PermissionRequest).where(
        PermissionRequest.user_id == target_user.id,
        PermissionRequest.status == "pending"
    )
    pending_requests = session.exec(req_statement).all()

    for req in pending_requests:
        req.status = "approved"
        req.reviewed_at = datetime.utcnow()
        req.reviewed_by = user_id
        session.add(req)

    session.commit()

    return PermissionResponse(
        user_id=target_user.id,
        user_email=target_user.email,
        can_upload=permission.can_upload,
        max_files=permission.max_files,
        max_file_size_mb=permission.max_file_size_mb,
        granted_at=permission.granted_at,
        expires_at=permission.expires_at
    )


@router.get("/permissions", response_model=List[PermissionResponse])
def list_permissions(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List all granted permissions (Admin only)
    """
    # Verify admin
    verify_admin(user_id, session)

    statement = select(FilePermission)
    permissions = session.exec(statement).all()

    results = []
    for perm in permissions:
        # Get user email
        user_statement = select(User).where(User.id == perm.user_id)
        user = session.exec(user_statement).first()

        if user:
            results.append(PermissionResponse(
                user_id=user.id,
                user_email=user.email,
                can_upload=perm.can_upload,
                max_files=perm.max_files,
                max_file_size_mb=perm.max_file_size_mb,
                granted_at=perm.granted_at,
                expires_at=perm.expires_at
            ))

    return results


@router.delete("/permissions/{target_user_email}")
def revoke_permission(
    target_user_email: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Revoke file upload permission (Admin only)
    """
    # Verify admin
    verify_admin(user_id, session)

    # Find target user
    user_statement = select(User).where(User.email == target_user_email.lower())
    target_user = session.exec(user_statement).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Find permission
    perm_statement = select(FilePermission).where(
        FilePermission.user_id == target_user.id
    )
    permission = session.exec(perm_statement).first()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No permission found for this user"
        )

    # Delete permission
    session.delete(permission)
    session.commit()

    return {"message": f"Permission revoked for {target_user_email}"}


@router.get("/permission-requests", response_model=List[PermissionRequestResponse])
def list_permission_requests(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List all permission requests (Admin only)
    """
    # Verify admin
    verify_admin(user_id, session)

    statement = select(PermissionRequest).where(
        PermissionRequest.status == "pending"
    )
    requests = session.exec(statement).all()

    return [
        PermissionRequestResponse(
            id=req.id,
            user_email=req.user_email,
            user_name=req.user_name,
            requested_at=req.requested_at,
            status=req.status
        )
        for req in requests
    ]


@router.get("/files", response_model=List[dict])
def list_all_files(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List all uploaded files (Admin only)
    """
    # Verify admin
    verify_admin(user_id, session)

    statement = select(FileUpload)
    files = session.exec(statement).all()

    results = []
    for f in files:
        # Get user email
        user_statement = select(User).where(User.id == f.user_id)
        user = session.exec(user_statement).first()

        results.append({
            "id": f.id,
            "filename": f.original_filename,
            "file_size": f.file_size,
            "file_type": f.file_type,
            "upload_date": f.upload_date,
            "processed": f.processed,
            "user_email": user.email if user else "Unknown",
            "user_name": user.name if user else "Unknown"
        })

    return results


@router.get("/users", response_model=List[dict])
def list_all_users(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List all users (Admin only)
    """
    # Verify admin
    verify_admin(user_id, session)

    statement = select(User)
    users = session.exec(statement).all()

    results = []
    for user in users:
        # Get file count
        file_statement = select(FileUpload).where(FileUpload.user_id == user.id)
        file_count = len(session.exec(file_statement).all())

        # Get permission
        perm_statement = select(FilePermission).where(FilePermission.user_id == user.id)
        permission = session.exec(perm_statement).first()

        results.append({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "created_at": user.created_at,
            "file_count": file_count,
            "has_permission": permission is not None,
            "permission_details": {
                "max_files": permission.max_files if permission else None,
                "max_file_size_mb": permission.max_file_size_mb if permission else None,
                "expires_at": permission.expires_at if permission else None
            } if permission else None
        })

    return results


@router.post("/users/{user_email}/reset-password")
def reset_password(
    user_email: str,
    session: Session = Depends(get_session)
):
    """
    Reset user password to 'Test12345678' (Public access for demo/reset)
    """
    from app.auth import hash_password

    # Find target user
    user_statement = select(User).where(User.email == user_email.lower())
    target_user = session.exec(user_statement).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Reset password to default
    target_user.hashed_password = hash_password("Test12345678")
    session.add(target_user)
    session.commit()

    return {"message": f"Password reset for {user_email}. New password: Test12345678"}


@router.delete("/users/{user_email}")
def delete_user(
    user_email: str,
    session: Session = Depends(get_session)
):
    """
    Delete a user and all their data (Public access for demo/reset)
    """
    # Find target user
    user_statement = select(User).where(User.email == user_email.lower())
    target_user = session.exec(user_statement).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete all related data first
    # 1. Delete conversations and messages
    conv_statement = select(Conversation).where(Conversation.user_id == target_user.id)
    conversations = session.exec(conv_statement).all()
    for conv in conversations:
        # Delete messages first
        msg_statement = select(Message).where(Message.conversation_id == conv.id)
        messages = session.exec(msg_statement).all()
        for msg in messages:
            session.delete(msg)
        # Then delete conversation
        session.delete(conv)

    # 2. Delete tasks
    task_statement = select(Task).where(Task.user_id == target_user.id)
    tasks = session.exec(task_statement).all()
    for task in tasks:
        session.delete(task)

    # 3. Delete files
    file_statement = select(FileUpload).where(FileUpload.user_id == target_user.id)
    files = session.exec(file_statement).all()
    for file in files:
        session.delete(file)

    # 4. Delete permissions
    perm_statement = select(FilePermission).where(FilePermission.user_id == target_user.id)
    permissions = session.exec(perm_statement).all()
    for perm in permissions:
        session.delete(perm)

    # 5. Delete permission requests
    req_statement = select(PermissionRequest).where(PermissionRequest.user_id == target_user.id)
    requests = session.exec(req_statement).all()
    for req in requests:
        session.delete(req)

    # Finally delete the user
    session.delete(target_user)
    session.commit()

    return {"message": f"User {user_email} and all related data deleted successfully"}
