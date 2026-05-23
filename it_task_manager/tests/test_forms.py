import datetime
from django.test import TestCase
from tasks.forms import WorkerCreationForm, TaskForm, ProjectForm
from tasks.models import Position, Project, TaskType


class WorkerCreationFormTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_creation_form_valid_data(self):
        """Verify form is valid with correct user and position data"""
        form_data = {
            "username": "new_developer",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": self.position.id,
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_missing_required_username(self):
        """Verify form is invalid when required username is missing"""
        form_data = {
            "username": "",
            "position": self.position.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class TaskFormTests(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name="Alpha Project")
        self.task_type = TaskType.objects.create(name="Bugfix")

    def test_task_form_valid_data(self):
        """Verify task form is valid with correct data and future deadline"""
        future_date = datetime.date.today() + datetime.timedelta(days=5)
        form_data = {
            "name": "Fix DB Connection",
            "description": "Resolve connection pooling issues.",
            "deadline": future_date,
            "priority": "HIGH",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "assignees": [],
            "tags": [],
            "is_complete": False,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_past_deadline(self):
        """Verify task form raises validation error for past deadline"""
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {
            "name": "Fix DB Connection",
            "deadline": past_date,
            "priority": "HIGH",
            "task_type": self.task_type.id,
            "project": self.project.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        self.assertEqual(form.errors["deadline"][0], "Deadline cannot be in the past.")


class ProjectFormTests(TestCase):

    def test_project_form_valid_data(self):
        """Verify project form is valid with correct data and no deadline"""
        form_data = {
            "name": "Beta Project",
            "description": "Development of Beta phase.",
            "team": [],
            "deadline": "",
            "is_complete": False,
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_project_form_invalid_past_deadline(self):
        """Verify project form raises validation error for past deadline"""
        past_date = datetime.date.today() - datetime.timedelta(days=5)
        form_data = {
            "name": "Old Project",
            "deadline": past_date,
            "is_complete": False,
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        self.assertEqual(form.errors["deadline"][0], "Deadline cannot be in the past.")
