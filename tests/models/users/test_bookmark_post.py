# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Errors
from app.errors.errors import BookmarkError


class TestBookmarkPost(BaseTestCase):
    def test_bookmark_post(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Bookmark the post
        user.bookmark_post(post)

        # Assert that the post was bookmarked
        self.assertIn(post, user.bookmarks)

    def test_bookmark_post_already_bookmarked(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the post to the user's bookmarks
        post.append_bookmarker(user)

        # Attempt to bookmark the post again
        with self.assertRaises(BookmarkError):
            user.bookmark_post(post)
