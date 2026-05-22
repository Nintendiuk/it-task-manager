from django.contrib.auth.models import AbstractUser
from django.db import models


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
