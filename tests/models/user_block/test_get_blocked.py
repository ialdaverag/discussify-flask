# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block


class TestGetBlockers(BaseTestCase):
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

        # Get the blocked
        blocked = Block.get_blocked(user)

        # Assert that blocked is a list
        self.assertIsInstance(blocked, list)

        # Assert the number of blocked
        self.assertEqual(len(blocked), n)

    def test_get_blocked_empty(self):
        # Create a user
        user = UserFactory()

        # Get the blocked
        blocked = Block.get_blocked(user)

        # Assert that blocked is a list
        self.assertIsInstance(blocked, list)

        # Assert that the blocked is an empty list
        self.assertEqual(blocked, [])
