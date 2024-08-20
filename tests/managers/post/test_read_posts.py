# Base
from tests.base.base_test_case import BaseTestCase

# Managers
from app.managers.post import PostManager

# Factories
from tests.factories.post_factory import PostFactory


class ReadPosts(BaseTestCase):
    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Read the posts
        read_posts = PostManager.read_all()

        # Assert the number of posts
        self.assertEqual(len(read_posts), n)

        # Assert that the posts are the same
        self.assertEqual(posts, read_posts)


    def test_read_posts_empty(self):
        # Read the posts
        read_posts = PostManager.read_all()

        # Assert that there are no posts
        self.assertEqual(len(read_posts), 0)

        # Assert that the posts are an empty list
        self.assertEqual(read_posts, [])