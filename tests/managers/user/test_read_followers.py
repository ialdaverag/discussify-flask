# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# Managers
from app.managers.user import FollowManager


class TestReadFollowers(BaseTestCase):
    def test_read_followers(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Read user followers
        followers_to_read = FollowManager.read_followers(user)

        # Assert the number of followers
        self.assertEqual(len(followers_to_read), n)

        # Assert the followers are the same
        self.assertEqual(followers, followers_to_read)

    def test_read_followers_empty(self):
        # Create a user
        user = UserFactory()

        # Read user followers
        followers_to_read = FollowManager.read_followers(user)

        # Assert the number of followers
        self.assertEqual(len(followers_to_read), 0)

        # Assert that the followers are an empty list
        self.assertEqual(followers_to_read, [])
