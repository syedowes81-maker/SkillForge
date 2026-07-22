from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.post_job, name="post_job"),
    path("",views.browse_jobs,name="browse_jobs"),
]
