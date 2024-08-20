# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Managers
from app.managers.comment import CommentVoteManager


class TestReadUpvotedComments(BaseTestCase):
    def test_read_upvoted_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some upvotes
        upvotes = CommentVoteFactory.create_batch(n, user=user, direction=1)

        # Read user upvotes
        upvoted_comments = CommentVoteManager.read_upvoted_comments_by_user(user)

        # Assert the number of upvotes
        self.assertEqual(len(upvoted_comments), n)

        # Get the comments from the upnvotes
        comments = [upvote.comment for upvote in upvotes]

        # Assert the upvotes are the same
        self.assertEqual(comments, upvoted_comments)

    def test_read_upvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Read user upvoted comments
        upvoted_comments = CommentVoteManager.read_upvoted_comments_by_user(user)

        # Assert the number of upvoted comments
        self.assertEqual(len(upvoted_comments), 0)

        # Assert that the upvoted comments are an empty list
        self.assertEqual(upvoted_comments, [])

