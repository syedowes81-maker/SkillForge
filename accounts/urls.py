from django.urls import path
from .import views

urlpatterns=[
   path("",views.home,name="home"),
   path("register/",views.register,name="register"),
   path("login/",views.login_view,name="login"),
   path("dashboard/",views.dashboard,name="dashboard"),
   path("logout/",views.logout_view,name="logout"),
   path("profile/",views.profile,name="profile"),
   path("profile/edit/",views.edit_profile,name="edit_profile"),
   path("freelancers/",views.freelancers,name="freelancers"),
   path("freelancers/<int:id>/",views.freelancer_detail,name="freelancer_detail"),
   path("freelancers/<int:id>/review/",views.add_review,name="add_review"),
   path("messages/", views.messages_view, name="messages"),
   path("messages/conversation/<int:id>/",views.conversation,name="conversation"),
   path("messages/send/<int:id>/",views.send_message,name="send_message"),
   path("notifications/", views.notifications, name="notifications"),
]
