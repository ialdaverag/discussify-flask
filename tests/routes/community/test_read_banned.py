# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunityModerator
from app.models.community import CommunityBan


class TestReadBanned(BaseTestCase):
    route = '/community/{}/banned'

    def test_read_banned(self):
        # Create a user
        users = UserFactory.create_batch(size=5)

        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunityModerator(community=community, user=owner).save()

        # Get the access token
        access_token = get_access_token(owner)

        # Append the users to the community banned users
        for user in users:
            CommunityBan(community=community, user=user).save()

        # Read the community banned users
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

    def test_read_banned_empty(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Get the access token
        access_token = get_access_token(owner)

        # Read the community banned users
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])

    def test_read_banned_nonexistent_community(self):
        # Try to get banned users of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert the keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
        