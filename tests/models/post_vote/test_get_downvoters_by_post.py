# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetDownvotersByPost(BasePaginationTest):
    def test_get_downvoters_by_post(self):
        # Number of downvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Set the args
        args = {}

        # Get the downvoters by post
        downvoters_by_post = PostVote.get_downvoters_by_post(post, args)

        # Assert downvoters_by_post is a Pagination object
        self.assertIsInstance(downvoters_by_post, Pagination)

        # Get the items
        downvoters = downvoters_by_post.items

        # Assert the number of downvoters
        self.assertEqual(len(downvoters), n)

    def test_get_downvoters_by_post_empty(self):
        # Create a post
        post = PostFactory()

        # Set the args
        args = {}

        # Get the downvoters by post
        downvoters_by_post = PostVote.get_downvoters_by_post(post, args)

        # Assert downvoters_by_post is a Pagination object
        self.assertIsInstance(downvoters_by_post, Pagination)

        # Get the items
        downvoters = downvoters_by_post.items

        # Assert the number of downvoters
        self.assertEqual(len(downvoters), 0)
