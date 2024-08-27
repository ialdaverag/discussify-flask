# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory
from tests.factories.user_factory import UserFactory
from tests.factories.block_factory import BlockFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadBookmarkedPosts(BaseTestCase):
    route = '/user/posts/bookmarked'

    def test_read_bookmarked_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        PostBookmarkFactory.create_batch(n, user=user)

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of bookmarks
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_bookmarked_posts_with_blocked(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of bookmarks
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_bookmarked_posts_with_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of bookmarks
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_bookmarked_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.post.owner, blocked=user).save()

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of bookmarks
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_bookmarked_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])