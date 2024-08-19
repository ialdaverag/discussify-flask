# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostVote

# Managers
from app.managers.post import PostVoteManager


class TestReadDownvotedPosts(BaseTestCase):
    def test_read_downvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user downvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=-1).save()

        # Read user downvotes
        posts_downvoted_to_read = PostVoteManager.read_downvoted_posts_by_user(user)

        # Assert the number of downvotes
        self.assertEqual(len(posts_downvoted_to_read), n)

        # Assert the downvotes are the same
        self.assertEqual(posts, posts_downvoted_to_read)

    def test_read_downvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Read user downvotes
        downvotes_to_read = PostVoteManager.read_downvoted_posts_by_user(user)

        # Assert the number of downvotes
        self.assertEqual(len(downvotes_to_read), 0)

        # Assert that the downvotes are an empty list
        self.assertEqual(downvotes_to_read, [])