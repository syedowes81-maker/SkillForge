from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import JobForm


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
