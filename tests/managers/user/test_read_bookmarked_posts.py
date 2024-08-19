# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostBookmark

# Managers
from app.managers.post import PostBookmarkManager


class TestReadBookmarkedPosts(BaseTestCase):
    def test_read_bookmarked_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user bookmark the posts
        for post in posts:
            PostBookmark(user=user, post=post).save()

        # Read user bookmarks
        bookmarks_to_read = PostBookmarkManager.read_bookmarked_posts_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_to_read), n)

        # Assert the bookmarks are the same
        self.assertEqual(posts, bookmarks_to_read)

    def test_read_bookmarked_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Read user bookmarks
        bookmarks_to_read = PostBookmarkManager.read_bookmarked_posts_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_to_read), 0)

        # Assert that the bookmarks are an empty list
        self.assertEqual(bookmarks_to_read, [])
