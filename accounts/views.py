from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import FreelancerProfile
from django.shortcuts import get_object_or_404
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

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
  return render(request,"accounts/dashboard.html")

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

    return render(
        request,
        "accounts/freelancer_detail.html",
        {
            "freelancer": freelancer,
        },
    )
