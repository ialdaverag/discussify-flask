# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetAll(BasePaginationTest):
    def test_get_all(self):
        # Number of users
        n = 5
        
        # Create users
        users = UserFactory.create_batch(n)

        # Set args
        args = {}

        # Get all users
        all_users = User.get_all(args=args)

        # Assert all_users is a Paginated object
        self.assertIsInstance(all_users, Pagination)

        # Get the items from the Paginated object
        all_users_items = all_users.items

        # Assert that all_users_items is a list
        self.assertIsInstance(all_users_items, list)

        # Assert that the users are the same as the all users
        self.assertCountEqual(users, all_users_items)

    def test_get_all_empty(self):
        # Set args
        args = {}

        # Get all users
        all_users = User.get_all(args=args)

        # Assert all_users is a Paginated object
        self.assertIsInstance(all_users, Pagination)

        # Get the items from the Paginated object
        all_users_items = all_users.items

        # Assert that all_users_items is a list
        self.assertIsInstance(all_users_items, list)

        # Assert that all_users_items is empty
        self.assertEqual(all_users_items, [])
