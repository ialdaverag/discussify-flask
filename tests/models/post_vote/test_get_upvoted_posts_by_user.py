# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetUpvotedPostsByUser(BaseTestCase):
    def test_get_upvoted_posts_by_user(self):
        # Number of upvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        PostVoteFactory.create_batch(n, user=user, direction=1)

        # Set the args
        args = {}

        # Get the upvoted posts by user
        upvoted_posts_by_user = PostVote.get_upvoted_posts_by_user(user, args)

        # Assert upvoted_posts_by_user is a Pagination object
        self.assertIsInstance(upvoted_posts_by_user, Pagination)

        # Get the items
        items = upvoted_posts_by_user.items

        # Assert the number of upvoted posts
        self.assertEqual(len(items), n)

    def test_get_upvoted_posts_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the upvoted posts by user
        upvoted_posts_by_user = PostVote.get_upvoted_posts_by_user(user, args)

        # Get the items
        items = upvoted_posts_by_user.items

        # Assert the number of upvoted posts
        self.assertEqual(len(items), 0)