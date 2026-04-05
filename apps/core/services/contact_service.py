from django.db import transaction

from apps.core.models import ContactSubmission
from apps.core.tasks import send_contact_notification_task


def create_submission_and_enqueue_email(*, validated_payload: dict) -> ContactSubmission:
    payload = dict(validated_payload)
    payload.pop("subject", None)

    with transaction.atomic():
        submission = ContactSubmission.objects.create(**payload)

    # why: Async email avoids SMTP latency in API request-response cycle.
    send_contact_notification_task.delay(submission.id)
    return submission
