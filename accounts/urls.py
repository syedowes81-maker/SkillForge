from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    path("freelancers/", views.freelancers, name="freelancers"),
    path(
        "freelancers/<int:id>/",
        views.freelancer_detail,
        name="freelancer_detail"
    ),
    path(
        "freelancers/<int:id>/review/",
        views.add_review,
        name="add_review"
    ),

    path("messages/", views.messages_view, name="messages"),
    path(
        "messages/conversation/<int:id>/",
        views.conversation,
        name="conversation"
    ),
    path(
        "messages/send/<int:id>/",
        views.send_message,
        name="send_message"
    ),

    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

    # Password reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
