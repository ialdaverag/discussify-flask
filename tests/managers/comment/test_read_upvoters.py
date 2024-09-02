# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Managers
from app.managers.comment import CommentVoteManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetUpvotersByComment(BaseTestCase):
    def test_get_upvoters_by_comment(self):
        # Number of upvotes
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some votes
        CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Set the args
        args = {}

        # Get the upvoters by comment
        upvoters_by_comment = CommentVoteManager.read_upvoters_by_comment(comment, args)

        # Assert upvoters_by_comment is a Pagination object
        self.assertIsInstance(upvoters_by_comment, Pagination)

        # Get the items
        upvoters_by_comment_items = upvoters_by_comment.items

        # Assert the number of upvoters
        self.assertEqual(len(upvoters_by_comment_items), n)

    def test_get_upvoters_by_comment_none(self):
        # Create a comment
        comment = CommentFactory()

        # Set the args
        args = {}

        # Get the upvoters by comment
        upvoters_by_comment = CommentVoteManager.read_upvoters_by_comment(comment, args)

        # Assert upvoters_by_comment is a Pagination object
        self.assertIsInstance(upvoters_by_comment, Pagination)

        # Get the items
        upvoters_by_comment_items = upvoters_by_comment.items

        # Assert the number of upvoters
        self.assertEqual(len(upvoters_by_comment_items), 0)
