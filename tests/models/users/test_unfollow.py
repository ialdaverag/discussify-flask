from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory

from app.errors.errors import FollowError


class TestUnfollow(BaseTestCase):
    def test_unfollow(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # user1 follows user2
        user1.follow(user2)

        # Assert that user1 is following user2
        self.assertTrue(user1.is_following(user2))

        # Assert that user2 is followed by user1
        self.assertTrue(user2.is_followed_by(user1))

        # user1 unfollows user2
        user1.unfollow(user2)

        # Verify that user1 is not following user2
        self.assertFalse(user1.is_following(user2))

        # Verify that user2 is not followed by user1
        self.assertFalse(user2.is_followed_by(user1))

        # Check if following count is updated
        self.assertEqual(user1.stats.following_count, 0)

        # Check if follower count is updated
        self.assertEqual(user2.stats.followers_count, 0)

    def test_unfollow_not_followed(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Attempt to unfollow user2 without following
        with self.assertRaises(FollowError):
            user1.unfollow(user2)

    def test_unfollow_self(self):
        # Create a user
        user = UserFactory()

        # Attempt to unfollow oneself
        with self.assertRaises(FollowError):
            user.unfollow(user)
