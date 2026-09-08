from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "start",
        "end",
        "priority",
        "recurrence",
        "completed",
    )

    list_filter = (
        "priority",
        "recurrence",
        "completed",
    )

    search_fields = (
        "title",
        "description",
        "owner__username",
    )

    ordering = (
        "start",
    )