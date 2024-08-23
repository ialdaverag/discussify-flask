# Base
from tests.base.base_test_case import BaseTestCase

# Errors
from app.errors.errors import BlockError

# Managers
from app.managers.post import PostManager

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block


class TestReadPost(BaseTestCase):
    def test_read_post_anonymous(self):
        # Create a user
        user = None

        # Create a post
        post = PostFactory()

        # Read the post
        post_to_read = PostManager.read(user, post)

        # Assert that the post is the same
        self.assertEqual(post, post_to_read)

    def test_read_post_user(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Read the post
        post_to_read = PostManager.read(user, post)

        # Assert that the post is the same
        self.assertEqual(post, post_to_read)

    def test_read_post_user_blocked_by_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the post
        owner = post.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Read the post
        with self.assertRaises(BlockError):
            PostManager.read(user, post)

    def test_read_post_user_owner_blocked_by_user(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the post
        owner = post.owner

        # Block the owner
        Block(blocker=user, blocked=owner).save()

        # Read the post
        with self.assertRaises(BlockError):
            PostManager.read(user, post)