# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostBookmark


class TestIsBookmarkedBy(BaseTestCase):
    def test_is_bookmarked_by_true(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Bookmark the post
        PostBookmark(user=user, post=post).save()

        # Assert that the post is bookmarked by the user
        self.assertTrue(post.is_bookmarked_by(user))

    def test_is_bookmarked_by_false(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Assert that the post is not bookmarked by the user
        self.assertFalse(post.is_bookmarked_by(user))