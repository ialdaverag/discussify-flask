from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory

from app.errors.errors import FollowError

class TestFollow(BaseTestCase):
    def test_follow(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # Check initial state
        self.assertFalse(user1.is_following(user2))
        self.assertFalse(user2.is_followed_by(user1))

        # Perform the follow action
        user1.follow(user2)

        # Verify that the follow relationship was created
        self.assertTrue(user1.is_following(user2))
        self.assertTrue(user2.is_followed_by(user1))

        # Test following the same user again raises FollowError
        with self.assertRaises(FollowError):
            user1.follow(user2)

        # Test attempting to follow oneself raises FollowError
        with self.assertRaises(FollowError):
            user1.follow(user1)

        # Check if follower and following counts are updated
        self.assertEqual(user1.stats.following_count, 1)
        self.assertEqual(user2.stats.followers_count, 1)
