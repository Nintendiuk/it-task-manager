import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Position, Project, Task, Worker


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        empty_label="-- No position --",
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "password1",
            "password2",
        ]


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "project",
            "assignees",
            "tags",
            "is_complete",
        ]

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < datetime.date.today():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline


class ProjectForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "team",
            "deadline",
            "is_complete",
        ]

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < datetime.date.today():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline
