# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Managers
from app.managers.comment import CommentVoteManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadDownvotedComments(BasePaginationTest):
    def test_read_downvoted_comments(self):
        # Number of downvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        CommentVoteFactory.create_batch(n, user=user, direction=-1)

        # Set the args
        args = {}

        # Get the downvoted comments by user
        downvoted_comments_by_user = CommentVoteManager.read_downvoted_comments_by_user(user, args)

        # Assert downvoted_comments_by_user is a Pagination object
        self.assertIsInstance(downvoted_comments_by_user, Pagination)

        # Get the items
        items = downvoted_comments_by_user.items

        # Assert the number of downvoted comments
        self.assertEqual(len(items), n)

    def test_read_downvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the downvoted comments by user
        downvoted_comments_by_user = CommentVoteManager.read_downvoted_comments_by_user(user, args)

        # Assert downvoted_comments_by_user is a Pagination object
        self.assertIsInstance(downvoted_comments_by_user, Pagination)

        # Get the items
        items = downvoted_comments_by_user.items

        # Assert the number of downvoted comments
        self.assertEqual(len(items), 0)

