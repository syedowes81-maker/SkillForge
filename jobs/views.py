from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job
from .models import Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from .models import Application

@login_required
def post_job(request):

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()

            return redirect("dashboard")

    else:
        form = JobForm()

    return render(request, "jobs/post_job.html", {
        "form": form
    })

from .models import Job


def browse_jobs(request):
    jobs = Job.objects.all().order_by("-created_at")

    return render(request, "jobs/browse_jobs.html", {
        "jobs": jobs
    })

def job_detail(request, id):
    job = Job.objects.get(id=id)

    return render(request, "jobs/job_detail.html", {
        "job": job
    })

@login_required
def apply_job(request, id):
    job = Job.objects.get(id=id)

    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.freelancer = request.user
            application.save()

            return redirect("browse_jobs")

    else:
        form = ApplicationForm()

    return render(request, "jobs/apply_job.html", {
        "form": form,
        "job": job
    })

@login_required
def my_applications(request):
    applications = Application.objects.filter(
        freelancer=request.user
    ).order_by("-applied_at")

    return render(request, "jobs/my_applications.html", {
        "applications": applications
    })

@login_required
def view_applicants(request, id):
    job = Job.objects.get(id=id)

    # Optional safety check: only the client who posted the job can view applicants
    if job.client != request.user:
        return redirect("browse_jobs")

    applications = Application.objects.filter(job=job).order_by("-applied_at")

    return render(request, "jobs/view_applicants.html", {
        "job": job,
        "applications": applications
    })

@login_required
def update_application_status(request, id, status):
    application = Application.objects.get(id=id)

    if application.job.client != request.user:
        return redirect("browse_jobs")

    if status in ["Accepted", "Rejected"]:
        application.status = status
        application.save()

    return redirect("view_applicants", id=application.job.id)

@login_required
def my_jobs(request):
    jobs = Job.objects.filter(client=request.user).order_by("-created_at")

    return render(request, "jobs/my_jobs.html", {
        "jobs": jobs
    })
