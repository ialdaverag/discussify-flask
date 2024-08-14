# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunitySubscriber


class TestUnsubscribe(BaseTestCase):
    route = '/community/{}/unsubscribe'

    def test_unsubscribe(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Unsubscribe from the community
        response = self.client.post(
            f'/community/{community.name}/unsubscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 204)

    def test_unsubscribe_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Unsubscribe from the community
        response = self.client.post(
            '/community/nonexistent/unsubscribe',
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

    def test_unsubscribe_not_being_subscribed(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Unsubscribe from the community
        response = self.client.post(
            f'/community/{community.name}/unsubscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_unsubscribe_to_community_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Get the user access token
        access_token = get_access_token(owner)

        # Unsubscribe from the community
        response = self.client.post(
            f'/community/{community.name}/unsubscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 403)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are the owner of this community and cannot unsubscribe.')