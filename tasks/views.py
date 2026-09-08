from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .forms import TaskForm
from .models import Task


@login_required
def tasks_page(request):
    form = TaskForm()

    return render(
        request,
        "tasks/tasks.html",
        {
            "form": form,
        },
    )

@login_required
@require_GET
def tasks_api(request):

    start = request.GET.get("start")
    end = request.GET.get("end")

    tasks = Task.objects.filter(
        owner=request.user
    )

    if start and end:
        tasks = tasks.filter(
            start__lt=end,
            end__gt=start,
        )

    events = []

    for task in tasks:

        events.append({
            "id": task.id, # type: ignore
            "title": task.title,
            "start": task.start.isoformat(),
            "end": task.end.isoformat(),
            "extendedProps": {
                "priority": task.priority,
                "recurrence": task.recurrence,
                "completed": task.completed,
                "description": task.description,
            },
        })

    return JsonResponse(events, safe=False)

@login_required
@require_POST
def create_task_api(request):

    form = TaskForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors,
            },
            status=400,
        )

    task = form.save(commit=False)

    task.owner = request.user

    task.save()

    return JsonResponse({
        "status": "success",
        "id": task.id,
    })

@login_required
@require_POST
def delete_task_api(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )

    task.delete()

    return JsonResponse({
        "status": "success",
    })