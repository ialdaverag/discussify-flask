# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow


class UserGetFollowers(BaseTestCase):
    def test_get_followers(self):
        # Number of users to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Block the user
        for user_ in users:
            Follow(follower=user_, followed=user).save()

        # Get the followers
        followers = Follow.get_followers(user)

        # Assert that followers is a list
        self.assertIsInstance(followers, list)

        # Assert the number of followers
        self.assertEqual(len(followers), n)

    def test_get_followers_empty(self):
        # Create a user
        user = UserFactory()

        # Get the followers
        followers = Follow.get_followers(user)

        # Assert that the followers is not None
        self.assertIsInstance(followers, list)

        # Assert that the followers is an empty list
        self.assertEqual(followers, [])