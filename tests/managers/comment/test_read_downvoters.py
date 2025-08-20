# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Managers
from app.managers.comment import CommentVoteManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetDownvotersByComment(BasePaginationTest):
    def test_get_downvoters_by_comment(self):
        # Number of downvotes
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some votes
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Set the args
        args = {}

        # Get the downvoters by comment
        downvoters_by_comment = CommentVoteManager.read_downvoters_by_comment(comment, args)

        # Assert downvoters_by_comment is a Pagination object
        self.assertIsInstance(downvoters_by_comment, Pagination)

        # Get the items
        downvoters_by_comment_items = downvoters_by_comment.items

        # Assert the number of downvoters
        self.assertEqual(len(downvoters_by_comment_items), n)

    def test_get_downvoters_by_comment_none(self):
        # Create a comment
        comment = CommentFactory()

        # Set the args
        args = {}

        # Get the downvoters by comment
        downvoters_by_comment = CommentVoteManager.read_downvoters_by_comment(comment, args)

        # Assert downvoters_by_comment is a Pagination object
        self.assertIsInstance(downvoters_by_comment, Pagination)

        # Get the items
        downvoters_by_comment_items = downvoters_by_comment.items

        # Assert the number of downvoters
        self.assertEqual(len(downvoters_by_comment_items), 0)
