# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Managers
from app.managers.comment import CommentVoteManager


class TestReadDownvotedComments(BaseTestCase):
    def test_read_downvoted_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some downvotes
        downvotes = CommentVoteFactory.create_batch(n, user=user, direction=-1)

        # Read user downvotes
        downvoted_comments = CommentVoteManager.read_downvoted_comments_by_user(user)

        # Assert the number of downvotes
        self.assertEqual(len(downvoted_comments), n)

        # Get the comments from the downvotes
        comments = [downvote.comment for downvote in downvotes]

        # Assert the downvotes are the same
        self.assertEqual(downvoted_comments, comments)

    def test_read_downvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Read user bookmarks
        downvoted_comments = CommentVoteManager.read_downvoted_comments_by_user(user)

        # Assert the number of downvoted comments
        self.assertEqual(len(downvoted_comments), 0)

        # Assert that the downvoted comments are an empty list
        self.assertEqual(downvoted_comments, [])
