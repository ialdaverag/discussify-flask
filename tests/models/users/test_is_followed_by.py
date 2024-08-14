# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow


class TestIsFollowedBy(BaseTestCase):
    def test_is_followed_by_true(self):
        # Create three users
        user1 = UserFactory()
        user2 = UserFactory()

        # Append user2 as a follower of user1
        Follow(follower=user1, followed=user2).save()

        # Test that user2 is followed by user1
        self.assertTrue(user2.is_followed_by(user1))

    def test_is_followed_by_false(self):
        # Create three users
        user1 = UserFactory()
        user2 = UserFactory()

        # Test that user2 is not followed by user1
        self.assertFalse(user2.is_followed_by(user1))
 