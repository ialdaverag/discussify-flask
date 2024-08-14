# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunityModerator


class TestUnmod(BaseTestCase):
    route = '/community/{}/unmod/{}'

    def test_unmod(self):
        # create a community
        community = CommunityFactory()

        # Get the community owner
        owner = community.owner

        # create a user
        user = UserFactory()

        # add moderator to the community
        CommunityModerator(community=community, user=user).save()

        # get user access token
        access_token = get_access_token(owner)

        # remove moderator from the community
        response = self.client.post(
            self.route.format(community.name, user.username),
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
            self.route.format('nonexistent', user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

        # get response data
        data = response.json

        # assert key in data
        self.assertIn('message', data)

        # assert the error
        self.assertEqual(data['message'], 'Community not found.')

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

        # get response data
        data = response.json

        # assert key in data
        self.assertIn('message', data)

        # assert the error
        self.assertEqual(data['message'], 'User not found.')

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

        # assert keys in data
        self.assertIn('message', data)

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

        # assert keys in data
        self.assertIn('message', data)

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

        # assert keys in data
        self.assertIn('message', data)

        # assert the error
        self.assertEqual(data['message'], 'The user is not a moderator of this community.')