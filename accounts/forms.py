from django import forms
from .models import user

class RegistrationForm(forms.ModelForm)
  class Meta:
    model=user
    field=[
      "username",
      "email",
    ]
