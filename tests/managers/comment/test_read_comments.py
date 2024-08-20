# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentManager


class TestReadComments(BaseTestCase):
    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a comment
        comments = CommentFactory.create_batch(n)

        # Read the comment
        comment_to_read = CommentManager.read_all()

        # Assert the number of comments
        self.assertEqual(len(comment_to_read), n)

        # Assert that the comment is the same
        self.assertEqual(comments, comment_to_read)

    def test_read_comments_empty(self):
        # Read the comments
        read_comments = CommentManager.read_all()

        # Assert that there are no comments
        self.assertEqual(len(read_comments), 0)

        # Assert that the comments are an empty list
        self.assertEqual(read_comments, [])