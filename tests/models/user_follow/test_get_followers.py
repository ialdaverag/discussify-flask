# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class UserGetFollowers(BasePaginationTest):
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

        # Set args
        args = {}

        # Get the followers
        followers = Follow.get_followers(user, args)

        # Assert that followers ia a Pagination object
        self.assertIsInstance(followers, Pagination)

        # Get the items from the Pagination object
        followers_items = followers.items

        # Assert that followers is a list
        self.assertIsInstance(followers_items, list)

        # Assert the number of followers
        self.assertEqual(len(followers_items), n)

    def test_get_followers_empty(self):
        # Create a user
        user = UserFactory()

        # Set args
        args = {}

        # Get the followers
        followers = Follow.get_followers(user, args)

        # Assert that followers is a Pagination object
        self.assertIsInstance(followers, Pagination)

        # Get the items from the Pagination object
        followers_items = followers.items

        # Assert that the followers is not None
        self.assertIsInstance(followers_items, list)

        # Assert that the followers is an empty list
        self.assertEqual(followers_items, [])