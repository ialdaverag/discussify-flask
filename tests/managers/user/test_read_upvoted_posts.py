# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Managers
from app.managers.post import PostVoteManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadUpvotedPosts(BaseTestCase):
    def test_read_upvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some upvotes
        upvotes = PostVoteFactory.create_batch(n, user=user, direction=1)

        # Set the args
        args = {}

        # Read user upvotes
        upvoted_posts = PostVoteManager.read_upvoted_posts_by_user(user, args)

        # Assert upvoted_posts is a Pagination object
        self.assertIsInstance(upvoted_posts, Pagination)

        # Get the items
        items = upvoted_posts.items

        # Assert items is a list
        self.assertIsInstance(items, list)

        # Assert the number of upvotes
        self.assertEqual(len(items), n)

    def test_read_upvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Read user upvotes
        upvotes_to_read = PostVoteManager.read_upvoted_posts_by_user(user, args)

        # Assert upvotes_to_read is a Pagination object
        self.assertIsInstance(upvotes_to_read, Pagination)

        # Get the items
        items = upvotes_to_read.items

        # Assert items is a list
        self.assertIsInstance(items, list)

        # Assert the number of upvotes
        self.assertEqual(len(items), 0)




