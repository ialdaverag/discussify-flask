# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetDownvotersByComment(BaseTestCase):
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
        downvoters_by_comment = CommentVote.get_downvoters_by_comment(comment, args)

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
        downvoters_by_comment = CommentVote.get_downvoters_by_comment(comment, args)

        # Assert downvoters_by_comment is a Pagination object
        self.assertIsInstance(downvoters_by_comment, Pagination)

        # Get the items
        downvoters_by_comment_items = downvoters_by_comment.items

        # Assert the number of downvoters
        self.assertEqual(len(downvoters_by_comment_items), 0)


