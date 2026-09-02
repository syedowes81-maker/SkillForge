from django import forms
from .models import User, FreelancerProfile, Review


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )


class FreelancerProfileForm(forms.ModelForm):

    class Meta:
        model = FreelancerProfile
        fields = [
            "skills",
            "bio",
            "experience",
            "hourly_rate",
            "location",
            "portfolio",
            "profile_picture",
            "resume",
        ]

    def clean_experience(self):

        experience = self.cleaned_data.get("experience")

        if experience is not None and experience > 50:
            raise forms.ValidationError(
                "Experience cannot be more than 50 years."
            )

        return experience

    def clean_hourly_rate(self):

        hourly_rate = self.cleaned_data.get("hourly_rate")

        if hourly_rate is not None and hourly_rate < 0:
            raise forms.ValidationError(
                "Hourly rate cannot be negative."
            )

        return hourly_rate

    def clean_skills(self):

        skills = self.cleaned_data.get(
            "skills",
            ""
        ).strip()

        if len(skills) > 255:
            raise forms.ValidationError(
                "Skills must be 255 characters or fewer."
            )

        return skills


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            "rating",
            "comment",
        ]
