# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory

# Managers
from app.managers.post import PostVoteManager

# Factories
from tests.factories.post_vote_factory import PostVoteFactory


class TestReadUpvoters(BaseTestCase):
    def test_read_upvoters(self):
        # Number of upvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        upvotes = PostVoteFactory.create_batch(n, post=post, direction=1)

        # Read the post upvoters
        upvoters = PostVoteManager.read_upvoters_by_post(post)

        # Assert the number of upvotes
        self.assertEqual(len(upvoters), n)

        # Get the users
        users = [upvote.user for upvote in upvotes]

        # Assert that the users are unique
        self.assertEqual(upvoters, users)            


    def test_read_upvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Read the upvoters of the post
        upvoters = PostVoteManager.read_upvoters_by_post(post)

        # Assert that there are no upvoters
        self.assertEqual(len(upvoters), 0)

        # Assert that the upvoters are an empty list
        self.assertEqual(upvoters, [])