# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUnban(BaseTestCase):
    route = '/community/{}/unban/{}'

    def test_unban(self):
        # Create a community
        community = CommunityFactory()

        # Append the owner as a moderator
        community.append_moderator(community.owner)

        # Create a user
        user = UserFactory()

        # Append the user to the community banned users
        community.append_banned(user)

        # Get user access token
        access_token = get_access_token(community.owner)

        # Ban user from the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 204)

    def test_unban_user_nonexistent_community(self):
        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Get the user access token
        access_token = get_access_token(user1)

        # Ban user from the community
        response = self.client.post(
            self.route.format('nonexistent', user2.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert the response data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'Community not found.')

    def test_unban_user_nonexistent_user(self):
        # Create a community
        community = CommunityFactory()

        # Get the user access token
        access_token = get_access_token(community.owner)

        # Ban user from the community
        response = self.client.post(
            self.route.format(community.name, 'nonexistent'),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert the response data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')

    def test_unban_user_not_being_moderator(self):
        # create a community
        community = CommunityFactory()

        user1 = UserFactory()

        # create a user
        user2 = UserFactory()

        # ban a user
        community.append_banned(user2)

        # get user access token
        access_token = get_access_token(user1)

        # ban user from the community
        response = self.client.post(
            self.route.format(community.name, user2.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 401)

        # Get the response data
        data = response.json

        # Assert the response data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'You are not a moderator of this community.')

    def test_unban_user_not_banned(self):
        # create a community
        community = CommunityFactory()

        community.append_moderator(community.owner)

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert the response data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'The user is not banned from the community.')