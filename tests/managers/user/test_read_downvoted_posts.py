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

        # Read user downvotes
        downvoted_posts = PostVoteManager.read_downvoted_posts_by_user(user)

        # Assert the number of downvotes
        self.assertEqual(len(downvoted_posts), n)

        # Get the posts from the downvotes
        posts = [downvote.post for downvote in downvotes]

        # Assert the downvotes are the same
        self.assertEqual(posts, downvoted_posts)

    def test_read_downvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Read user downvotes
        downvoted_comments = PostVoteManager.read_downvoted_posts_by_user(user)

        # Assert the number of downvotes
        self.assertEqual(len(downvoted_comments), 0)

        # Assert that the downvotes are an empty list
        self.assertEqual(downvoted_comments, [])