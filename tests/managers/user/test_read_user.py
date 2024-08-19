# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User

# Managers
from app.managers.user import UserManager

# Errors
from app.errors.errors import NotFoundError


class TestReadUser(BaseTestCase):
    def test_read_user(self):
        # Create a user
        user = UserFactory()

        # Read the user
        user_to_read = UserManager.read(user.username)

        # Check if the user is the same
        self.assertEqual(user, user_to_read)

    def test_read_user_not_found(self):
        # Attempt to read a user that does not exist
        with self.assertRaises(NotFoundError):
            UserManager.read('username')
