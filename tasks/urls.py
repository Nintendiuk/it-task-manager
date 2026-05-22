from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.CustomLoginView.as_view(), name="login-page"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        views.WorkerDetailView.as_view(),
        name="worker-detail",
    ),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path(
        "tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "tasks/create/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "tasks/<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path(
        "tasks/<int:pk>/toggle/",
        views.toggle_assign_to_task,
        name="toggle-assign",
    ),
    path(
        "projects/",
        views.ProjectListView.as_view(),
        name="project-list",
    ),
    path(
        "projects/<int:pk>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/create/",
        views.ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/update/",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project-delete",
    ),
]
