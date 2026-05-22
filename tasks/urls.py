from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.CustomLoginView.as_view(), name="login-page"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
]
