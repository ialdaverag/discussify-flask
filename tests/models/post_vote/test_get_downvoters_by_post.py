# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote


class TestGetDownvotersByPost(BaseTestCase):
    def test_get_downvoters_by_post(self):
        # Number of downvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        votes = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters by post
        downvoters_by_post = PostVote.get_downvoters_by_post(post)

        # Assert the number of downvoters
        self.assertEqual(len(votes), n)

        # Get the downvoters
        users = [vote.user for vote in votes]

        # Assert that the downvoters are the same
        self.assertEqual(downvoters_by_post, users)

    def test_get_downvoters_by_post_none(self):
        # Create a post
        post = PostFactory()

        # Get the downvoters by post
        downvoters_by_post = PostVote.get_downvoters_by_post(post)

        # Assert the number of downvoters
        self.assertEqual(len(downvoters_by_post), 0)

        # Assert that the downvoters list is empty
        self.assertEqual(downvoters_by_post, [])