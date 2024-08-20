# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote


class TestGetUpvotersByPost(BaseTestCase):
    def test_get_upvoters_by_post(self):
        # Number of upvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        votes = PostVoteFactory.create_batch(n, post=post, direction=1)

        # Get the upvoters by post
        upvoters_by_post = PostVote.get_upvoters_by_post(post)

        # Assert the number of upvoters
        self.assertEqual(len(votes), n)

        # Get the upvoters
        users = [vote.user for vote in votes]

        # Assert that the upvoters are the same
        self.assertEqual(upvoters_by_post, users)

    def test_get_upvoters_by_post_empty(self):
        # Create a post
        post = PostFactory()

        # Get the upvoters by post
        upvoters_by_post = PostVote.get_upvoters_by_post(post)

        # Assert the number of upvoters
        self.assertEqual(len(upvoters_by_post), 0)

        # Assert that the upvoters list is empty
        self.assertEqual(upvoters_by_post, [])