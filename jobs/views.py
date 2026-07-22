from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job

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
