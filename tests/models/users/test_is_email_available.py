# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User


class TestIsEmailAvailable(BaseTestCase):
    def test_is_email_available_true(self):
        # Create an email
        email = 'user@email.com'

        # Check that the email is not available
        self.assertTrue(User.is_email_available(email))

    def test_is_email_available_false(self):
        # Create a user
        user = UserFactory()

        # Get the email of the user
        email = user.email

        # Check that the email is not available
        self.assertFalse(User.is_email_available(email))