# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote


class TestGetDownvotedCommentsByUser(BaseTestCase):
    def test_get_downvoted_comments_by_user(self):
        # Number of downvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        votes = CommentVoteFactory.create_batch(n, user=user, direction=-1)

        # Get the downvoted comments by user
        downvoted_comments_by_user = CommentVote.get_downvoted_comments_by_user(user)

        # Assert the number of downvoted comments
        self.assertEqual(len(votes), n)

        # Get the downvoted comments
        comments = [vote.comment for vote in votes]

        # Assert that the downvoted comments are the same
        self.assertEqual(downvoted_comments_by_user, comments)

    def test_get_downvoted_comments_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Get the downvoted comments by user
        downvoted_comments_by_user = CommentVote.get_downvoted_comments_by_user(user)

        # Assert the number of downvoted comments
        self.assertEqual(len(downvoted_comments_by_user), 0)

        # Assert that the downvoted comments list is empty
        self.assertEqual(downvoted_comments_by_user, [])