# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Errors
from app.errors.errors import BookmarkError

# Models
from app.models.post import PostBookmark


class TestUnbookmarkPost(BaseTestCase):
    def test_unbookmark_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the post to the user's bookmarks
        PostBookmark(user=user, post=post).save()

        # Unbookmark the post
        user.unbookmark_post(post)

        # Assert that the post was unbookmarked
        self.assertNotIn(post, user.bookmarks)

    def test_unbookmark_post_not_bookmarked(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Attempt to unbookmark the post again
        with self.assertRaises(BookmarkError):
            user.unbookmark_post(post)
