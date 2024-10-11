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

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadUser(BaseTestCase):
    def test_read_users(self):
        # Number of users to create
        n = 5

        # Create a user
        users = UserFactory.create_batch(n)

        # Set args
        args = {}

        # Read the user
        users_to_read = UserManager.read_all(None, args)

        # Assert users is a Paginated object
        self.assertIsInstance(users_to_read, Pagination)

        # Get the items from the Paginated object
        users_to_read_items = users_to_read.items

        # Assert that users_to_read_items is a list
        self.assertIsInstance(users_to_read_items, list)

        # Assert that the users are the same as the all users
        self.assertCountEqual(users, users_to_read_items)

    def test_read_users_empty(self):
        # Set args
        args = {}

        # Read the user
        users_to_read = UserManager.read_all(None, args)

        # Assert users is a Paginated object
        self.assertIsInstance(users_to_read, Pagination)

        # Get the items from the Paginated object
        users_to_read_items = users_to_read.items

        # Assert that users_to_read_items is a list
        self.assertIsInstance(users_to_read_items, list)

        # Assert that users_to_read_items is empty
        self.assertEqual(users_to_read_items, [])