from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory

from app.errors.errors import FollowError


class TestUnfollow(BaseTestCase):
    def test_unfollow(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # User1 follows user2
        user1.follow(user2)

        # Check initial state
        self.assertTrue(user1.is_following(user2))
        self.assertTrue(user2.is_followed_by(user1))

        # Perform the unfollow action
        user1.unfollow(user2)

        # Verify that the follow relationship was removed
        self.assertFalse(user1.is_following(user2))
        self.assertFalse(user2.is_followed_by(user1))

        # Test unfollowing the same user again raises FollowError
        with self.assertRaises(FollowError):
            user1.unfollow(user2)

        # Test attempting to unfollow oneself raises FollowError
        with self.assertRaises(FollowError):
            user1.unfollow(user1)

        # Check if follower and following counts are updated
        self.assertEqual(user1.stats.following_count, 0)
        self.assertEqual(user2.stats.followers_count, 0)
