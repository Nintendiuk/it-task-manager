from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
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
