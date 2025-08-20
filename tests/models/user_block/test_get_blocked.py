# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetBlockers(BasePaginationTest):
    def test_get_blockers(self):
        # Number of users to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Block the user
        for user_ in users:
            Block(blocker=user, blocked=user_).save()

        # Set the args
        args = {}

        # Get the blocked
        blocked = Block.get_blocked_with_args(user, args)

        # Assert that blocked is Pagination object
        self.assertIsInstance(blocked, Pagination)

        # Get the items
        blocked_items = blocked.items

        # Assert that blocked is a list
        self.assertIsInstance(blocked_items, list)

        # Assert the number of blocked
        self.assertEqual(len(blocked_items), n)

    def test_get_blocked_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the blocked
        blocked = Block.get_blocked_with_args(user, args)

        # Assert that blocked is Pagination object
        self.assertIsInstance(blocked, Pagination)

        # Get the items
        blocked_items = blocked.items

        # Assert that blocked is a list
        self.assertIsInstance(blocked_items, list)

        # Assert that the blocked is an empty list
        self.assertEqual(blocked_items, [])
