# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow


class UserGetFollowed(BaseTestCase):
    def test_get_followed(self):
        # Number of users to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Block the user
        for user_ in users:
            Follow(follower=user, followed=user_).save()

        # Get the followers
        followed = Follow.get_followed(user)

        # Assert that followers is a list
        self.assertIsInstance(followed, list)

        # Assert the number of followers
        self.assertEqual(len(followed), n)

    def test_get_followed_empty(self):
        # Create a user
        user = UserFactory()

        # Get the followed
        followed = Follow.get_followed(user)

        # Assert that the followed is not None
        self.assertIsInstance(followed, list)

        # Assert that the followed is an empty list
        self.assertEqual(followed, [])