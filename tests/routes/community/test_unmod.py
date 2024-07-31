# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestUnmod(BaseTestCase):

    def test_unmod(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # add moderator to the community
        community.append_moderator(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # remove moderator from the community
        response = self.client.post(
            f'/community/{community.name}/unmod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_unmod_nonexistent_community(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # remove moderator from the community
        response = self.client.post(
            '/community/nonexistent/unmod/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_unmod_nonexistent_user(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # remove moderator from the community
        response = self.client.post(
            f'/community/{community.name}/unmod/nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_unmod_not_owner(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # remove moderator from the community
        response = self.client.post(
            f'/community/{community.name}/unmod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'You are not the owner of this community.')

    def test_unmod_being_owner(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # remove moderator from the community
        response = self.client.post(
            f'/community/{community.name}/unmod/{community.owner.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'You are the owner of this community and cannot unmod yourself.')

    def test_unmod_not_moderator(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # remove moderator from the community
        response = self.client.post(
            f'/community/{community.name}/unmod/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'The user is not a moderator of this community.')