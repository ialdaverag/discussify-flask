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


class TestCreateBlock(BaseTestCase):
    def test_create_block(self):
        # Create a user
        user = UserFactory()

        # Create a user to block
        user_to_block = UserFactory()

        # Create the block
        BlockManager.create(user, user_to_block)

        # Get the block relationship between user1 and user2
        block = Block.get_by_blocker_and_blocked(blocker=user, blocked=user_to_block)

        # Assert that the block relationship was created
        self.assertIsNotNone(block)

    def test_create_block_already_blocked(self):
        # Create a user
        user = UserFactory()

        # Create a user to block
        user_to_block = UserFactory()

        # Create a block relationship between user1 and user2
        Block(blocker=user, blocked=user_to_block).save()

        # Attempt to block user2 again
        with self.assertRaises(BlockError):
            BlockManager.create(user, user_to_block)

    def test_create_block_blocked_user(self):
        # Create a user
        user = UserFactory()

        # Attempt to block oneself
        with self.assertRaises(BlockError):
            BlockManager.create(user, user)
