# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostVote

# Managers
from app.managers.post import PostVoteManager


class TestReadUpvotedPosts(BaseTestCase):
    def test_read_upvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Read user upvotes
        posts_upvoted_to_read = PostVoteManager.read_upvoted_posts_by_user(user)

        # Assert the number of upvotes
        self.assertEqual(len(posts_upvoted_to_read), n)

        # Assert the upvotes are the same
        self.assertEqual(posts, posts_upvoted_to_read)

    def test_read_upvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Read user upvotes
        upvotes_to_read = PostVoteManager.read_upvoted_posts_by_user(user)

        # Assert the number of upvotes
        self.assertEqual(len(upvotes_to_read), 0)

        # Assert that the upvotes are an empty list
        self.assertEqual(upvotes_to_read, [])




