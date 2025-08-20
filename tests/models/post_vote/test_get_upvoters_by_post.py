# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetUpvotersByPost(BasePaginationTest):
    def test_get_upvoters_by_post(self):
        # Number of upvotes
        n = 5

        # Create a post
        post = PostFactory()

        # Create some votes
        PostVoteFactory.create_batch(n, post=post, direction=1)

        # Set the args
        args = {}

        # Get the upvoters by post
        upvoters_by_post = PostVote.get_upvoters_by_post(post, args)

        # Assert upvoters_by_post is a Pagination object
        self.assertIsInstance(upvoters_by_post, Pagination)

        # Get the items
        upvoters = upvoters_by_post.items

        # Assert the number of upvoters
        self.assertEqual(len(upvoters), n)

    def test_get_upvoters_by_post_empty(self):
        # Create a post
        post = PostFactory()

        # Set the args
        args = {}

        # Get the upvoters by post
        upvoters_by_post = PostVote.get_upvoters_by_post(post, args)

        # Assert upvoters_by_post is a Pagination object
        self.assertIsInstance(upvoters_by_post, Pagination)

        # Get the items
        upvoters = upvoters_by_post.items

        # Assert the number of upvoters
        self.assertEqual(len(upvoters), 0)
