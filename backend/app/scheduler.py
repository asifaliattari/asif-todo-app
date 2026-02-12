"""
Background scheduler for task reminders
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.email_service import email_service
from app.database import get_session
import logging

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()


def check_reminders_job():
    """Background job to check and send task reminders"""
    try:
        logger.info("Running reminder check job...")
        session = next(get_session())
        email_service.check_and_send_reminders(session)
        logger.info("Reminder check completed")
    except Exception as e:
        logger.error(f"Error in reminder check job: {str(e)}")


def start_scheduler():
    """Start the background scheduler"""
    if not scheduler.running:
        # Check for reminders every 10 minutes
        scheduler.add_job(
            check_reminders_job,
            trigger=IntervalTrigger(minutes=10),
            id="reminder_check",
            name="Check task reminders every 10 minutes",
            replace_existing=True
        )

        scheduler.start()
        logger.info("Scheduler started - checking reminders every 10 minutes")


def stop_scheduler():
    """Stop the background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
