"""
Notification endpoints for email reminders
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.auth import get_current_user_id
from app.models.user import User
from app.email_service import email_service
from sqlmodel import select

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.post("/test-email")
def send_test_email(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Send a test email to verify email configuration
    """
    # Get user
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create test email content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                <h1 style="margin: 0; color: white; font-size: 28px;">✅ Email Notifications Active!</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 30px;">
                                <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px;">Hi {user.name}! 👋</p>
                                <p style="margin: 0 0 20px 0; color: #6b7280; font-size: 14px;">
                                    Great news! Email notifications are now working for your TaskFlow account.
                                </p>
                                <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 14px;">
                                    <strong>You'll receive emails for:</strong>
                                </p>
                                <ul style="color: #6b7280; font-size: 14px;">
                                    <li>Tasks due in 1 hour (⏰ reminder)</li>
                                    <li>Tasks due now (🔔 notification)</li>
                                    <li>Overdue tasks (⚠️ alert)</li>
                                </ul>
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <a href="https://asif-todo-app.vercel.app" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 14px 32px; border-radius: 6px; font-weight: bold; font-size: 16px;">
                                                Open TaskFlow
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                                <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                    Created by Asif Ali AstolixGen | GIAIC Hackathon 2026
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Send test email
    success = email_service.send_email(
        to_email=user.email,
        subject="✅ TaskFlow Email Notifications Active",
        html_content=html_content
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email. Please check SMTP configuration."
        )

    return {
        "message": f"Test email sent successfully to {user.email}",
        "status": "success"
    }


@router.post("/trigger-reminders")
def trigger_reminder_check(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Manually trigger reminder check (for testing)
    """
    # Verify admin
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    # Run reminder check
    email_service.check_and_send_reminders(session)

    return {
        "message": "Reminder check triggered successfully",
        "status": "success"
    }
