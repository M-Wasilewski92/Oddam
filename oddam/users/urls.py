from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = "users"

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="./password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="./password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="./password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", views.Activate.as_view(), name="activate"),
    path(
        "password_reset/", views.PasswordResetRequest.as_view(), name="password_reset"
    ),
    path("settings/", views.UserSettings.as_view(), name="settings"),
]
