from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
 list_display=(
  "username",
  "email",
  "phone_number",
  "can_freelance",
  "can_hire",
  "is_staff"
)
admin.site.register(User,CustomUserAdmin)

