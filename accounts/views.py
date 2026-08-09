from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import FreelancerProfile
from django.shortcuts import get_object_or_404
from .forms import FreelancerProfileForm
from django.contrib.auth.decorators import login_required
from .models import FreelancerProfile, Review, Message
from .forms import FreelancerProfileForm, ReviewForm
from django.db.models import Avg
from .models import FreelancerProfile, Review, Notification
from jobs.models import Job,Application
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            FreelancerProfile.objects.create(user=user)

            return redirect("login")

    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("/dashboard/")

        return render(request, "accounts/login.html", {"form": form})

    form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

@login_required
def dashboard(request):
    jobs_posted = Job.objects.filter(
        client=request.user
    ).count()

    applications_received = Application.objects.filter(
        job__client=request.user
    ).count()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "jobs_posted": jobs_posted,
            "applications_received": applications_received,
        },
    )

def logout_view(request):
  logout(request)
  return redirect("/login/")

def home(request):
 return render(request,"accounts/home.html")

@login_required
def profile(request):
  profile=request.user.freelancerprofile
  return render(request,"accounts/profile.html",{"profile":profile})

def freelancers(request):

    query = request.GET.get("q")

    freelancers = FreelancerProfile.objects.all()

    if query:
        freelancers = freelancers.filter(skills__icontains=query)

    return render(
        request,
        "accounts/freelancers.html",
        {
            "freelancers": freelancers,
            "query": query,
        }
    )

def freelancer_detail(request, id):
    freelancer = get_object_or_404(FreelancerProfile, id=id)

    reviews = Review.objects.filter(
        freelancer=freelancer
    ).order_by("-created_at")
    average_rating = reviews.aggregate(
    Avg("rating")
)["rating__avg"]
    return render(
        request,
        "accounts/freelancer_detail.html",
        {
            "freelancer": freelancer,
            "reviews": reviews,
            "average_rating":average_rating,
        },
    )
@login_required
def edit_profile(request):
    profile = request.user.freelancerprofile

    if request.method == "POST":
        form = FreelancerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {
        "form": form
    })

@login_required
def add_review(request, id):
    freelancer = get_object_or_404(FreelancerProfile, id=id)

    existing_review = Review.objects.filter(
        freelancer=freelancer,
        client=request.user
    ).first()

    if existing_review:
        return redirect("freelancer_detail", id=freelancer.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.freelancer = freelancer
            review.client = request.user
            review.save()

            return redirect("freelancer_detail", id=freelancer.id)

    else:
        form = ReviewForm()

    return render(
        request,
        "accounts/add_review.html",
        {
            "form": form,
            "freelancer": freelancer,
        },
    )
@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/notifications.html",
        {
            "notifications": notifications
        }
    )
@login_required
def send_message(request, id):
    receiver = get_object_or_404(User, id=id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )

        return redirect("messages")

    return render(
        request,
        "accounts/send_message.html",
        {
            "receiver": receiver,
        }
    )

@login_required
def messages_view(request):
    messages = Message.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/messages.html",
        {
            "messages": messages,
        },
    )
