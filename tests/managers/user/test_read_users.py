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
    def test_read_users(self):
        # Number of users to create
        n = 5

        # Create a user
        users = UserFactory.create_batch(n)

        # Read the user
        users_to_read = UserManager.read_all()

        # Assert the number of users
        self.assertEqual(len(users_to_read), n)

        # Assert that the users are the same as the all users
        self.assertEqual(users, users_to_read)

    def test_read_users_empty(self):
        # Read the user
        users_to_read = UserManager.read_all()

        # Assert the number of users
        self.assertEqual(len(users_to_read), 0)

        # Assert that the all users is an empty list
        self.assertEqual(users_to_read, [])