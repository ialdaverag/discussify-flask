# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Managers
from app.managers.post import PostVoteManager


class TestReadDownvotedPosts(BaseTestCase):
    def test_read_downvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some downvotes
        downvotes = PostVoteFactory.create_batch(n, user=user, direction=-1)

        # Set the args
        args = {}

        # Read user downvotes
        downvoted_posts = PostVoteManager.read_downvoted_posts_by_user(user, args)

        # Get the items
        items = downvoted_posts.items

        # Assert items is a list
        self.assertIsInstance(items, list)

        # Assert the number of downvotes
        self.assertEqual(len(items), n)

    def test_read_downvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Read user downvotes
        downvoted_comments = PostVoteManager.read_downvoted_posts_by_user(user, args)

        # Get the items
        items = downvoted_comments.items

        # Assert items is a list
        self.assertIsInstance(items, list)

        # Assert the number of downvotes
        self.assertEqual(len(items), 0)