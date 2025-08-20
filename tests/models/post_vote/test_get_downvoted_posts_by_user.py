# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetDownvotedPostsByUser(BasePaginationTest):
    def test_get_downvoted_posts_by_user(self):
        # Number of downvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        PostVoteFactory.create_batch(n, user=user, direction=-1)

        # Set the args
        args = {}

        # Get the downvoted posts by user
        downvoted_posts_by_user = PostVote.get_downvoted_posts_by_user(user, args)

        # Assert downvoted_posts_by_user is a Pagination object
        self.assertIsInstance(downvoted_posts_by_user, Pagination)

        # Get the items
        items = downvoted_posts_by_user.items

        # Assert the number of downvoted posts
        self.assertEqual(len(items), n)

    def test_get_downvoted_posts_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the downvoted posts by user
        downvoted_posts_by_user = PostVote.get_downvoted_posts_by_user(user, args)

        # Get the items
        items = downvoted_posts_by_user.items

        # Assert the number of downvoted posts
        self.assertEqual(len(items), 0)