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
