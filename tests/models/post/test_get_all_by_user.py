# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post


class TestGetAllByUser(BaseTestCase):
    def test_get_all_by_user(self):
        # Create a user
        user = UserFactory()

        # Number of posts to create
        n = 5

        # Create a post
        PostFactory.create_batch(n, owner=user)

        # Get all posts by the user
        posts_by_user = Post.get_all_by_user(user)

        # Assert the number of posts
        self.assertEqual(len(posts_by_user), n)

    def test_get_all_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Get all posts by the user
        posts_by_user = Post.get_all_by_user(user)

        # Assert that posts_by_user is an empty list
        self.assertEqual(posts_by_user, [])
