from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Authentication
    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # Freelancer profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),

    # Client profile
    path(
        "client-profile/",
        views.client_profile,
        name="client_profile"
    ),

    path(
        "client-profile/edit/",
        views.client_profile_edit,
        name="client_profile_edit"
    ),

    # Freelancers
    path(
        "freelancers/",
        views.freelancers,
        name="freelancers"
    ),

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

    # Messages
    path(
        "messages/",
        views.messages_view,
        name="messages"
    ),

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

    # Notifications
    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

    path(
        "notifications/read/",
        views.mark_notifications_read,
        name="mark_notifications_read"
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
