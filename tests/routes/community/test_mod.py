# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestMod(BaseTestCase):
    route = '/community/<string:name>/mod/<string:username>'

    def test_add_moderator(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # subscribe user
        community.append_subscriber(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/mod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_add_moderator_nonexistent_community(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # add moderator to the community
        response = self.client.post(
            '/community/nonexistent/mod/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_add_moderator_nonexistent_user(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/mod/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_add_moderator_not_owner(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/mod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)

    def test_add_moderator_not_subscribed_user(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/mod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

    def test_add_moderator_banned_user(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # ban user
        community.append_banned(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/mod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

    def test_add_moderator_already_moderator(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # add user as moderator
        community.append_moderator(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/mod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)
