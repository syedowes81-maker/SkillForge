from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,FreelancerProfile

class CustomUserAdmin(UserAdmin):
 list_display=(
  "username",
  "email",
  "phone_number",
  "can_freelance",
  "can_hire",
  "is_staff"
)

class FreelancerProfileAdmin(admin.ModelAdmin):
  list_display=(
    "user",
    "skills",
    "experience",
    "hourly_rate",
   )
admin.site.register(User,CustomUserAdmin)
admin.site.register(FreelancerProfile,FreelancerProfileAdmin)
