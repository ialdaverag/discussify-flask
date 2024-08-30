# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.comment import Comment


class TestGetAllRootCommentsByPost(BaseTestCase):
    def test_get_all_root_comments_by_post(self):
        # Create a post
        post = PostFactory()

        # Number of root comments to create
        n = 5

        # Create a root comment
        CommentFactory.create_batch(n, post=post)

        # Get all root comments by the post
        root_comments_by_post = Comment.get_all_root_comments_by_post(post)

        # Assert the number of root comments
        self.assertEqual(len(root_comments_by_post), n)

    def test_get_all_root_comments_by_post_empty(self):
        # Create a post
        post = PostFactory()

        # Get all root comments by the post
        root_comments_by_post = Comment.get_all_root_comments_by_post(post)

        # Assert that root_comments_by_post is an empty list
        self.assertEqual(root_comments_by_post, [])