# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory

# Managers
from app.managers.post import PostVoteManager

# Factories
from tests.factories.post_vote_factory import PostVoteFactory


class TestReadDownvoters(BaseTestCase):
    def test_read_downvoters(self):
         # Number of upvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        downvotes = PostVoteFactory.create_batch(n, post=post, direction=1)

        # Read the post downvoters
        downvoters = PostVoteManager.read_upvoters_by_post(post)

        # Assert the number of downvotes
        self.assertEqual(len(downvoters), n)

        # Get the users
        users = [downvote.user for downvote in downvotes]

        # Assert that the users are unique
        self.assertEqual(downvoters, users) 


    def test_read_downvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Read the downvoters of the post
        downvoters = PostVoteManager.read_downvoters_by_post(post)

        # Assert that there are no downvoters
        self.assertEqual(len(downvoters), 0)

        # Assert that the downvoters are an empty list
        self.assertEqual(downvoters, [])