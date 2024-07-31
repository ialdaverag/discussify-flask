# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestBan(BaseTestCase):
    route = '/community/<string:name>/ban/<string:username>'

    def test_ban(self):
        # create a community
        community = CommunityFactory()

        community.append_moderator(community.owner)

        # create a user
        user = UserFactory()

        # subscribe user
        community.append_subscriber(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            f'/community/{community.name}/ban/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_ban_nonexistent_community(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # ban user from the community
        response = self.client.post(
            '/community/nonexistent/ban/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_ban_nonexistent_user(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            f'/community/{community.name}/ban/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)


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
            f'/community/{community.name}/ban/{user_to_ban.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 401)

        # get response data
        data = response.json

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
            f'/community/{community.name}/ban/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 401)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'You are not a moderator of this community.')

    def test_ban_banned_user(self):
        # create a community
        community = CommunityFactory()

        community.append_moderator(community.owner)

        # create the user to ban
        user_to_ban = UserFactory()

        # ban the user
        community.append_banned(user_to_ban)

        # get user access token
        access_token = get_access_token(community.owner)

        # ban the user again
        response = self.client.post(
            f'/community/{community.name}/ban/{user_to_ban.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'The user is already banned from the community.')
