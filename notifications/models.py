from django.db import models
from django.db import models
from django.contrib.auth.models import User


class NotificationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"
    PERMANENTLY_FAILED = "PERMANENTLY_FAILED", "Permanently Failed"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    scheduled_time = models.DateTimeField()

    status = models.CharField(
        max_length=30,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING
    )

    retry_count = models.PositiveIntegerField(default=0)

    last_error = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title