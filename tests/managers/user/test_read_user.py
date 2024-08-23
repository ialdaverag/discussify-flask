# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Managers
from app.managers.user import UserManager

# Models
from app.models.user import Block

# Errors
from app.errors.errors import BlockError


class TestReadUser(BaseTestCase):
    def test_read_user_anonymous(self):
        # Create a user
        user = None

        # Authenticated user
        other = UserFactory()

        # Read the user
        user_to_read = UserManager.read(user, other)

        # Check if the user is the same
        self.assertEqual(other, user_to_read)

    def test_read_user(self):
        # Create a user
        user = UserFactory()

        # Authenticated user
        other = UserFactory()

        # Read the user
        user_to_read = UserManager.read(user, other)

        # Check if the user is the same
        self.assertEqual(other, user_to_read)

    def test_read_user_user_blocked_by_other(self):
        # Create a user
        user = UserFactory()

        # Create an owner
        other = UserFactory()

        # Block the user
        Block(blocker=other, blocked=user).save()

        # Read the user
        with self.assertRaises(BlockError):
            UserManager.read(user, other)

    def test_read_user_other_blocked_by_user(self):
        # Create a user
        user = UserFactory()

        # Create an owner
        other = UserFactory()

        # Block the owner
        Block(blocker=user, blocked=other).save()

        # Read the user
        with self.assertRaises(BlockError):
            UserManager.read(user, other)
