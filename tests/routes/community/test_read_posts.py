# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestReadPosts(BaseTestCase):
    route = '/community/{}/posts'

    def test_read_posts_successful(self):
        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(5, community=community)

        # Read the community posts
        response = self.client.get(self.route.format(community.name))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

    def test_read_posts_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community posts
        response = self.client.get(self.route.format(community.name))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is an empty list
        self.assertEqual(data, [])

    def test_read_posts_nonexistent_community(self):
        # Try to get posts of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
