# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

class UserGetByFollowerAndFollowed(BaseTestCase):
    def test_get_by_follower_and_followed(self):
        # Create a user
        user = UserFactory()

        # Create another user  
        user2 = UserFactory()

        # Create a follow
        Follow(follower=user, followed=user2).save()

        # Get the follow by follower and followed
        relationship = Follow.get_by_follower_and_followed(user, user2)

        # Assert that the follow is the same as the follow by follower and followed
        self.assertIsNotNone(relationship)

    def test_get_by_follower_and_followed_no_follow(self):
        # Create a user
        user = UserFactory()

        # Create another user  
        user2 = UserFactory()

        # Get the follow by follower and followed
        follow_by_follower_and_followed = Follow.get_by_follower_and_followed(user, user2)

        # Assert that the follow by follower and followed is None
        self.assertIsNone(follow_by_follower_and_followed)