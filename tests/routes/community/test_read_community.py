# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory


class TestReadCommunity(BaseTestCase):
    route = '/community/{}'

    def test_read_community(self):
        # Create a community
        community = CommunityFactory()

        # Get the community
        response = self.client.get(self.route.format(community.name))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('about', data)
        self.assertIn('owned_by', data)
        self.assertIn('subscriber', data)
        self.assertIn('moderator', data)
        self.assertIn('ban', data)
        self.assertIn('owner', data)
        self.assertIn('stats', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert the community data
        self.assertEqual(data['id'], community.id)
        self.assertEqual(data['name'], community.name)
        self.assertEqual(data['about'], community.about)
        self.assertEqual(data['created_at'], community.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], community.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_community_nonexistent(self):
        # Get the community
        response = self.client.get(self.route.format('inexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('message', data)

        # Assert the error
        self.assertEqual(data['message'], 'Community not found.')