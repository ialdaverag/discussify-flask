# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetDownvotedCommentsByUser(BasePaginationTest):
    def test_get_downvoted_comments_by_user(self):
        # Number of downvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        CommentVoteFactory.create_batch(n, user=user, direction=-1)

        # Set the args
        args = {}

        # Get the downvoted comments by user
        downvoted_comments_by_user = CommentVote.get_downvoted_comments_by_user(user, args)

        # Assert downvoted_comments_by_user is a Pagination object
        self.assertIsInstance(downvoted_comments_by_user, Pagination)

        # Get the items
        items = downvoted_comments_by_user.items

        # Assert the number of downvoted comments
        self.assertEqual(len(items), n)

    def test_get_downvoted_comments_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the downvoted comments by user
        downvoted_comments_by_user = CommentVote.get_downvoted_comments_by_user(user, args)

        # Assert downvoted_comments_by_user is a Pagination object
        self.assertIsInstance(downvoted_comments_by_user, Pagination)

        # Get the items
        items = downvoted_comments_by_user.items

        # Assert the number of downvoted comments
        self.assertEqual(len(items), 0)