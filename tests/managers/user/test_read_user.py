# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Managers
from app.managers.user import UserManager

# Errors
from app.errors.errors import NotFoundError


class TestReadUser(BaseTestCase):
    def test_read_user(self):
        # Create a user
        user = UserFactory()

        # Read the user
        user_to_read = UserManager.read(user)

        # Check if the user is the same
        self.assertEqual(user, user_to_read)
