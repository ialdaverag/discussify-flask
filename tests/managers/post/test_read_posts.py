# Base
from tests.base.base_pagination_test import BasePaginationTest

# Managers
from app.managers.post import PostManager

# Factories
from tests.factories.post_factory import PostFactory

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class ReadPosts(BasePaginationTest):
    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Set the args
        args = {}

        # Read the posts
        read_posts = PostManager.read_all(args)

        # Assert read_posts is a Pagination object
        self.assertIsInstance(read_posts, Pagination)

        # Get the items
        read_posts_items = read_posts.items

        # Assert the number of posts
        self.assertEqual(len(read_posts_items), n)

        # Assert that the posts are the same
        self.assertCountEqual(posts, read_posts_items)


    def test_read_posts_empty(self):
        # Set the args
        args = {}

        # Read the posts
        read_posts = PostManager.read_all(args)

        # Assert read_posts is a Pagination object
        self.assertIsInstance(read_posts, Pagination)

        # Get the items
        read_posts_items = read_posts.items

        # Assert that there are no posts
        self.assertEqual(len(read_posts_items), 0)