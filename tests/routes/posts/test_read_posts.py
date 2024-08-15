# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestDeletePost(BaseTestCase):
    route = '/post/'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create multiple communities
        posts = PostFactory.create_batch(n)

        # Get the posts
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the number of posts
        self.assertEqual(len(data), n)

        # Assert each post
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_posts_empty(self):
        # Get the posts
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)