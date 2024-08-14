# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan


class TestSubscribe(BaseTestCase):
    route = '/community/{}/subscribe'

    def test_subscribe(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Subscribe to the community
        response = self.client.post(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 204)

    def test_subscribe_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Subscribe to the community
        response = self.client.post(
            self.route.format('nonexistent'),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')

    def test_subscribe_already_subscribed(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Subscribe to the community
        response = self.client.post(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are already subscribed to this community.')

    def test_subscribe_to_community_being_banned(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community banned users
        CommunityBan(community=community, user=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Subscribe to the community
        response = self.client.post(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')