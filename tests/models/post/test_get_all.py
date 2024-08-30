# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post


class TestGetAll(BaseTestCase):
    def test_get_all(self):
        # Number of posts to create
        n = 5

        # Create a post
        PostFactory.create_batch(n)

        # Get all posts
        posts = Post.get_all()

        # Assert the number of posts
        self.assertEqual(len(posts), n)

    def test_get_all_empty(self):
        # Get all posts
        posts = Post.get_all()

        # Assert that posts is an empty list
        self.assertEqual(posts, [])