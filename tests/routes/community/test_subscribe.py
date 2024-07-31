# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestSubscribe(BaseTestCase):
    route = '/community/<string:name>/subscribe/'

    def test_subscribe(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # subscribe to the community
        response = self.client.post(
            f'/community/{community.name}/subscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_subscribe_nonexistent(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # subscribe to the community
        response = self.client.post(
            '/community/nonexistent/subscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_subscribe_already_subscribed(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # subscribe user
        community.append_subscriber(user)

        # get user access token
        access_token = get_access_token(user)

        # subscribe to the community
        response = self.client.post(
            f'/community/{community.name}/subscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert response data
        self.assertEqual(data['message'], 'You are already subscribed to this community.')

    def test_subscribe_to_community_being_banned(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # ban user
        community.append_banned(user)

        # get user access token
        access_token = get_access_token(user)

        # subscribe to the community
        response = self.client.post(
            f'/community/{community.name}/subscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert response data
        self.assertEqual(data['message'], 'You are banned from this community.')