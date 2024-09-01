# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block

# Managers
from app.managers.user import BlockManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadBlocked(BaseTestCase):
    def test_read_blocked(self):
        # Number of users to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Block the users
        for user_ in users:
            Block(blocker=user, blocked=user_).save()

        # Set args
        args = {}

        # Read user blocked
        blocked_to_read = BlockManager.read_blocked(user, args)

        # Assert blocked_to_read is a Paginated object
        self.assertIsInstance(blocked_to_read, Pagination)

        # Get the items from the Paginated object
        blocked_to_read_items = blocked_to_read.items

        # Assert the number of blocked
        self.assertEqual(len(blocked_to_read_items), n) 

        # Assert the blocked are the same
        self.assertEqual(users, blocked_to_read_items)

    def test_read_blocked_empty(self):
        # Create a user
        user = UserFactory()

        # Set args
        args = {}

        # Read user blocked
        blocked_to_read = BlockManager.read_blocked(user, args)

        # Assert blocked_to_read is a Paginated object
        self.assertIsInstance(blocked_to_read, Pagination)

        # Get the items from the Paginated object
        blocked_to_read_items = blocked_to_read.items

        # Assert the number of blocked
        self.assertEqual(len(blocked_to_read_items), 0)

        # Assert that the blocked are an empty list
        self.assertEqual(blocked_to_read_items, [])
