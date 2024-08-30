# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User


class TestIsUsernameAvailable(BaseTestCase):
    def test_is_username_available_true(self):
        # Create a username
        username = 'user1'

        # Check if the username is available
        is_username_available = User.is_username_available(username)

        # Check that the username is not available
        self.assertTrue(is_username_available)

    def test_is_username_available_false(self):
        # Create a user
        user = UserFactory()

        # Get the username of the user
        username = user.username

        # Check if the username is available
        is_username_available = User.is_username_available(username)

        # Check that the username is not available
        self.assertFalse(is_username_available)
