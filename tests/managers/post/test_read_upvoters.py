# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.post_factory import PostFactory

# Managers
from app.managers.post import PostVoteManager

# Factories
from tests.factories.post_vote_factory import PostVoteFactory

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadUpvoters(BasePaginationTest):
    def test_read_upvoters(self):
        # Number of upvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        PostVoteFactory.create_batch(n, post=post, direction=1)

        # Set the args
        args = {}

        # Read the post upvoters
        upvoters_by_post = PostVoteManager.read_upvoters_by_post(post, args)

        # Assert that the upvoters are a Pagination object
        self.assertIsInstance(upvoters_by_post, Pagination)

        # Get the items
        upvoters = upvoters_by_post.items  

        # Assert the number of upvoters
        self.assertEqual(len(upvoters), n)     

    def test_read_upvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Set the args
        args = {}

        # Read the upvoters of the post
        upvoters_by_post = PostVoteManager.read_upvoters_by_post(post, args)

        # Assert that the upvoters are a Pagination object
        self.assertIsInstance(upvoters_by_post, Pagination)

        # Get the items
        upvoters = upvoters_by_post.items

        # Assert that there are no upvoters
        self.assertEqual(len(upvoters), 0)
