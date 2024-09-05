# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Managers
from app.managers.comment import CommentVoteManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadUpvotedComments(BaseTestCase):
    def test_read_upvoted_comments(self):
        # Number of upvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        CommentVoteFactory.create_batch(n, user=user, direction=1)

        # Set the args
        args = {}

        # Get the upvoted comments by user
        upvoted_comments_by_user = CommentVoteManager.read_upvoted_comments_by_user(user, args)

        # Assert upvoted_comments_by_user is a Pagination object
        self.assertIsInstance(upvoted_comments_by_user, Pagination)

        # Get the items
        items = upvoted_comments_by_user.items

        # Assert the number of upvoted comments
        self.assertEqual(len(items), n)

    def test_read_upvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the upvoted comments by user
        upvoted_comments_by_user = CommentVoteManager.read_upvoted_comments_by_user(user, args)

        # Assert upvoted_comments_by_user is a Pagination object
        self.assertIsInstance(upvoted_comments_by_user, Pagination)

        # Get the items
        items = upvoted_comments_by_user.items

        # Assert the number of upvoted comments
        self.assertEqual(len(items), 0)

