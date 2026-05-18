from django.test import TestCase, override_settings

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

    @override_settings(REGISTRATION_INVITE_CODE=None)
    def test_rejects_registration_when_invite_code_is_not_configured(self):
        form = SpamProtectedRegistrationForm(data=self.form_data())

        self.assertFalse(form.is_valid())
        self.assertIn("invite_code", form.errors)
