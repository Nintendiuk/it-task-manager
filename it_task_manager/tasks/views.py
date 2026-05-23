from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django.views.generic.edit import FormView

from tasks.forms import ProjectForm, TaskForm, WorkerCreationForm
from tasks.models import Project, Task, Worker


class CustomLoginView(LoginView):
    template_name = "registration/login.html"


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        request.session.flush()
        return super().dispatch(request, *args, **kwargs)


class SignupView(FormView):
    template_name = "registration/signup.html"
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:login-page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("tasks:index")


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"
    context_object_name = "worker"

    def get_queryset(self):
        return Worker.objects.select_related("position").prefetch_related(
            "assigned_tasks__project",
            "assigned_tasks__task_type",
        )


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "tasks/worker_list.html"
    context_object_name = "workers"
    paginate_by = 10

    def get_queryset(self):
        qs = Worker.objects.select_related("position")
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(username__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_string"] = self.request.GET.urlencode()
        context["search_query"] = self.request.GET.get("q", "")
        return context


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        return (
            Task.objects
            .select_related("task_type", "project")
            .prefetch_related("assignees", "tags")
            .filter(is_complete=False)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visits = self.request.session.get("visit_count", 0) + 1
        self.request.session["visit_count"] = visits
        context["visit_count"] = visits
        return context


class ToggleAssignToTaskView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user in task.assignees.all():
            task.assignees.remove(request.user)
        else:
            task.assignees.add(request.user)
        return redirect("tasks:task-detail", pk=pk)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Task.objects
            .select_related("task_type", "project")
            .prefetch_related("assignees", "tags")
        )
        query = self.request.GET.get("q", "").strip()
        priority = self.request.GET.get("priority", "").strip()
        if query:
            qs = qs.filter(name__icontains=query)
        if priority:
            qs = qs.filter(priority=priority)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_string"] = self.request.GET.urlencode()
        context["search_query"] = self.request.GET.get("q", "")
        context["priority_filter"] = self.request.GET.get("priority", "")
        context["priorities"] = Task.Priority.choices
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return (
            Task.objects
            .select_related("task_type", "project")
            .prefetch_related("assignees", "tags")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_assigned"] = (
            self.request.user in self.object.assignees.all()
        )
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")

    def test_func(self):
        return self.request.user.is_staff


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasks/project_list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Project.objects
            .select_related("team")
            .prefetch_related("tasks")
        )
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_string"] = self.request.GET.urlencode()
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "tasks/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return (
            Project.objects
            .select_related("team")
            .prefetch_related("tasks__assignees", "tasks__task_type")
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("tasks:project-list")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project_form.html"
    success_url = reverse_lazy("tasks:project-list")


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "tasks/project_confirm_delete.html"
    success_url = reverse_lazy("tasks:project-list")

    def test_func(self):
        return self.request.user.is_staff
