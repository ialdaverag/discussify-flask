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


class TestCreateFollow(BaseTestCase):
    def test_create_follow(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Assert that user1 is not following user2
        self.assertFalse(user1.is_following(user2))

        # Asser that user2 is not followed by user1
        self.assertFalse(user2.is_followed_by(user1))

        # user1 follows user2
        FollowManager.create(user1, user2)

        # Assert that user1 is following user2
        self.assertTrue(user1.is_following(user2))

        # Assert that user2 is followed by user1
        self.assertTrue(user2.is_followed_by(user1))

        # Check if following count is updated
        self.assertEqual(user1.stats.following_count, 1)

        # Check if follower count is updated
        self.assertEqual(user2.stats.followers_count, 1)

    def test_create_follow_already_followed(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Create a follow relationship between user1 and user2
        Follow(follower=user1, followed=user2).save()

        # Attempt to follow user2 again
        with self.assertRaises(FollowError):
            FollowManager.create(user1, user2)

    def test_create_follow_self(self):
        # Create a user
        user = UserFactory()

        # Attempt to follow oneself
        with self.assertRaises(FollowError):
            FollowManager.create(user, user)
