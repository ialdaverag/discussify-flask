# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory

# Managers
from app.managers.post import PostBookmarkManager


class TestReadBookmarkedPosts(BaseTestCase):
    def test_read_bookmarked_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Read user bookmarks
        bookmarked_posts = PostBookmarkManager.read_bookmarked_posts_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarked_posts), n)

        # Get the posts from the bookmarks
        posts = [bookmark.post for bookmark in bookmarks]

        # Assert the bookmarks are the same
        self.assertEqual(bookmarked_posts, posts)

    def test_read_bookmarked_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Read user bookmarks
        bookmarks_to_read = PostBookmarkManager.read_bookmarked_posts_by_user(user)

        # Assert the number of bookmarks
        self.assertEqual(len(bookmarks_to_read), 0)

        # Assert that the bookmarks are an empty list
        self.assertEqual(bookmarks_to_read, [])
