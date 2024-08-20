# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_vote_factory import CommentVoteFactory

# Models
from app.models.comment import CommentVote


class TestGetByUserAndComment(BaseTestCase):
    def test_get_by_user_and_comment(self):
        # Create a vote
        vote = CommentVoteFactory()

        # Get the user
        user = vote.user

        # Get the comment
        comment = vote.comment

        # Get the vote by user and comment
        vote_by_user_and_comment = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the vote is the same
        self.assertEqual(vote, vote_by_user_and_comment)

    def test_get_by_user_and_comment_none(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Get the vote by user and comment
        vote_by_user_and_comment = CommentVote.get_by_user_and_comment(user, comment)

        # Assert that the vote is None
        self.assertIsNone(vote_by_user_and_comment)
