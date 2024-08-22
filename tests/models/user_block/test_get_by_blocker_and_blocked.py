# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block


class TestGetByBlockerAndBlocked(BaseTestCase):
    def test_get_by_blocker_and_blocked(self):
        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Block the user
        Block(blocker=user1, blocked=user2).save()

        # Get the block
        block_to_get = Block.get_by_blocker_and_blocked(user1, blocked=user2)

        # Assert that the block is not None
        self.assertIsNotNone(block_to_get)

    def test_get_by_blocker_and_blocked_no_block(self):
        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Get the block
        block_to_get = Block.get_by_blocker_and_blocked(user1, user2)

        # Assert that the block is None
        self.assertIsNone(block_to_get)

    