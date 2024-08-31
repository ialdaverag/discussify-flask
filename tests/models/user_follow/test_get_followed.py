# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


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

        # Set args
        args = {}

        # Get the followers
        followed = Follow.get_followed(user, args)

        # Assert that followed is a Paginated object
        self.assertIsInstance(followed, Pagination)

        # Get the items from the Paginated object
        followed_items = followed.items

        # Assert that followers is a list
        self.assertIsInstance(followed_items, list)

        # Assert the number of followers
        self.assertEqual(len(followed_items), n)

    def test_get_followed_empty(self):
        # Create a user
        user = UserFactory()

        # Set args
        args = {}

        # Get the followed
        followed = Follow.get_followed(user, args)

        # Assert that followed is a Paginated object
        self.assertIsInstance(followed, Pagination)

        # Get the items from the Paginated object
        followed_items = followed.items

        # Assert that the followed is not None
        self.assertIsInstance(followed_items, list)

        # Assert that the followed is an empty list
        self.assertEqual(followed_items, [])