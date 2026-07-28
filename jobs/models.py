from django.db import models
from django.conf import settings

class Job(models.Model):
    client=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    CATEGORY_CHOICES = [
        ("Web Development", "Web Development"),
        ("Python", "Python"),
        ("Java", "Java"),
        ("Data Science", "Data Science"),
        ("Design", "Design"),
        ("Other", "Other"),
    ]

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="Other"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def _str_(self):
        return f"{self.freelancer.username} -> {self.job.title}"

class SavedJob(models.Model):
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("freelancer", "job")

    def _str_(self):
        return f"{self.freelancer.username} saved {self.job.title}"
