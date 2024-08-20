# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote


class TestGetUpvotedCommentsByUser(BaseTestCase):
    def test_get_upvoted_comments_by_user(self):
        # Number of upvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        votes = CommentVoteFactory.create_batch(n, user=user, direction=1)

        # Get the upvoted comments by user
        upvoted_comments_by_user = CommentVote.get_upvoted_comments_by_user(user)

        # Assert the number of upvoted comments
        self.assertEqual(len(votes), n)

        # Get the upvoted comments
        comments = [vote.comment for vote in votes]

        # Assert that the upvoted comments are the same
        self.assertEqual(upvoted_comments_by_user, comments)

    def test_get_upvoted_comments_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Get the upvoted comments by user
        upvoted_comments_by_user = CommentVote.get_upvoted_comments_by_user(user)

        # Assert the number of upvoted comments
        self.assertEqual(len(upvoted_comments_by_user), 0)

        # Assert that the upvoted comments list is empty
        self.assertEqual(upvoted_comments_by_user, [])