from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.username

    @property
    def completed_tasks(self):
        return self.assigned_tasks.filter(is_complete=True)

    @property
    def uncompleted_tasks(self):
        return self.assigned_tasks.filter(is_complete=False)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="teams",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    deadline = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    deadline = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="assigned_tasks",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tasks",
    )

    class Meta:
        ordering = ["-priority", "deadline"]

    def __str__(self):
        return self.name
