# Tests
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.community import CommunityBan


class TestMod(TestRoute):
    route = '/community/{}/mod/{}'

    def test_add_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the user access token
        access_token = get_access_token(community.owner)

        # Add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 204)

    def test_add_moderator_nonexistent_community(self):
        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Add moderator to the community
        response = self.client.post(
            self.route.format('nonexistent', user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')

    def test_add_moderator_nonexistent_user(self):
        # Create a community
        community = CommunityFactory()

        # Get the user access token
        access_token = get_access_token(community.owner)

        # Add moderator to the community
        response = self.client.post(
            self.route.format(community.name, 'nonexistent'),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'User not found.')

    def test_add_moderator_not_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 403)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not the owner of this community.')

    def test_add_moderator_not_subscribed_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(community.owner)

        # Add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'The user is not subscribed to this community.')

    def test_add_moderator_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunityBan(community=community, user=user).save()

        # Get the user access token
        access_token = get_access_token(community.owner)

        # Add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'The user is banned from this community.')

    def test_add_moderator_already_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunityModerator(community=community, user=user).save()

        # Get the user access token
        access_token = get_access_token(community.owner)

        # Add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'The user is not subscribed to this community.')
