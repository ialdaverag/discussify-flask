# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block

# Managers
from app.managers.user import BlockManager

# Errors
from app.errors.errors import BlockError


class TestDeleteBlock(BaseTestCase):
    def test_delete_block(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # user1 blocks user2
        Block(blocker=user1, blocked=user2).save()

        # Delete the block relationship
        BlockManager.delete(user1, user2)

        # Get the block relationship between user1 and user2
        block = Block.get_by_blocker_and_blocked(blocker=user1, blocked=user2)

        # Assert that the block relationship was deleted
        self.assertIsNone(block)

    def test_delete_block_not_blocked(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Attempt to delete a block relationship that does not exist
        with self.assertRaises(BlockError):
            BlockManager.delete(user1, user2)


    def test_delete_block_blocked_self(self):
        # Create a user
        user1 = UserFactory()

        # Attempt to block self
        with self.assertRaises(BlockError):
            BlockManager.delete(user1, user1)
    