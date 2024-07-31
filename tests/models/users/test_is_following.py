from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory


class TestFollow(BaseTestCase):
    def test_is_following_true(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # Append user2 as a follower of user1
        user2.append_follower(user1)

        # Test that user1 is following user2
        self.assertTrue(user1.is_following(user2))

    def test_is_following_false(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # Test that user1 is not following user2
        self.assertFalse(user1.is_following(user2))
