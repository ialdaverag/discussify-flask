# Base
from tests.base.base_test_case import BaseTestCase

# Errors
from app.errors.errors import NotFoundError

# Managers
from app.managers.post import PostManager

# Factories
from tests.factories.post_factory import PostFactory


class TestReadPost(BaseTestCase):
    def test_read_post(self):
        # Create a post
        post = PostFactory()

        # Read the post
        post_to_read = PostManager.read(post.id)

        # Assert that the post is the same
        self.assertEqual(post, post_to_read)

    def test_read_post_not_found(self):
        # Attempt to read a post that does not exist
        with self.assertRaises(NotFoundError):
            post_to_read = PostManager.read(0)