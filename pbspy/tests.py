from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from registration.models import RegistrationProfile
from unittest.mock import patch

from pbspy.forms import SpamProtectedRegistrationForm


class SpamProtectedRegistrationFormTests(TestCase):
    def form_data(self, **overrides):
        data = {
            "username": "new-user",
            "email": "new-user@example.com",
            "password1": "A-difficult-registration-password-123",
            "password2": "A-difficult-registration-password-123",
            "website": "",
            "invite_code": "secret-code",
        }
        data.update(overrides)
        return data

    @override_settings(REGISTRATION_INVITE_CODE="secret-code")
    def test_accepts_valid_registration(self):
        form = SpamProtectedRegistrationForm(data=self.form_data())

        self.assertTrue(form.is_valid(), form.errors)

    @override_settings(REGISTRATION_INVITE_CODE="secret-code")
    def test_rejects_filled_honeypot(self):
        form = SpamProtectedRegistrationForm(
            data=self.form_data(website="https://spam.example")
        )

        self.assertFalse(form.is_valid())
        self.assertIn("website", form.errors)

    @override_settings(REGISTRATION_INVITE_CODE="secret-code")
    def test_rejects_wrong_invite_code(self):
        form = SpamProtectedRegistrationForm(data=self.form_data(invite_code="wrong"))

        self.assertFalse(form.is_valid())
        self.assertIn("invite_code", form.errors)


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    REGISTRATION_INVITE_CODE="secret-code",
    STORAGES={
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class InviteOnlyRegistrationViewTests(TestCase):
    def setUp(self):
        super().setUp()
        patcher = patch("static_precompiler.settings.DISABLE_AUTO_COMPILE", True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def form_data(self, **overrides):
        data = {
            "username": "new-user",
            "email": "new-user@example.com",
            "password1": "A-difficult-registration-password-123",
            "password2": "A-difficult-registration-password-123",
            "website": "",
            "invite_code": "secret-code",
        }
        data.update(overrides)
        return data

    def test_registration_view_rejects_wrong_invite_without_email(self):
        response = self.client.post(
            reverse("registration_register"),
            self.form_data(invite_code="wrong"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_registration_view_creates_inactive_user_and_sends_activation_email(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("registration_register"),
                self.form_data(),
            )

        self.assertRedirects(response, reverse("registration_complete"))
        user = User.objects.get(username="new-user")
        self.assertFalse(user.is_active)
        self.assertEqual(RegistrationProfile.objects.filter(user=user).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        profile = RegistrationProfile.objects.get(user=user)
        self.assertIn(
            f"http://testserver/accounts/activate/{profile.activation_key}/",
            mail.outbox[0].body,
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_activation_activates_and_logs_in_user(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("registration_register"), self.form_data())

        user = User.objects.get(username="new-user")
        profile = RegistrationProfile.objects.get(user=user)

        response = self.client.get(
            reverse(
                "registration_activate",
                kwargs={"activation_key": profile.activation_key},
            )
        )

        user.refresh_from_db()
        self.assertRedirects(response, reverse("registration_activation_complete"))
        self.assertTrue(user.is_active)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

    @override_settings(REGISTRATION_INVITE_CODE=None)
    def test_rejects_registration_when_invite_code_is_not_configured(self):
        form = SpamProtectedRegistrationForm(data=self.form_data())

        self.assertFalse(form.is_valid())
        self.assertIn("invite_code", form.errors)
