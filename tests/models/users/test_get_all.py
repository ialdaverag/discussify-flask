# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User


class TestGetAll(BaseTestCase):
    def test_get_all(self):
        # Create users
        users = UserFactory.create_batch(5)

        # Get all users
        all_users = User.get_all()

        # Assert that the users are the same as the all users
        self.assertEqual(users, all_users)

    def test_get_all_empty(self):
        # Get all users
        all_users = User.get_all()

        # Assert that the all users is an empty list
        self.assertEqual(all_users, [])
