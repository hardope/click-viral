from django.test import TestCase

# Create your tests here.
from .models import Otp, Post


class OtpTestCase(TestCase):
    def setUp(self):
        Otp.objects.create(mail="nobody@example.com", username="nobody", otp="1234")
        Otp.objects.create(mail="nobody1@example.com", username="nobody1", otp="0234")

    def test_otp_creation(self):
        self.assertEqual(Otp.objects.count(), 2)

    def test_otp_mail(self):
        self.assertEqual(
            Otp.objects.get(mail="nobody@example.com").mail, "nobody@example.com"
        )
        self.assertEqual(
            Otp.objects.get(mail="nobody1@example.com").mail, "nobody1@example.com"
        )

    def test_otp_username(self):
        self.assertEqual(Otp.objects.get(username="nobody").username, "nobody")
        self.assertEqual(Otp.objects.get(username="nobody1").username, "nobody1")

    def test_tries_otp(self):
        self.assertEqual(Otp.objects.get(otp="1234").tries, 0)
        self.assertEqual(Otp.objects.get(otp="0234").tries, 0)
