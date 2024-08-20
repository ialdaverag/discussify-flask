# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote


class TestGetUpvotedPostsByUser(BaseTestCase):
    def test_get_upvoted_posts_by_user(self):
        # Number of upvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        votes = PostVoteFactory.create_batch(n, user=user, direction=1)

        # Get the upvoted posts by user
        upvoted_posts_by_user = PostVote.get_upvoted_posts_by_user(user)

        # Assert the number of upvoted posts
        self.assertEqual(len(votes), n)

        # Get the upvoted posts
        posts = [vote.post for vote in votes]

        # Assert that the upvoted posts are the same
        self.assertEqual(posts, upvoted_posts_by_user)

    def test_get_upvoted_posts_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Get the upvoted posts by user
        upvoted_posts_by_user = PostVote.get_upvoted_posts_by_user(user)

        # Assert the number of upvoted posts
        self.assertEqual(len(upvoted_posts_by_user), 0)

        # Assert that the upvoters list is empty
        self.assertEqual(upvoted_posts_by_user, [])