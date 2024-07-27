from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory


class TestIsFollowedBy(BaseTestCase):
    def test_is_followed_by(self):
        # Create test users
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        user3 = UserFactory.create()

        # Make user2 follow user1
        user2.follow(user1)

        # Test that user1 is followed by user2
        self.assertTrue(user1.is_followed_by(user2))

        # Test that user1 is not followed by user3
        self.assertFalse(user1.is_followed_by(user3))

        # Test that user2 is not followed by user1
        self.assertFalse(user2.is_followed_by(user1))
