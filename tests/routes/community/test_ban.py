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


class TestBan(TestRoute):
    route = '/community/{}/ban/{}'

    def test_ban(self):
        # create a community
        community = CommunityFactory()

        
        CommunityModerator(community=community, user=community.owner).save()

        # create a user
        user = UserFactory()

        # subscribe user
        CommunitySubscriber(community=community, user=user).save()

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertStatusCode(response, 204)

    def test_ban_nonexistent_community(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # ban user from the community
        response = self.client.post(
            self.route.format('nonexistent', user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertStatusCode(response, 404)

        # get response data
        data = response.json

        # assert the keys in the response data
        self.assertIn('message', data)

        # assert the message
        self.assertEqual(data['message'], 'Community not found.')

    def test_ban_nonexistent_user(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            self.route.format(community.name, 'nonexistent'),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertStatusCode(response, 404)

        # get response data
        data = response.json

        # assert the keys in the response data
        self.assertIn('message', data)

        # assert the message
        self.assertEqual(data['message'], 'User not found.')


    def test_ban_not_being_moderator(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # create the user to ban
        user_to_ban = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # ban user from the community
        response = self.client.post(
            self.route.format(community.name, user_to_ban.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertStatusCode(response, 401)

        # get response data
        data = response.json

        # assert keys in the response data
        self.assertIn('message', data)

        # assert the error
        self.assertEqual(data['message'], 'You are not a moderator of this community.')

    def test_ban_not_subscribed(self):
        # create a community
        community = CommunityFactory()

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
        self.assertStatusCode(response, 401)

        # get response data
        data = response.json

        # assert keys in the response data
        self.assertIn('message', data)

        # assert the error
        self.assertEqual(data['message'], 'You are not a moderator of this community.')

    def test_ban_banned_user(self):
        # create a community
        community = CommunityFactory()

        CommunityModerator(community=community, user=community.owner).save()

        # create the user to ban
        user_to_ban = UserFactory()

        # ban the user
        CommunityBan(community=community, user=user_to_ban).save()

        # get user access token
        access_token = get_access_token(community.owner)

        # ban the user again
        response = self.client.post(
            self.route.format(community.name, user_to_ban.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # get response data
        data = response.json

        # assert keys in the response data
        self.assertIn('message', data)

        # assert the error
        self.assertEqual(data['message'], 'The user is already banned from the community.')
