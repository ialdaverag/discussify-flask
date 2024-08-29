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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - 2)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - 2)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n - 4)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

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

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for subscriber in data:
            self.assertIn('id', subscriber)
            self.assertIn('username', subscriber)
            self.assertIn('email', subscriber)
            self.assertIn('following', subscriber)
            self.assertIn('follower', subscriber)
            self.assertIn('stats', subscriber)
            self.assertIn('created_at', subscriber)
            self.assertIn('updated_at', subscriber)

    def test_read_subscribers_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community subscribers
        response = self.client.get(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
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
