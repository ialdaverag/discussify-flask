# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.comment import Comment

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetAllRootCommentsByPost(BasePaginationTest):
    def test_get_all_root_comments_by_post(self):
        # Create a post
        post = PostFactory()

        # Number of root comments to create
        n = 5

        # Create a root comment
        CommentFactory.create_batch(n, post=post)

        # Set the args
        args = {}

        # Get all root comments by the post
        root_comments_by_post = Comment.get_all_root_comments_by_post(post, args)

        # Assert the type of root_comments_by_post
        self.assertIsInstance(root_comments_by_post, Pagination)

        # Get the items
        items = root_comments_by_post.items

        # Assert the number of root comments
        self.assertEqual(len(items), n)

    def test_get_all_root_comments_by_post_empty(self):
        # Create a post
        post = PostFactory()

        # Set the args
        args = {}

        # Get all root comments by the post
        root_comments_by_post = Comment.get_all_root_comments_by_post(post, args)

        # Assert the type of root_comments_by_post
        self.assertIsInstance(root_comments_by_post, Pagination)

        # Get the items
        items = root_comments_by_post.items

        # Assert the number of root comments
        self.assertEqual(len(items), 0)