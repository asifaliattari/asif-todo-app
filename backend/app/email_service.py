"""
Email notification service for task reminders
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List
import os
from sqlmodel import Session, select
from app.models.task import Task
from app.models.user import User


class EmailService:
    """Email notification service using Gmail SMTP"""

    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SMTP_EMAIL", "")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        self.app_name = "TaskFlow"

    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send an email using Gmail SMTP"""
        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured")
            return False

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.app_name} <{self.sender_email}>"
            message["To"] = to_email

            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def get_task_reminder_email(self, task: Task, user_name: str, reminder_type: str) -> str:
        """Generate HTML email for task reminder"""

        # Determine emoji and message based on reminder type
        if reminder_type == "due_soon":
            emoji = "⏰"
            title = "Task Due Soon!"
            message = "This task is due in 1 hour:"
            color = "#f59e0b"  # Yellow
        elif reminder_type == "due_now":
            emoji = "🔔"
            title = "Task Due Now!"
            message = "This task is due now:"
            color = "#3b82f6"  # Blue
        elif reminder_type == "overdue":
            emoji = "⚠️"
            title = "Task Overdue!"
            message = "This task is overdue:"
            color = "#ef4444"  # Red
        else:
            emoji = "📋"
            title = "Task Reminder"
            message = "You have a task reminder:"
            color = "#8b5cf6"  # Purple

        # Priority badge
        priority_colors = {
            "high": "#ef4444",
            "medium": "#f59e0b",
            "low": "#10b981"
        }
        priority_color = priority_colors.get(task.priority, "#6b7280")

        # Format due date
        due_date_str = "Not set"
        if task.due_date:
            due_date_str = task.due_date.strftime("%B %d, %Y at %I:%M %p")

        # Tags
        tags_html = ""
        if task.tags:
            tags_html = " ".join([f'<span style="background-color: #8b5cf6; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 4px;">#{tag}</span>' for tag in task.tags])

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                    <h1 style="margin: 0; color: white; font-size: 28px;">{emoji} {self.app_name}</h1>
                                    <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">{title}</p>
                                </td>
                            </tr>

                            <!-- Content -->
                            <tr>
                                <td style="padding: 30px;">
                                    <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px;">Hi {user_name},</p>
                                    <p style="margin: 0 0 20px 0; color: #6b7280; font-size: 14px;">{message}</p>

                                    <!-- Task Card -->
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f9fafb; border-left: 4px solid {color}; border-radius: 6px; margin: 20px 0;">
                                        <tr>
                                            <td style="padding: 20px;">
                                                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                                    <h2 style="margin: 0; color: #111827; font-size: 20px; flex: 1;">{task.title}</h2>
                                                    <span style="background-color: {priority_color}; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase;">{task.priority}</span>
                                                </div>

                                                {f'<p style="margin: 10px 0; color: #6b7280; font-size: 14px;">{task.description}</p>' if task.description else ''}

                                                {f'<div style="margin: 10px 0;">{tags_html}</div>' if tags_html else ''}

                                                <p style="margin: 15px 0 0 0; color: #9ca3af; font-size: 13px;">
                                                    📅 <strong>Due:</strong> {due_date_str}
                                                </p>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- CTA Button -->
                                    <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                        <tr>
                                            <td align="center">
                                                <a href="https://asif-todo-app.vercel.app" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 14px 32px; border-radius: 6px; font-weight: bold; font-size: 16px;">
                                                    View Task in App
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                                    <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                        Created by Asif Ali AstolixGen | GIAIC Hackathon 2026
                                    </p>
                                    <p style="margin: 10px 0 0 0; color: #9ca3af; font-size: 12px;">
                                        You're receiving this because you have task reminders enabled in TaskFlow.
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

        return html

    def get_daily_digest_email(self, user_name: str, tasks: List[Task]) -> str:
        """Generate HTML email for daily task digest"""

        # Count tasks by status
        total = len(tasks)
        overdue = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and not t.completed])
        due_today = len([t for t in tasks if t.due_date and t.due_date.date() == datetime.utcnow().date() and not t.completed])

        # Generate task list HTML
        tasks_html = ""
        for task in tasks[:10]:  # Show max 10 tasks
            status_icon = "✅" if task.completed else "⭕"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")

            tasks_html += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 20px; margin-right: 10px;">{status_icon}</span>
                        <div style="flex: 1;">
                            <strong style="color: #111827;">{task.title}</strong>
                            {f'<br><span style="color: #6b7280; font-size: 13px;">{task.description[:50]}...</span>' if task.description else ''}
                        </div>
                        <span style="margin-left: 10px;">{priority_emoji}</span>
                    </div>
                </td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                    <h1 style="margin: 0; color: white; font-size: 28px;">📊 Daily Task Summary</h1>
                                    <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">{datetime.utcnow().strftime("%A, %B %d, %Y")}</p>
                                </td>
                            </tr>

                            <!-- Stats -->
                            <tr>
                                <td style="padding: 30px;">
                                    <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px;">Good morning {user_name}! 👋</p>

                                    <table width="100%" cellpadding="0" cellspacing="10">
                                        <tr>
                                            <td width="33%" style="background-color: #dbeafe; padding: 15px; border-radius: 6px; text-align: center;">
                                                <div style="font-size: 28px; font-weight: bold; color: #1e40af;">{total}</div>
                                                <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">Total Tasks</div>
                                            </td>
                                            <td width="33%" style="background-color: #fef3c7; padding: 15px; border-radius: 6px; text-align: center;">
                                                <div style="font-size: 28px; font-weight: bold; color: #b45309;">{due_today}</div>
                                                <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">Due Today</div>
                                            </td>
                                            <td width="33%" style="background-color: #fee2e2; padding: 15px; border-radius: 6px; text-align: center;">
                                                <div style="font-size: 28px; font-weight: bold; color: #b91c1c;">{overdue}</div>
                                                <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">Overdue</div>
                                            </td>
                                        </tr>
                                    </table>

                                    <h3 style="margin: 30px 0 15px 0; color: #111827;">Your Tasks:</h3>
                                    <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #e5e7eb; border-radius: 6px; overflow: hidden;">
                                        {tasks_html}
                                    </table>

                                    <!-- CTA Button -->
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

                            <!-- Footer -->
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

        return html

    def check_and_send_reminders(self, session: Session):
        """Check for tasks that need reminders and send emails"""
        now = datetime.utcnow()
        one_hour_later = now + timedelta(hours=1)

        # Get all tasks with reminder dates
        statement = select(Task).where(
            Task.reminder_date.isnot(None),
            Task.completed == False,
            Task.reminder_date <= one_hour_later
        )
        tasks = session.exec(statement).all()

        for task in tasks:
            # Get user
            user_statement = select(User).where(User.id == task.user_id)
            user = session.exec(user_statement).first()

            if not user:
                continue

            # Determine reminder type
            if task.reminder_date <= now:
                reminder_type = "due_now"
            elif task.reminder_date <= one_hour_later:
                reminder_type = "due_soon"
            else:
                continue

            # Generate and send email
            html_content = self.get_task_reminder_email(task, user.name, reminder_type)
            subject = f"⏰ Reminder: {task.title}"

            self.send_email(user.email, subject, html_content)

            # Update reminder_date to avoid sending multiple times
            task.reminder_date = None
            session.add(task)

        session.commit()
        print(f"Checked reminders: {len(tasks)} tasks processed")


# Global instance
email_service = EmailService()
