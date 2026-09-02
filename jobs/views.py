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
from django.core.paginator import Paginator

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

    # Closed jobs cannot receive applications
    if job.status == "Closed":
        return redirect("job_detail", id=job.id)

    # Prevent the client from applying to their own job
    if job.client == request.user:
        return redirect("job_detail", id=job.id)

    # Prevent duplicate applications
    if Application.objects.filter(
        job=job,
        freelancer=request.user
    ).exists():
        return redirect("my_applications")

    if request.method == "POST":

        cover_letter = request.POST.get("cover_letter")

        if cover_letter:
            Application.objects.create(
                job=job,
                freelancer=request.user,
                cover_letter=cover_letter
            )

            return redirect("my_applications")

    return render(
        request,
        "jobs/apply_job.html",
        {
            "job": job
        }
    )


@login_required
def my_applications(request):

    status = request.GET.get("status")

    all_applications = Application.objects.filter(
        freelancer=request.user
    )

    applications = all_applications.order_by("-applied_at")

    if status in ["Pending", "Accepted", "Rejected"]:
        applications = applications.filter(status=status)

    total_applications = all_applications.count()

    pending_applications = all_applications.filter(
        status="Pending"
    ).count()

    accepted_applications = all_applications.filter(
        status="Accepted"
    ).count()

    rejected_applications = all_applications.filter(
        status="Rejected"
    ).count()

    return render(
        request,
        "jobs/my_applications.html",
        {
            "applications": applications,
            "status": status,
            "total_applications": total_applications,
            "pending_applications": pending_applications,
            "accepted_applications": accepted_applications,
            "rejected_applications": rejected_applications,
        }
    )

@login_required
def my_work(request):

    accepted_applications = Application.objects.filter(
        freelancer=request.user,
        status="Accepted"
    ).select_related("job").order_by("-applied_at")

    return render(
        request,
        "jobs/my_work.html",
        {
            "accepted_applications": accepted_applications,
        }
    )




@login_required
def withdraw_application(request, id):

    application = Application.objects.get(id=id)

    # Only the freelancer who submitted it can withdraw it
    if application.freelancer != request.user:
        return redirect("my_applications")

    # Only pending applications can be withdrawn
    if application.status == "Pending":
        application.delete()

    return redirect("my_applications")

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
    job = application.job

    if job.client != request.user:
        return redirect("browse_jobs")

    if request.method != "POST":
        return redirect("view_applicants", id=job.id)

    if application.status != "Pending":
        return redirect("view_applicants", id=job.id)

    # Keep the rest of your existing Accepted/Rejected logic here.
    if status == "Accepted":

        # Accept this applicant
        application.status = "Accepted"
        application.save()

        Notification.objects.create(
            user=application.freelancer,
            message=f"Your application for '{job.title}' was Accepted."
        )

        # Reject all other pending applicants
        other_applications = Application.objects.filter(
            job=job,
            status="Pending"
        ).exclude(id=application.id)

        for other_application in other_applications:

            other_application.status = "Rejected"
            other_application.save()

            Notification.objects.create(
                user=other_application.freelancer,
                message=f"Your application for '{job.title}' was Rejected because another applicant was selected."
            )

        # Close the job because a freelancer has been hired
        job.status = "Closed"
        job.save()

    elif status == "Rejected":

        application.status = "Rejected"
        application.save()

        Notification.objects.create(
            user=application.freelancer,
            message=f"Your application for '{job.title}' was Rejected."
        )

    return redirect("view_applicants", id=job.id)


@login_required
def my_jobs(request):

    query = request.GET.get("q")
    status = request.GET.get("status")

    jobs = Job.objects.filter(
        client=request.user
    ).order_by("-created_at")

    # Search by title
    if query:
        jobs = jobs.filter(
            title__icontains=query
        )

    # Filter by status
    if status in ["Open", "Closed"]:
        jobs = jobs.filter(
            status=status
        )

    total_jobs = Job.objects.filter(
        client=request.user
    ).count()

    open_jobs = Job.objects.filter(
        client=request.user,
        status="Open"
    ).count()

    closed_jobs = Job.objects.filter(
        client=request.user,
        status="Closed"
    ).count()

    total_applications = Application.objects.filter(
        job__client=request.user
    ).count()

    return render(
        request,
        "jobs/my_jobs.html",
        {
            "jobs": jobs,
            "query": query,
            "status": status,
            "total_jobs": total_jobs,
            "open_jobs": open_jobs,
            "closed_jobs": closed_jobs,
            "total_applications": total_applications,
        }
    )
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
def toggle_job_status(request, id):
    job = Job.objects.get(id=id)

    if job.client != request.user:
        return redirect("my_jobs")

    if request.method == "POST":
        if job.status == "Open":
            job.status = "Closed"
        else:
            job.status = "Open"

        job.save()

    return redirect("my_jobs")
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
    min_budget = request.GET.get("min_budget")
    max_budget = request.GET.get("max_budget")
    sort = request.GET.get("sort", "newest")

    jobs = Job.objects.all()

    # Search by job title
    if query:
        jobs = jobs.filter(title__icontains=query)

    # Filter by category
    if category:
        jobs = jobs.filter(category=category)

    # Filter by minimum budget
    if min_budget:
        jobs = jobs.filter(budget__gte=min_budget)

    # Filter by maximum budget
    if max_budget:
        jobs = jobs.filter(budget__lte=max_budget)

    # Sorting
    if sort == "budget_low":
        jobs = jobs.order_by("budget")
    elif sort == "budget_high":
        jobs = jobs.order_by("-budget")
    else:
        jobs = jobs.order_by("-created_at")

    # Pagination
    paginator = Paginator(jobs, 5)

    page_number = request.GET.get("page")
    jobs_page = paginator.get_page(page_number)

    return render(
        request,
        "jobs/browse_jobs.html",
        {
            "jobs": jobs_page,
            "query": query,
            "category": category,
            "min_budget": min_budget,
            "max_budget": max_budget,
            "sort": sort,
            "categories": Job.CATEGORY_CHOICES,
        },
    )

@login_required
def withdraw_application(request, id):

    application = Application.objects.get(id=id)

    # Only the freelancer who submitted the application
    # can withdraw it
    if application.freelancer != request.user:
        return redirect("my_applications")

    # Only pending applications can be withdrawn
    if application.status == "Pending":
        application.delete()

    return redirect("my_applications")
