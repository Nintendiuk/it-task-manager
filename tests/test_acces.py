from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Project, Task


class AccessControlTests(TestCase):

    def setUp(self):
        self.regular_worker = get_user_model().objects.create_user(
            username="regular.developer",
            password="password123",
            is_staff=False
        )
        self.manager_worker = get_user_model().objects.create_user(
            username="manager.admin",
            password="password123",
            is_staff=True
        )

        self.project = Project.objects.create(name="Core Infrastructure")
        self.task = Task.objects.create(
            name="Deploy to production",
            project=self.project
        )

        self.project_delete_url = reverse(
            "tasks:project-delete",
            kwargs={"pk": self.project.pk}
        )
        self.task_delete_url = reverse(
            "tasks:task-delete",
            kwargs={"pk": self.task.pk}
        )

    def test_regular_worker_cannot_delete_project(self):
        """Verify that a non-staff worker receives a 403 Forbidden status when attempting to delete a project"""
        self.client.login(username="regular.developer", password="password123")

        response = self.client.post(self.project_delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_regular_worker_cannot_delete_task(self):
        """Verify that a non-staff worker receives a 403 Forbidden status when attempting to delete a task"""
        self.client.login(username="regular.developer", password="password123")

        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_manager_can_delete_project(self):
        """Verify that a staff manager can successfully delete a project"""
        self.client.login(username="manager.admin", password="password123")

        response = self.client.post(self.project_delete_url)
        self.assertRedirects(response, reverse("tasks:project-list"))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_manager_can_delete_task(self):
        """Verify that a staff manager can successfully delete a task"""
        self.client.login(username="manager.admin", password="password123")

        response = self.client.post(self.task_delete_url)
        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
