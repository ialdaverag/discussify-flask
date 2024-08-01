# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestDeleteCommunity(BaseTestCase):
    route = '/community/{}'

    def test_delete_community(self):
        # Create a community
        community = CommunityFactory()

        # Get the community owner
        owner = community.owner

        # Get owner access token
        access_token = get_access_token(owner)

        # Delete the community
        response = self.client.delete(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Rssert the response status code
        self.assertEqual(response.status_code, 204)

    def test_delete_community_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Delete the community
        response = self.client.delete(
            '/community/inexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('message', data)

        # Assert the error
        self.assertEqual(data['message'], 'Community not found.')

    def test_delete_community_not_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Delete the community
        response = self.client.delete(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 403)
        
        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('message', data)

        # Assert the error
        self.assertEqual(data['message'], 'You are not the owner of this community.')
