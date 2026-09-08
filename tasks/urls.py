from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path(
        "",
        views.tasks_page,
        name="tasks",
    ),

    path(
        "api/",
        views.tasks_api,
        name="tasks_api",
    ),

    path(
        "api/create/",
        views.create_task_api,
        name="create_task_api",
    ),

    path(
        "api/<int:task_id>/delete/",
        views.delete_task_api,
        name="delete_task_api",
    ),
]