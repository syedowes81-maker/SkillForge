from django.shortcuts import render
from .forms import RegistrationForm 

def register(request):
  form=RegistrationForm()
  return render(request,"register.html",{"form":form})

# Create your views here.
