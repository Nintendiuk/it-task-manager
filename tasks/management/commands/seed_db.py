import datetime

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from tasks.models import Position, Project, Tag, Task, TaskType, Team, Worker


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        pos_dev, _ = Position.objects.get_or_create(name="Developer")
        pos_pm, _ = Position.objects.get_or_create(name="Project Manager")
        TaskType.objects.get_or_create(name="Bug Fix")
        tt_feat, _ = TaskType.objects.get_or_create(name="Feature")
        tt_ref, _ = TaskType.objects.get_or_create(name="Refactor")
        tag_be, _ = Tag.objects.get_or_create(name="backend")
        tag_urg, _ = Tag.objects.get_or_create(name="urgent")

        admin_user, _ = Worker.objects.get_or_create(
            username="admin",
            defaults={
                "password": make_password("admin123"),
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
                "position": pos_dev,
            },
        )
        alice, _ = Worker.objects.get_or_create(
            username="alice",
            defaults={
                "password": make_password("alice123"),
                "first_name": "Alice",
                "last_name": "Smith",
                "position": pos_dev,
            },
        )
        bob, _ = Worker.objects.get_or_create(
            username="bob",
            defaults={
                "password": make_password("bob123"),
                "first_name": "Bob",
                "last_name": "Jones",
                "position": pos_pm,
            },
        )

        team, _ = Team.objects.get_or_create(name="Core Team")
        team.members.set([admin_user, alice, bob])

        future = datetime.date.today() + datetime.timedelta(days=30)
        far = datetime.date.today() + datetime.timedelta(days=60)

        proj_a, _ = Project.objects.get_or_create(
            name="Project Alpha",
            defaults={"team": team, "deadline": future},
        )
        proj_b, _ = Project.objects.get_or_create(
            name="Project Beta",
            defaults={"team": team, "deadline": far},
        )

        tasks_data = [
            {
                "name": "Fix login bug",
                "priority": Task.Priority.CRITICAL,
                "task_type": tt_feat,
                "project": proj_a,
                "deadline": future,
            },
            {
                "name": "Add dashboard",
                "priority": Task.Priority.HIGH,
                "task_type": tt_feat,
                "project": proj_a,
                "deadline": future,
            },
            {
                "name": "Refactor models",
                "priority": Task.Priority.MEDIUM,
                "task_type": tt_ref,
                "project": proj_b,
                "deadline": future,
                "is_complete": True,
            },
            {
                "name": "Write tests",
                "priority": Task.Priority.HIGH,
                "task_type": tt_feat,
                "project": proj_b,
                "deadline": far,
            },
            {
                "name": "Update docs",
                "priority": Task.Priority.LOW,
                "task_type": tt_feat,
                "project": proj_b,
                "deadline": far,
            },
        ]
        for data in tasks_data:
            task, created = Task.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                task.assignees.add(alice)
                task.tags.add(tag_be)
                if data["priority"] == Task.Priority.CRITICAL:
                    task.tags.add(tag_urg)

        self.stdout.write(self.style.SUCCESS("Done!"))
        self.stdout.write("  admin / admin123  (superuser)")
        self.stdout.write("  alice / alice123")
        self.stdout.write("  bob   / bob123")
