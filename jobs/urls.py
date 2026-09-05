from django.urls import path
from .import views

urlpatterns = [
    path("", views.browse_jobs, name="browse_jobs"),
    path("post/", views.post_job, name="post_job"),
    path("applications/", views.my_applications, name="my_applications"),
    path("my-work/", views.my_work, name="my_work"),
    path("my-work/<int:id>/complete/",views.complete_work,name="complete_work"),
    path("my-projects/",views.my_projects,name="my_projects"),
    path("my-projects/<int:id>/confirm/",views.confirm_completion,name="confirm_completion"),
    path("my-jobs/",views.my_jobs,name="my_jobs"),
    path("saved/", views.saved_jobs, name="saved_jobs"),
    path("<int:id>/apply/", views.apply_job, name="apply_job"),
    path("<int:id>/withdraw/",views.withdraw_application,name="withdraw_application"),
    path("<int:id>/applicants/", views.view_applicants, name="view_applicants"),
    path("<int:id>/status/<str:status>/",views.update_application_status,name="update_application_status"),
    path("<int:id>/edit/",views.edit_job,name="edit_job"),
    path("<int:id>/delete/",views.delete_job,name="delete_job"),
    path("<int:id>/toggle-status/", views.toggle_job_status, name="toggle_job_status"),
    path("<int:id>/save/",views.save_job,name="save_job"),
    path("<int:id>/unsave/",views.unsave_job,name="unsave_job"),
    path("<int:id>/", views.job_detail, name="job_detail"),
]
