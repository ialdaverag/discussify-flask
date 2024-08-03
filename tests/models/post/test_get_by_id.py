# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post

# Errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_id(self):
        # Create a post 
        post_to_find = PostFactory()

        # Get the post by id
        post = Post.get_by_id(post_to_find.id)

        # Assert that the post is the one we are looking for
        self.assertEqual(post.id, post_to_find.id)

    def test_get_by_id__nonexistent(self):
        # Attempt to get a post that does not exist
        with self.assertRaises(NotFoundError):
            Post.get_by_id(1)
