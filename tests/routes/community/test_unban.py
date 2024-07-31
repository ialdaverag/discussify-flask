# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestUnban(BaseTestCase):
    route = '/community/<string:name>/unban/<string:username>'

    def test_unban(self):
        # create a community
        community = CommunityFactory()

        community.append_moderator(community.owner)

        # create a user
        user = UserFactory()

        # ban a user
        community.append_banned(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            f'/community/{community.name}/unban/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_unban_nonexistent_community(self):
        # create a user
        user1 = UserFactory()
        user2 = UserFactory()

        # get user access token
        access_token = get_access_token(user1)

        # ban user from the community
        response = self.client.post(
            f'/community/nonexistent/unban/{user2.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_unban_nonexistent_user(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # ban user from the community
        response = self.client.post(
            f'/community/{community.name}/unban/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

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
            f'/community/{community.name}/unban/{user2.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 401)

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
            f'/community/{community.name}/unban/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)