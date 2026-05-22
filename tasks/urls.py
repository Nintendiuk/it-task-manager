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
    path(
        "tasks/<int:pk>/toggle/",
        views.toggle_assign_to_task,
        name="toggle-assign",
    ),
]
