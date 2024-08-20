# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory

# Models
from app.models.post import PostVote


class TestGetDownvotedPostsByUser(BaseTestCase):
    def test_get_downvoted_posts_by_user(self):
        # Number of downvotes
        n = 5

        # Create a user
        user = UserFactory()

        # Create some votes
        votes = PostVoteFactory.create_batch(n, user=user, direction=-1)

        # Get the downvoted posts by user
        downvoted_posts_by_user = PostVote.get_downvoted_posts_by_user(user)

        # Assert the number of downvoted posts
        self.assertEqual(len(votes), n)

        # Get the downvoted posts
        posts = [vote.post for vote in votes]

        # Assert that the downvoted posts are the same
        self.assertEqual(downvoted_posts_by_user, posts)

    def test_get_downvoted_posts_by_user_none(self):
        # Create a user
        user = UserFactory()

        # Get the downvoted posts by user
        downvoted_posts_by_user = PostVote.get_downvoted_posts_by_user(user)

        # Assert the number of downvoted posts
        self.assertEqual(len(downvoted_posts_by_user), 0)

        # Assert that the downvoted posts list is empty
        self.assertEqual(downvoted_posts_by_user, [])



        