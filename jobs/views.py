from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job
from .models import Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from .models import Application
from .models import Job,Application,SavedJob
from accounts.models import Notification

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
            Notification.objects.create(
            user=job.client,
            message=f"{request.user.username} applied for your job '{job.title}'"
)
            return redirect("browse_jobs")

    else:
        form = ApplicationForm()

    return render(request, "jobs/apply_job.html",{
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
        Notification.objects.create(
        user=application.freelancer,
        message=f"Your application for '{application.job.title}' was {status}."
)

    return redirect("view_applicants", id=application.job.id)

@login_required
def my_jobs(request):
    jobs = Job.objects.filter(client=request.user).order_by("-created_at")

    return render(request, "jobs/my_jobs.html", {
        "jobs": jobs
    })

@login_required
def edit_job(request, id):
    job = Job.objects.get(id=id)

    if job.client != request.user:
        return redirect("my_jobs")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("my_jobs")

    else:
        form = JobForm(instance=job)

    return render(request, "jobs/edit_job.html", {
        "form": form
    })

@login_required
def delete_job(request, id):
    job = Job.objects.get(id=id)

    if job.client != request.user:
        return redirect("my_jobs")

    if request.method == "POST":
        job.delete()
        return redirect("my_jobs")

    return render(request, "jobs/delete_job.html", {
        "job": job
    })

@login_required
def save_job(request, id):
    job = Job.objects.get(id=id)

    SavedJob.objects.get_or_create(
        freelancer=request.user,
        job=job
    )

    return redirect("job_detail", id=job.id)

@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(
        freelancer=request.user
    )

    return render(
        request,
        "jobs/saved_jobs.html",
        {
            "saved": saved
        }
    )
@login_required
def unsave_job(request, id):
    job = Job.objects.get(id=id)

    SavedJob.objects.filter(
        freelancer=request.user,
        job=job
    ).delete()

    return redirect("saved_jobs")

def browse_jobs(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    max_budget = request.GET.get("max_budget")

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)

    if category:
        jobs = jobs.filter(category=category)

    if max_budget:
        jobs = jobs.filter(budget__lte=max_budget)

    jobs = jobs.order_by("-created_at")

    return render(
        request,
        "jobs/browse_jobs.html",
        {
            "jobs": jobs,
            "query": query,
            "category": category,
            "max_budget": max_budget,
            "categories": Job.CATEGORY_CHOICES,
        },
    )
