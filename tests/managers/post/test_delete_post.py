# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.post import Post

# Errors
from app.errors.errors import OwnershipError

# Managers
from app.managers.post import PostManager

# Factories
from tests.factories.post_factory import PostFactory


class TestDeletePost(BaseTestCase):
    def test_delete_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        user = post.owner

        # Get the post to delete
        post_to_delete = Post.get_by_id(post.id)

        # Delete the post
        PostManager.delete(user, post_to_delete)

        # Assert that the post was deleted
        self.assertNotIn(post, user.posts)

        # Assert that the owner's stats were updated
        posts_count = user.stats.posts_count

        self.assertEqual(posts_count, 0)

    def test_delete_post_not_being_the_owner(self):
        # Create a user to be the creator of the post
        post = PostFactory()

        # Create another user
        user = UserFactory()

        # Attempt to delete the post
        with self.assertRaises(OwnershipError):
            PostManager.delete(user, post)