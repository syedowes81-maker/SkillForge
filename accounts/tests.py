from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import FreelancerProfile, Review, Notification
from jobs.models import Job, Application


User = get_user_model()


class FreelancerReviewTests(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="reviewclient",
            password="TestPass123!"
        )

        self.freelancer_user = User.objects.create_user(
            username="reviewfreelancer",
            password="TestPass123!"
        )

        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.freelancer_user,
            skills="Python, Django",
            bio="Test freelancer",
            experience=2,
            hourly_rate=500
        )

        self.job = Job.objects.create(
            client=self.client_user,
            category="Python",
            title="Python Developer",
            description="Need a Python developer",
            budget=10000,
            location="Bangalore"
        )

        self.application = Application.objects.create(
            job=self.job,
            freelancer=self.freelancer_user,
            cover_letter="I am interested in this project.",
            status="Confirmed"
        )

        self.detail_url = reverse(
            "freelancer_detail",
            kwargs={"id": self.freelancer_profile.id}
        )

        self.review_url = reverse(
            "add_review",
            kwargs={"id": self.freelancer_profile.id}
        )

    def test_confirmed_client_can_see_review_form(self):
        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["can_review"])

    def test_unconfirmed_client_cannot_see_review_form(self):
        self.application.status = "Pending"
        self.application.save()

        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["can_review"])

    def test_valid_review_is_saved(self):
        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        response = self.client.post(
            self.review_url,
            {
                "rating": 5,
                "comment": "Excellent work!"
            }
        )

        self.assertRedirects(response, self.detail_url)
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.get()

        self.assertEqual(review.client, self.client_user)
        self.assertEqual(review.freelancer, self.freelancer_profile)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent work!")

    def test_freelancer_receives_notification(self):
        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        self.client.post(
            self.review_url,
            {
                "rating": 5,
                "comment": "Excellent work!"
            }
        )

        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.objects.get()

        self.assertEqual(notification.user, self.freelancer_user)
        self.assertIn("5-star review", notification.message)

    def test_duplicate_review_is_rejected(self):
        Review.objects.create(
            client=self.client_user,
            freelancer=self.freelancer_profile,
            rating=4,
            comment="Previous review"
        )

        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        self.client.post(
            self.review_url,
            {
                "rating": 5,
                "comment": "Trying again"
            }
        )

        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 0)

    def test_unconfirmed_client_cannot_submit_review(self):
        self.application.status = "Pending"
        self.application.save()

        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        response = self.client.post(
            self.review_url,
            {
                "rating": 5,
                "comment": "Trying to review"
            }
        )

        self.assertRedirects(response, self.detail_url)
        self.assertEqual(Review.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_get_request_to_review_endpoint_returns_405(self):
        self.client.login(
            username="reviewclient",
            password="TestPass123!"
        )

        response = self.client.get(self.review_url)

        self.assertEqual(response.status_code, 405)

    def test_unauthenticated_user_cannot_submit_review(self):
        response = self.client.post(
            self.review_url,
            {
                "rating": 5,
                "comment": "Unauthenticated review"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)


