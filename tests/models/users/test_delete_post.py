# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Errors
from app.errors.errors import OwnershipError

# Models
from app.models.post import Post


class TestCreatePost(BaseTestCase):
    def test_delete_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        user = post.owner

        # Get the post to delete
        post_to_delete = Post.get_by_id(post.id)

        # Delete the post
        user.delete_post(post_to_delete)

        # Assert that the post was deleted
        self.assertNotIn(post, user.posts)

    def test_delete_post_not_being_the_owner(self):
        # Create a user to be the creator of the post
        post = PostFactory()

        # Create another user
        user = UserFactory()

        # Attempt to delete the post
        with self.assertRaises(OwnershipError):
            user.delete_post(post)