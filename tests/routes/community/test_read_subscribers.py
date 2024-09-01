# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token

class TestReadSubscribers(BaseTestCase):
    route = '/community/{}/subscribers'
    route_with_args = '/community/{}/subscribers?page={}&per_page={}'

    def test_read_subscribers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Read the community subscribers
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

    def test_read_subscribers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Read the community subscribers
        response = self.client.get(self.route_with_args.format(community.name, 1, 5))

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
        self.assertEqual(pagination['per_page'], 5)

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

    def test_read_subscribers_as_user(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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

    def test_read_subscribers_as_user_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

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

    def test_read_subscribers_as_user_with_blocked(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['total'], n - b)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - b)

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

    def test_read_subscribers_as_user_with_blocked_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

        # Assert the total
        self.assertEqual(pagination['total'], n - b)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - b)

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

    def test_read_subscribers_as_user_with_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['total'], n - b)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - b)

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

    def test_read_subscribers_as_user_with_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

        # Assert the total
        self.assertEqual(pagination['total'], n - b)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - b)

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

    def test_read_subscribers_as_user_with_blocked_and_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['total'], n - b - c)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - b - c)

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

    def test_read_subscribers_as_user_with_blocked_and_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

        # Assert the total
        self.assertEqual(pagination['total'], n - b - c)

        # Get the users
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - b - c)

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

    def test_read_subscribers_as_moderator(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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

    def test_read_subscribers_as_moderator_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

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

    def test_read_subscribers_as_moderator_with_blocked(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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

    def test_read_subscribers_as_moderator_with_blocked_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

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

    def test_read_subscribers_as_moderator_with_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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

    def test_read_subscribers_as_moderator_with_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

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

    def test_read_subscribers_as_moderator_with_blocked_and_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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

    def test_read_subscribers_as_moderator_with_blocked_and_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

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
        self.assertEqual(pagination['per_page'], 5)

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

    def test_read_subscribers_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community subscribers
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

    def test_read_subscribers_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Read the community subscribers
        response = self.client.get(self.route_with_args.format(community.name, 1, 5))

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
        self.assertEqual(pagination['per_page'], 5)

        # Assert the total
        self.assertEqual(pagination['total'], 0)

        # Get response data
        data = pagination['users']

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the response data
        self.assertEqual(data, [])

    def test_read_subscribers_nonexistent_community(self):
        # Try to get subscribers of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
