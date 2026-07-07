from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
 phone_number = models.CharField(max_length=15,blank=True)
 can_freelance=models.BooleanField(default=False)
 can_hire=models.BooleanField(default=False)

class FreelancerProfile(models.Model):
 user=models.OneToOneField(
  User,
  on_delete=models.CASCADE
)

 skills=models.CharField(max_length=255,default=0)
 bio=models.TextField(default=0)
 experience=models.IntegerField(default="")
 hourly_rate=models.IntegerField(default="")
 portfolio=models.URLField(blank=True)

 def __str__(self):
   return self.user.username
