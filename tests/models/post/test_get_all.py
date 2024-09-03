# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class GetAllPosts(BaseTestCase):
    def test_get_posts(self):
        # Number of posts
        n = 5

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Set the args
        args = {}

        # get the posts
        get_posts = Post.get_all(args)

        # Assert get_posts is a Pagination object
        self.assertIsInstance(get_posts, Pagination)

        # Get the items
        get_posts_items = get_posts.items

        # Assert the number of posts
        self.assertEqual(len(get_posts_items), n)

        # Assert that the posts are the same
        self.assertEqual(posts, get_posts_items)


    def test_get_posts_empty(self):
        # Set the args
        args = {}

        # get the posts
        get_posts = Post.get_all(args)

        # Assert get_posts is a Pagination object
        self.assertIsInstance(get_posts, Pagination)

        # Get the items
        get_posts_items = get_posts.items

        # Assert that there are no posts
        self.assertEqual(len(get_posts_items), 0)