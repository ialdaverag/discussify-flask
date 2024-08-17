# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# Managers
from app.managers.user import FollowManager

# Errors
from app.errors.errors import FollowError


class TestDeleteFollow(BaseTestCase):
    def test_delete_follow(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # user1 follows user2
        FollowManager.create(user1, user2)

        # Assert that user1 is following user2
        self.assertTrue(user1.is_following(user2))

        # Asser that user2 is followed by user1
        self.assertTrue(user2.is_followed_by(user1))

        # Check if following count is updated
        self.assertEqual(user1.stats.following_count, 1)

        # Check if follower count is updated
        self.assertEqual(user2.stats.followers_count, 1)

        # user1 unfollows user2
        FollowManager.delete(user1, user2)

        # Assert that user1 is not following user2
        self.assertFalse(user1.is_following(user2))

        # Assert that user2 is not followed by user1
        self.assertFalse(user2.is_followed_by(user1))

        # Check if following count is updated
        self.assertEqual(user1.stats.following_count, 0)

        # Check if follower count is updated
        self.assertEqual(user2.stats.followers_count, 0)

    def test_delete_follow_not_followed(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Attempt to unfollow user2
        with self.assertRaises(FollowError):
            FollowManager.delete(user1, user2)

    def test_delete_follow_self(self):
        # Create a user
        user1 = UserFactory()

        # Attempt to unfollow self
        with self.assertRaises(FollowError):
            FollowManager.delete(user1, user1)
