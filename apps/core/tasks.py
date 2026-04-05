import logging

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from apps.core.models import ContactSubmission

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 4},
    soft_time_limit=20,
    time_limit=30,
)
def send_contact_notification_task(self, submission_id: int) -> None:
    idempotency_key = f"contact-email-lock:{submission_id}"
    if not cache.add(idempotency_key, "1", timeout=300):
        logger.info("Contact notification already queued for submission=%s", submission_id)
        return

    submission = ContactSubmission.objects.filter(pk=submission_id).only(
        "id",
        "name",
        "email",
        "company",
        "service_interest",
        "message",
    ).first()
    if submission is None:
        logger.warning("Contact submission not found for notification: %s", submission_id)
        return

    sent = send_mail(
        subject=f"[Portfolio Contact] {submission.service_interest or 'General Inquiry'}",
        message=(
            f"Name: {submission.name}\n"
            f"Email: {submission.email}\n"
            f"Company: {submission.company or 'N/A'}\n"
            f"Service Interest: {submission.service_interest or 'N/A'}\n\n"
            f"Message:\n{submission.message}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
        fail_silently=False,
    )
    logger.info(
        "Contact notification completed submission=%s sent_count=%s",
        submission_id,
        sent,
    )
