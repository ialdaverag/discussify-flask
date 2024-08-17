# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Managers
from app.managers.post import PostBookmarkManager

# utils
from tests.utils.tokens import get_access_token


class TestReadBookmarkedPosts(BaseTestCase):
    route = '/user/posts/bookmarked'

    def test_read_bookmarked_posts(self):
        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(5)

        # Make the user bookmark the posts
        for post in posts:
            PostBookmarkManager.create(user, post)

        # Get user access token
        access_token = get_access_token(user)

        # Get user bookmarked posts
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