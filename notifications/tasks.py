from celery import shared_task
from django.db import transaction
import random
import time
from .models import Notification, NotificationStatus
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status

from .models import NotificationStatus
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_notification(self, notification_id):

    try:

        notification = Notification.objects.select_for_update().get(
                            id=notification_id
                        )

        # Prevent reprocessing
        if notification.status == NotificationStatus.SENT:
            return

        notification.status = NotificationStatus.PROCESSING
        notification.save()

        # Simulate processing delay
        time.sleep(5)

        # Simulate random failure
        random_failure = random.choice([True, False])

        if random_failure:
            raise Exception("Simulated notification failure")

        # Success
        notification.status = NotificationStatus.SENT
        notification.last_error = None
        notification.save()

        logger.info(f"Notification {notification.id} sent successfully")

    except Exception as exc:

        notification.retry_count += 1

        notification.last_error = str(exc)

        if notification.retry_count >= 3:

            notification.status = (
                NotificationStatus.PERMANENTLY_FAILED
            )

        else:

            notification.status = NotificationStatus.FAILED

            # Retry after 10 seconds
            self.retry(exc=exc, countdown=10)

        notification.save()

        logger.error(f"Notification {notification.id} failed")






@shared_task
def check_scheduled_notifications():

    with transaction.atomic():

        notifications = (
            Notification.objects
            .select_for_update()
            .filter(
                scheduled_time__lte=timezone.now(),
                status=NotificationStatus.PENDING
            )
        )

        for notification in notifications:

            notification.status = (
                NotificationStatus.PROCESSING
            )

            notification.save()

            process_notification.delay(
                notification.id
            )

            print(
                f"Queued notification {notification.id}"
            )


