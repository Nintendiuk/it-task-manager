from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import (
    Position, Project, Tag, Task, TaskType, Team, Worker
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ["name", "priority", "is_complete", "deadline"]
    show_change_link = True


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = [
        "username", "first_name", "last_name",
        "email", "position", "is_staff",
    ]
    list_filter = ["position", "is_staff", "is_active"]
    search_fields = ["username", "first_name", "last_name", "email"]
    fieldsets = UserAdmin.fieldsets + (
        ("Work Info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Work Info", {"fields": ("position",)}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ["members"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "team", "deadline", "is_complete"]
    list_filter = ["is_complete", "team"]
    search_fields = ["name", "description"]
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name", "priority", "is_complete",
        "deadline", "task_type", "project",
    ]
    list_filter = ["priority", "is_complete", "task_type"]
    search_fields = ["name", "description"]
    filter_horizontal = ["assignees", "tags"]
