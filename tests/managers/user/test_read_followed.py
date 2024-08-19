# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# Managers
from app.managers.user import FollowManager


class TestReadFollowed(BaseTestCase):
    def test_read_followed(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the user follow the followers
        for follower in followers:
            Follow(follower=user, followed=follower).save()

        # Read user followers
        followers_to_read = FollowManager.read_followed(user)

        # Assert the number of followers
        self.assertEqual(len(followers_to_read), n)

        # Assert the followers are the same
        self.assertEqual(followers, followers_to_read)

    def test_read_followed_empty(self):
        # Create a user
        user = UserFactory()

        # Read user followers
        followers_to_read = FollowManager.read_followed(user)

        # Assert the number of followers
        self.assertEqual(len(followers_to_read), 0)

        # Assert that the followers are an empty list
        self.assertEqual(followers_to_read, [])