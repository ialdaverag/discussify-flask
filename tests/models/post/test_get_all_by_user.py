# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetAllByUser(BaseTestCase):
    def test_get_all_by_user(self):
        # Create a user
        user = UserFactory()

        # Number of posts to create
        n = 5

        # Create a post
        PostFactory.create_batch(n, owner=user)

        # Set the args
        args = {}

        # Get all posts by the user
        posts_by_user = Post.get_all_by_user(user, args)

        # Assert posts_by_user is a Pagination object
        self.assertIsInstance(posts_by_user, Pagination)

        # Get the items
        posts_by_user_items = posts_by_user.items

        # Assert the number of posts
        self.assertEqual(len(posts_by_user_items), n)

    def test_get_all_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get all posts by the user
        posts_by_user = Post.get_all_by_user(user, args)

        # Assert posts_by_user is a Pagination object
        self.assertIsInstance(posts_by_user, Pagination)

        # Get the items
        posts_by_user_items = posts_by_user.items

        # Assert that posts_by_user is an empty list
        self.assertEqual(len(posts_by_user_items), 0)
