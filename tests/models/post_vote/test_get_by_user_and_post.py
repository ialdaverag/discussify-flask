# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote


class TestGetByUserAndPost(BaseTestCase):
    def test_get_by_user_and_post(self):
        # Create a vote
        vote = PostVoteFactory()

        # Get the user
        user = vote.user

        # Get the post
        post = vote.post

        # Get the vote by user and post
        vote_by_user_and_post = PostVote.get_by_user_and_post(user, post)

        # Assert that the vote is the same
        self.assertEqual(vote, vote_by_user_and_post)

    def test_get_by_user_and_post_none(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Get the vote by user and post
        vote_by_user_and_post = PostVote.get_by_user_and_post(user, post)

        # Assert that the vote is None
        self.assertIsNone(vote_by_user_and_post)
