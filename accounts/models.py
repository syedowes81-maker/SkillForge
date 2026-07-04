from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
 phone_number = models.CharField(max_length=15,blank=True)
 can_freelance=models.BooleanField(default=False)
 can_hire=models.BooleanField(default=False)
