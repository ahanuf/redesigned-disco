from django.conf import settings
from django.db import models


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Normal", "Normal"),
        ("High", "High"),
    ]

    RECURRENCE_CHOICES = [
        ("N", "None"),
        ("D", "Daily"),
        ("W", "Weekly"),
        ("M", "Monthly"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    start = models.DateTimeField()

    end = models.DateTimeField()

    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default="Normal",
    )

    recurrence = models.CharField(
        max_length=1,
        choices=RECURRENCE_CHOICES,
        default="N",
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["start"]
        indexes = [
            models.Index(fields=["owner", "start"]),
        ]