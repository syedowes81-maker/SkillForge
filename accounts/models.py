from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
class User(AbstractUser):
 phone_number = models.CharField(max_length=15,blank=True)
 can_freelance=models.BooleanField(default=False)
 can_hire=models.BooleanField(default=False)

class FreelancerProfile(models.Model):
 user=models.OneToOneField(
  User,
  on_delete=models.CASCADE
)

 skills=models.CharField(max_length=255,blank=True)
 bio=models.TextField(blank=True)
 experience=models.PositiveIntegerField(default=0)
 hourly_rate=models.DecimalField(max_digits=8,decimal_places=2,default=0)
 location=models.CharField(max_length=100,blank=True)
 profile_picture=models.ImageField(upload_to="profiles/",blank=True,null=True)
 resume = models.FileField(
     upload_to="resumes/",
     blank=True,
     null=True
)
 portfolio=models.URLField(blank=True)

 def __str__(self):
   return self.user.username

class Review(models.Model):
    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ]
)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} -> {self.freelancer.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def _str_(self):
        return self.message
