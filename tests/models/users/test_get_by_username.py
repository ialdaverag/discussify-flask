# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User

# Errors
from app.errors.errors import NotFoundError


class TestGetByUsername(BaseTestCase):
    def test_get_by_username(self):
        # Create a user
        user = UserFactory()

        # Get the user by username
        user_by_username = User.get_by_username(user.username)

        # Assert that the user is the same as the user by username
        self.assertEqual(user, user_by_username)

    def test_get_by_username_nonexistent(self):
        # Attempt to get a user by username
        with self.assertRaises(NotFoundError):
            User.get_by_username('username')