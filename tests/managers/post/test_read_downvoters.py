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


class TestReadDownvoters(BasePaginationTest):
    def test_read_downvoters(self):
        # Number of downvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Set the args
        args = {}

        # Read the post downvoters
        downvoters_by_post = PostVoteManager.read_downvoters_by_post(post, args)

        # Assert that the downvoters are a Pagination object
        self.assertIsInstance(downvoters_by_post, Pagination)

        # Get the items
        downvoters = downvoters_by_post.items  

        # Assert the number of downvoters
        self.assertEqual(len(downvoters), n)     

    def test_read_downvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Set the args
        args = {}

        # Read the downvoters of the post
        downvoters_by_post = PostVoteManager.read_downvoters_by_post(post, args)

        # Assert that the downvoters are a Pagination object
        self.assertIsInstance(downvoters_by_post, Pagination)

        # Get the items
        downvoters = downvoters_by_post.items

        # Assert that there are no downvoters
        self.assertEqual(len(downvoters), 0)
