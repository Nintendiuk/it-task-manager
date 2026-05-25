from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Project, Task


class PublicViewsTests(TestCase):

    def setUp(self):
        self.worker_user = get_user_model().objects.create_user(
            username="testworker", password="password123"
        )
        self.project = Project.objects.create(name="Test Project")
        self.task = Task.objects.create(
            name="Test Task",
            project=self.project,
        )

    def test_login_required_for_private_pages(self):
        """Verify that anonymous users are redirected to the login page"""
        urls = [
            reverse("tasks:index"),
            reverse("tasks:worker-list"),
            reverse("tasks:worker-detail", kwargs={"pk": self.worker_user.pk}),
            reverse("tasks:task-list"),
            reverse("tasks:task-detail", kwargs={"pk": self.task.pk}),
            reverse("tasks:task-create"),
            reverse("tasks:project-list"),
            reverse("tasks:project-detail", kwargs={"pk": self.project.pk}),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login/", response.url)


class PrivateViewsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="developer", password="password123", is_staff=True
        )
        self.client.login(username="developer", password="password123")

        self.project_1 = Project.objects.create(name="Alpha Project")
        self.project_2 = Project.objects.create(name="Beta Project")

        self.task_1 = Task.objects.create(
            name="Fix authentication bug",
            project=self.project_1,
            is_complete=False
        )
        self.task_2 = Task.objects.create(
            name="Write view tests",
            project=self.project_2,
            is_complete=True
        )

    def test_index_view_returns_only_incomplete_tasks(self):
        """Verify that the index page displays only incomplete tasks"""
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

        tasks_in_context = response.context["tasks"]
        self.assertIn(self.task_1, tasks_in_context)
        self.assertNotIn(self.task_2, tasks_in_context)

    def test_index_view_session_visit_count(self):
        """Verify that the session visit counter increments correctly on the index page"""
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.context["visit_count"], 1)

        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.context["visit_count"], 2)

    def test_worker_list_view_search(self):
        """Verify worker search and filtering functionality by username"""
        get_user_model().objects.create_user(username="designer", password="123")

        response = self.client.get(reverse("tasks:worker-list"), {"q": "dev"})
        workers = response.context["workers"]
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].username, "developer")

    def test_task_list_view_search_and_context(self):
        """Verify task search functionality and presence of filter parameters in the context"""
        response = self.client.get(
            reverse("tasks:task-list"),
            {"q": "Fix", "priority": "HIGH"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_query"], "Fix")
        self.assertEqual(response.context["priority_filter"], "HIGH")
        self.assertIsNotNone(response.context["query_string"])

    def test_toggle_assign_to_task_view(self):
        """Verify assigning and removing a user from a task via a POST request"""
        url = reverse("tasks:toggle-assign", kwargs={"pk": self.task_1.pk})

        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:task-detail", kwargs={"pk": self.task_1.pk}))
        self.assertTrue(self.task_1.assignees.filter(pk=self.user.pk).exists())

        response = self.client.post(url)
        self.assertFalse(self.task_1.assignees.filter(pk=self.user.pk).exists())

    def test_project_create_view_post(self):
        """Verify successful project creation through the form submission"""
        form_data = {"name": "Gamma Project"}
        response = self.client.post(reverse("tasks:project-create"), data=form_data)

        self.assertRedirects(response, reverse("tasks:project-list"))
        self.assertTrue(Project.objects.filter(name="Gamma Project").exists())

    def test_project_delete_view_post(self):
        """Verify successful project deletion via a POST request"""
        project_to_delete = Project.objects.create(name="Temporary Project")
        url = reverse("tasks:project-delete", kwargs={"pk": project_to_delete.pk})

        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:project-list"))
        self.assertFalse(Project.objects.filter(pk=project_to_delete.pk).exists())
