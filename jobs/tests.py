from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Job


User = get_user_model()


class JobModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testclient",
            password="testpass123"
        )

    def test_job_creation(self):
        job = Job.objects.create(
            client=self.user,
            category="Python",
            title="Python Developer",
            description="Need a Python developer",
            budget=10000,
            location="Bangalore"
        )

        self.assertEqual(job.title, "Python Developer")
        self.assertEqual(job.category, "Python")
        self.assertEqual(job.budget, 10000)
        self.assertEqual(job.location, "Bangalore")
        self.assertEqual(job.client, self.user)
