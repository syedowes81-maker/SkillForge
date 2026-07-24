from django.urls import path
from . import views

urlpatterns = [
    path("", views.browse_jobs, name="browse_jobs"),
    path("post/", views.post_job, name="post_job"),
    path("applications/", views.my_applications, name="my_applications"),
    path("<int:id>/apply/", views.apply_job, name="apply_job"),
    path("<int:id>/applicants/", views.view_applicants, name="view_applicants"),
    path("<int:id>/", views.job_detail, name="job_detail"),
]
