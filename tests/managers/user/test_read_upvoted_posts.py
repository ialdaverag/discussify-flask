# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Managers
from app.managers.post import PostVoteManager


class TestReadUpvotedPosts(BaseTestCase):
    def test_read_upvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some upvotes
        upvotes = PostVoteFactory.create_batch(n, user=user, direction=1)

        # Read user upvotes
        upvoted_posts = PostVoteManager.read_upvoted_posts_by_user(user)

        # Assert the number of upvotes
        self.assertEqual(len(upvoted_posts), n)

        # Get the posts from the upnvotes
        posts = [upvote.post for upvote in upvotes]

        # Assert the upvotes are the same
        self.assertEqual(posts, upvoted_posts)

    def test_read_upvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Read user upvotes
        upvotes_to_read = PostVoteManager.read_upvoted_posts_by_user(user)

        # Assert the number of upvotes
        self.assertEqual(len(upvotes_to_read), 0)

        # Assert that the upvotes are an empty list
        self.assertEqual(upvotes_to_read, [])




