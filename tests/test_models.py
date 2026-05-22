import datetime

import pytest
from django.db import IntegrityError

from tasks.models import (
    Position, Project, Tag, Task, TaskType, Team, Worker
)


@pytest.mark.django_db
class TestPosition:
    def test_str(self):
        pos = Position.objects.create(name="Developer")
        assert str(pos) == "Developer"

    def test_unique_name(self):
        Position.objects.create(name="Unique")
        with pytest.raises(IntegrityError):
            Position.objects.create(name="Unique")


@pytest.mark.django_db
class TestTaskType:
    def test_str(self):
        tt = TaskType.objects.create(name="Bug Fix")
        assert str(tt) == "Bug Fix"


@pytest.mark.django_db
class TestTag:
    def test_str(self):
        tag = Tag.objects.create(name="backend")
        assert str(tag) == "backend"


@pytest.mark.django_db
class TestWorker:
    def test_str_with_full_name(self):
        pos = Position.objects.create(name="Dev")
        worker = Worker.objects.create_user(
            username="john", password="pass",
            first_name="John", last_name="Doe", position=pos,
        )
        assert str(worker) == "John Doe"

    def test_str_fallback_to_username(self):
        worker = Worker.objects.create_user(
            username="janedoe", password="pass"
        )
        assert str(worker) == "janedoe"

    def test_completed_tasks_property(self):
        worker = Worker.objects.create_user(
            username="worker1", password="pass"
        )
        done = Task.objects.create(name="Done", is_complete=True)
        open_ = Task.objects.create(name="Open", is_complete=False)
        done.assignees.add(worker)
        open_.assignees.add(worker)
        assert done in worker.completed_tasks
        assert open_ not in worker.completed_tasks

    def test_uncompleted_tasks_property(self):
        worker = Worker.objects.create_user(
            username="worker2", password="pass"
        )
        done = Task.objects.create(name="Done2", is_complete=True)
        open_ = Task.objects.create(name="Open2", is_complete=False)
        done.assignees.add(worker)
        open_.assignees.add(worker)
        assert open_ in worker.uncompleted_tasks
        assert done not in worker.uncompleted_tasks


@pytest.mark.django_db
class TestTeam:
    def test_str(self):
        assert str(Team.objects.create(name="Alpha")) == "Alpha"

    def test_members_m2m(self):
        team = Team.objects.create(name="Beta")
        w = Worker.objects.create_user(username="m1", password="pass")
        team.members.add(w)
        assert w in team.members.all()


@pytest.mark.django_db
class TestProject:
    def test_str(self):
        assert str(Project.objects.create(name="P1")) == "P1"

    def test_deadline_optional(self):
        assert Project.objects.create(name="ND").deadline is None


@pytest.mark.django_db
class TestTask:
    def test_str(self):
        assert str(Task.objects.create(name="Fix bug")) == "Fix bug"

    def test_default_priority(self):
        assert Task.objects.create(name="T").priority == Task.Priority.MEDIUM

    def test_default_is_complete(self):
        assert Task.objects.create(name="T2").is_complete is False

    @pytest.mark.parametrize("priority", [
        Task.Priority.LOW, Task.Priority.MEDIUM,
        Task.Priority.HIGH, Task.Priority.CRITICAL,
    ])
    def test_priority_choices(self, priority):
        t = Task.objects.create(name=f"T-{priority}", priority=priority)
        assert t.priority == priority

    def test_assignees_m2m(self):
        task = Task.objects.create(name="Assigned")
        w = Worker.objects.create_user(username="a1", password="pass")
        task.assignees.add(w)
        assert w in task.assignees.all()

    def test_tags_m2m(self):
        task = Task.objects.create(name="Tagged")
        tag = Tag.objects.create(name="urgent")
        task.tags.add(tag)
        assert tag in task.tags.all()

    def test_deadline_field(self):
        future = datetime.date.today() + datetime.timedelta(days=10)
        t = Task.objects.create(name="DL", deadline=future)
        assert t.deadline == future
