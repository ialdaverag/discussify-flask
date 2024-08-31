# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# Managers
from app.managers.user import FollowManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


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

        # Set args
        args = {}

        # Read user followers
        followers_to_read = FollowManager.read_followers(user, args)

        # Assert that followers is a Pagination object
        self.assertIsInstance(followers_to_read, Pagination)

        # Get the items from the Pagination object
        followers_to_read_items = followers_to_read.items

        # Assert the number of followers
        self.assertEqual(len(followers_to_read_items), n)

        # Assert the followers are the same
        self.assertEqual(followers, followers_to_read_items)

    def test_read_followers_empty(self):
        # Create a user
        user = UserFactory()

        # Set args
        args = {}

        # Read user followers
        followers_to_read = FollowManager.read_followers(user, args)

        # Assert that followers is a Pagination object
        self.assertIsInstance(followers_to_read, Pagination)

        # Get the items from the Pagination object
        followers_to_read_items = followers_to_read.items

        # Assert the number of followers
        self.assertEqual(len(followers_to_read_items), 0)

        # Assert that the followers are an empty list
        self.assertEqual(followers_to_read_items, [])
