# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadBlocked(BaseTestCase):
    route = '/user/blocked'

    def test_read_blocked(self):
        # Number of blocked users
        n = 5

        # create a user
        user = UserFactory()

        # Create some users to block
        users = UserFactory.create_batch(n)

        # Block all users
        for u in users:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
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

        # Assert the response data
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

    def test_read_blocked_args(self):
        # Number of blocked users
        n = 15

        # create a user
        user = UserFactory()

        # Create some users to block
        users = UserFactory.create_batch(n)

        # Block all users
        for u in users:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Get the blocked
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            query_string=args
        )

        # Assert the response status code
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
        self.assertEqual(pagination['pages'], 8)

        # Assert the per page
        self.assertEqual(pagination['per_page'], 2)

        # Assert the total
        self.assertEqual(pagination['total'], n)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data
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

    def test_read_blocked_empty(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
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
        self.assertEqual(len(data), 0)

        # Assert the response data structure
        self.assertEqual(data, [])

    def test_read_blocked_empty_args(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
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
        self.assertEqual(len(data), 0)

        # Assert the response data structure
        self.assertEqual(data, [])

        