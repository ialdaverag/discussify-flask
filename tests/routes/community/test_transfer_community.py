# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestTransfer(BaseTestCase):
    route = '/community/{}/transfer/{}'

    def test_transfer(self):
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
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_transfer_nonexistent_community(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # add moderator to the community
        response = self.client.post(
            self.route.format('nonexistent', user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_transfer_nonexistent_user(self):
        # create a community
        community = CommunityFactory()

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            self.route.format(community.name, 'nonexistent'),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_transfer_not_being_owner(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)

    def test_transfer_not_subscribed_user(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get the owner of the community
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert response data structure
        self.assertIn('message', data)

        # assert response data value
        self.assertEqual(data['message'], 'The user is not subscribed to this community.')

    def test_transfer_community_banned_user(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get the owner of the community
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # append banned user to the community
        community.append_banned(user)

        # add moderator to the community
        response = self.client.post(
            self.route.format(community.name, user.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert response data structure
        self.assertIn('message', data)

        # assert response data value
        self.assertEqual(data['message'], 'You cannot transfer the community to a banned user.')

    def test_transfer_user_already_owner(self):
        # create a community
        community = CommunityFactory()

        # get the owner of the community
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # add moderator to the community
        response = self.client.post(
            self.route.format(community.name, owner.username),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)

        # get response data
        data = response.json

        # assert response data structure
        self.assertIn('message', data)

        # assert response data value
        self.assertEqual(data['message'], 'You are already the owner of this community.')

    