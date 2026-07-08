from django import forms
from .models import user

class RegistrationForm(forms.ModelForm):
  password=forms.CharField(widget=forms.PasswordInput)
  confirm_password=forms.CharField(widget=forms.PasswordInput)
  class Meta:
    model=user
    field=[
      "username",
      "email",
    ]
    def clean(self):
     cleaned_data=super().clean()
     password=cleaned_data.get("password")
     confirm_password=cleaned_data.get("confirm_password")
     if password !=confirm_password:
       raise forms.validateError("Passwords do not match.")
       return cleaned_data
