from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "start",
            "end",
            "priority",
            "recurrence",
        ]

        widgets = {
            "start": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),

            "end": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }