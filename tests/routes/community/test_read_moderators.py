# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestReadModerators(BaseTestCase):
    route = '/community/{}/moderators'

    def test_read_moderators(self):
        # Number of moderators
        n = 5

        # Create multiple moderators
        moderators = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the moderators to the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Read the community moderators
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert that pagination is a dictionary
        self.assertIsInstance(pagination, dict)

        # Assert the response data structure
        self.assertIn('links', pagination)
        self.assertIn('page', pagination)
        self.assertIn('pages', pagination)
        self.assertIn('per_page', pagination)
        self.assertIn('total', pagination)
        self.assertIn('users', pagination)

        # Assert that links is a dictionary
        self.assertIsInstance(pagination['links'], dict)

        # Get the links
        links = pagination['links']

        # Assert the links
        self.assertIn('first', links)
        self.assertIn('last', links)
        self.assertNotIn('prev', links)
        self.assertNotIn('next', links)

        # Assert the page
        self.assertEqual(pagination['page'], 1)
        
        # Assert the pages
        self.assertEqual(pagination['pages'], 1)

        # Assert the per page
        self.assertEqual(pagination['per_page'], 10)

        # Assert the total
        self.assertEqual(pagination['total'], n)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for user in data:
            self.assertIn('id', user)
            self.assertIn('username', user)
            self.assertIn('email', user)
            self.assertIn('following', user)
            self.assertIn('follower', user)
            self.assertIn('stats', user)
            self.assertIn('created_at', user)
            self.assertIn('updated_at', user)

    def test_read_moderators_args(self):
        # Number of moderators
        n = 5

        # Create multiple moderators
        moderators = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the moderators to the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Read the community moderators
        response = self.client.get(self.route.format(community.name), query_string=args)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert that pagination is a dictionary
        self.assertIsInstance(pagination, dict)

        # Assert the response data structure
        self.assertIn('links', pagination)
        self.assertIn('page', pagination)
        self.assertIn('pages', pagination)
        self.assertIn('per_page', pagination)
        self.assertIn('total', pagination)
        self.assertIn('users', pagination)

        # Assert that links is a dictionary
        self.assertIsInstance(pagination['links'], dict)

        # Get the links
        links = pagination['links']

        # Assert the links
        self.assertIn('first', links)
        self.assertIn('last', links)
        self.assertNotIn('prev', links)
        self.assertIn('next', links)

        # Assert the page
        self.assertEqual(pagination['page'], 1)
        
        # Assert the pages
        self.assertEqual(pagination['pages'], 3)

        # Assert the per page
        self.assertEqual(pagination['per_page'], 2)

        # Assert the total
        self.assertEqual(pagination['total'], n)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), 2)

        # Assert the response data structure
        for user in data:
            self.assertIn('id', user)
            self.assertIn('username', user)
            self.assertIn('email', user)
            self.assertIn('following', user)
            self.assertIn('follower', user)
            self.assertIn('stats', user)
            self.assertIn('created_at', user)
            self.assertIn('updated_at', user)

    def test_read_moderators_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community moderators
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert that pagination is a dictionary
        self.assertIsInstance(pagination, dict)

        # Assert the response data structure
        self.assertIn('links', pagination)
        self.assertIn('page', pagination)
        self.assertIn('pages', pagination)
        self.assertIn('per_page', pagination)
        self.assertIn('total', pagination)
        self.assertIn('users', pagination)

        # Assert that links is a dictionary
        self.assertIsInstance(pagination['links'], dict)

        # Get the links
        links = pagination['links']

        # Assert the links
        self.assertIn('first', links)
        self.assertIn('last', links)
        self.assertNotIn('prev', links)
        self.assertNotIn('next', links)

        # Assert the page
        self.assertEqual(pagination['page'], 1)
        
        # Assert the pages
        self.assertEqual(pagination['pages'], 0)

        # Assert the per page
        self.assertEqual(pagination['per_page'], 10)

        # Assert the total
        self.assertEqual(pagination['total'], 0)

        # Get response data
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data
        self.assertEqual(data, [])

    def test_read_moderators_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Read the community moderators
        response = self.client.get(self.route.format(community.name), query_string=args)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert that pagination is a dictionary
        self.assertIsInstance(pagination, dict)

        # Assert the response data structure
        self.assertIn('links', pagination)
        self.assertIn('page', pagination)
        self.assertIn('pages', pagination)
        self.assertIn('per_page', pagination)
        self.assertIn('total', pagination)
        self.assertIn('users', pagination)

        # Assert that links is a dictionary
        self.assertIsInstance(pagination['links'], dict)

        # Get the links
        links = pagination['links']

        # Assert the links
        self.assertIn('first', links)
        self.assertIn('last', links)
        self.assertNotIn('prev', links)
        self.assertNotIn('next', links)

        # Assert the page
        self.assertEqual(pagination['page'], 1)
        
        # Assert the pages
        self.assertEqual(pagination['pages'], 0)

        # Assert the per page
        self.assertEqual(pagination['per_page'], 2)

        # Assert the total
        self.assertEqual(pagination['total'], 0)

        # Get response data
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data
        self.assertEqual(data, [])

    def test_read_moderators_nonexistent_community(self):
        # Try to get moderators of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
